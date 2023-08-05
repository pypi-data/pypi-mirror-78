"""
Internal package providing a Python CRUD interface to MLflow experiments, runs, registered models,
and model versions. This is a lower level API than the :py:mod:`mlflow.tracking.fluent` module,
and is exposed in the :py:mod:`mlflow.tracking` module.
"""
import logging

from mlflow.entities import ViewType
from mlflow.entities.model_registry.model_version_stages import ALL_STAGES
from mlflow.exceptions import MlflowException
from mlflow.protos.databricks_pb2 import FEATURE_DISABLED
from mlflow.store.model_registry import SEARCH_REGISTERED_MODEL_MAX_RESULTS_DEFAULT
from mlflow.store.tracking import SEARCH_MAX_RESULTS_DEFAULT
from mlflow.tracking._model_registry.client import ModelRegistryClient
from mlflow.tracking._model_registry import utils as registry_utils
from mlflow.tracking._tracking_service import utils
from mlflow.tracking._tracking_service.client import TrackingServiceClient
from mlflow.tracking.artifact_utils import _upload_artifacts_to_databricks
from mlflow.tracking.registry import UnsupportedModelRegistryStoreURIException
from mlflow.utils.annotations import experimental
from mlflow.utils.databricks_utils import (
    is_databricks_default_tracking_uri,
    is_in_databricks_job,
    is_in_databricks_notebook,
    get_workspace_info_from_dbutils,
    get_workspace_info_from_databricks_secrets,
)
from mlflow.utils.logging_utils import eprint
from mlflow.utils.uri import is_databricks_uri, construct_run_url

_logger = logging.getLogger(__name__)


class MlflowClient(object):
    """
    Client of an MLflow Tracking Server that creates and manages experiments and runs, and of an
    MLflow Registry Server that creates and manages registered models and model versions. It's a
    thin wrapper around TrackingServiceClient and RegistryClient so there is a unified API but we
    can keep the implementation of the tracking and registry clients independent from each other.
    """

    def __init__(self, tracking_uri=None, registry_uri=None):
        """
        :param tracking_uri: Address of local or remote tracking server. If not provided, defaults
                             to the service set by ``mlflow.tracking.set_tracking_uri``. See
                             `Where Runs Get Recorded <../tracking.html#where-runs-get-recorded>`_
                             for more info.
        :param registry_uri: Address of local or remote model registry server. If not provided,
                             defaults to the service set by ``mlflow.tracking.set_registry_uri``. If
                             no such service was set, defaults to the tracking uri of the client.
        """
        final_tracking_uri = utils._resolve_tracking_uri(tracking_uri)
        self._registry_uri = registry_utils._resolve_registry_uri(registry_uri, tracking_uri)
        self._tracking_client = TrackingServiceClient(final_tracking_uri)
        # `MlflowClient` also references a `ModelRegistryClient` instance that is provided by the
        # `MlflowClient._get_registry_client()` method. This `ModelRegistryClient` is not explicitly
        # defined as an instance variable in the `MlflowClient` constructor; an instance variable
        # is assigned lazily by `MlflowClient._get_registry_client()` and should not be referenced
        # outside of the `MlflowClient._get_registry_client()` method

    def _get_registry_client(self):
        """
        Attempts to create a py:class:`ModelRegistryClient` if one does not already exist.

        :raises: py:class:`mlflow.exceptions.MlflowException` if the py:class:`ModelRegistryClient`
                 cannot be created. This may occur, for example, when the registry URI refers
                 to an unsupported store type (e.g., the FileStore).
        :return: A py:class:`ModelRegistryClient` instance
        """
        # Attempt to fetch a `ModelRegistryClient` that is lazily instantiated and defined as
        # an instance variable on this `MlflowClient` instance. Because the instance variable
        # is undefined until the first invocation of _get_registry_client(), the `getattr()`
        # function is used to safely fetch the variable (if it is defined) or a NoneType
        # (if it is not defined)
        registry_client_attr = "_registry_client_lazy"
        registry_client = getattr(self, registry_client_attr, None)
        if registry_client is None:
            try:
                registry_client = ModelRegistryClient(self._registry_uri)
                # Define an instance variable on this `MlflowClient` instance to reference the
                # `ModelRegistryClient` that was just constructed. `setattr()` is used to ensure
                # that the variable name is consistent with the variable name specified in the
                # preceding call to `getattr()`
                setattr(self, registry_client_attr, registry_client)
            except UnsupportedModelRegistryStoreURIException as exc:
                raise MlflowException(
                    "Model Registry features are not supported by the store with URI:"
                    " '{uri}'. Stores with the following URI schemes are supported:"
                    " {schemes}.".format(uri=self._registry_uri, schemes=exc.supported_uri_schemes),
                    FEATURE_DISABLED,
                )
        return registry_client

    # Tracking API

    def get_run(self, run_id):
        """
        Fetch the run from backend store. The resulting :py:class:`Run <mlflow.entities.Run>`
        contains a collection of run metadata -- :py:class:`RunInfo <mlflow.entities.RunInfo>`,
        as well as a collection of run parameters, tags, and metrics --
        :py:class:`RunData <mlflow.entities.RunData>`. In the case where multiple metrics with the
        same key are logged for the run, the :py:class:`RunData <mlflow.entities.RunData>` contains
        the most recently logged value at the largest step for each metric.

        :param run_id: Unique identifier for the run.

        :return: A single :py:class:`mlflow.entities.Run` object, if the run exists. Otherwise,
                 raises an exception.
        """
        return self._tracking_client.get_run(run_id)

    def get_metric_history(self, run_id, key):
        """
        Return a list of metric objects corresponding to all values logged for a given metric.

        :param run_id: Unique identifier for run
        :param key: Metric name within the run

        :return: A list of :py:class:`mlflow.entities.Metric` entities if logged, else empty list
        """
        return self._tracking_client.get_metric_history(run_id, key)

    def create_run(self, experiment_id, start_time=None, tags=None):
        """
        Create a :py:class:`mlflow.entities.Run` object that can be associated with
        metrics, parameters, artifacts, etc.
        Unlike :py:func:`mlflow.projects.run`, creates objects but does not run code.
        Unlike :py:func:`mlflow.start_run`, does not change the "active run" used by
        :py:func:`mlflow.log_param`.

        :param experiment_id: The ID of then experiment to create a run in.
        :param start_time: If not provided, use the current timestamp.
        :param tags: A dictionary of key-value pairs that are converted into
                     :py:class:`mlflow.entities.RunTag` objects.
        :return: :py:class:`mlflow.entities.Run` that was created.
        """
        return self._tracking_client.create_run(experiment_id, start_time, tags)

    def list_run_infos(
        self,
        experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=SEARCH_MAX_RESULTS_DEFAULT,
        order_by=None,
        page_token=None,
    ):
        """:return: List of :py:class:`mlflow.entities.RunInfo`"""
        return self._tracking_client.list_run_infos(
            experiment_id, run_view_type, max_results, order_by, page_token
        )

    def list_experiments(self, view_type=None):
        """
        :return: List of :py:class:`mlflow.entities.Experiment`
        """
        return self._tracking_client.list_experiments(view_type)

    def get_experiment(self, experiment_id):
        """
        Retrieve an experiment by experiment_id from the backend store

        :param experiment_id: The experiment ID returned from ``create_experiment``.
        :return: :py:class:`mlflow.entities.Experiment`
        """
        return self._tracking_client.get_experiment(experiment_id)

    def get_experiment_by_name(self, name):
        """
        Retrieve an experiment by experiment name from the backend store

        :param name: The experiment name.
        :return: :py:class:`mlflow.entities.Experiment`
        """
        return self._tracking_client.get_experiment_by_name(name)

    def create_experiment(self, name, artifact_location=None):
        """Create an experiment.

        :param name: The experiment name. Must be unique.
        :param artifact_location: The location to store run artifacts.
                                  If not provided, the server picks an appropriate default.
        :return: Integer ID of the created experiment.
        """
        return self._tracking_client.create_experiment(name, artifact_location)

    def delete_experiment(self, experiment_id):
        """
        Delete an experiment from the backend store.

        :param experiment_id: The experiment ID returned from ``create_experiment``.
        """
        self._tracking_client.delete_experiment(experiment_id)

    def restore_experiment(self, experiment_id):
        """
        Restore a deleted experiment unless permanently deleted.

        :param experiment_id: The experiment ID returned from ``create_experiment``.
        """
        self._tracking_client.restore_experiment(experiment_id)

    def rename_experiment(self, experiment_id, new_name):
        """
        Update an experiment's name. The new name must be unique.

        :param experiment_id: The experiment ID returned from ``create_experiment``.
        """
        self._tracking_client.rename_experiment(experiment_id, new_name)

    def log_metric(self, run_id, key, value, timestamp=None, step=None):
        """
        Log a metric against the run ID.

        :param run_id: The run id to which the metric should be logged.
        :param key: Metric name.
        :param value: Metric value (float). Note that some special values such
                      as +/- Infinity may be replaced by other values depending on the store. For
                      example, the SQLAlchemy store replaces +/- Inf with max / min float values.
        :param timestamp: Time when this metric was calculated. Defaults to the current system time.
        :param step: Integer training step (iteration) at which was the metric calculated.
                     Defaults to 0.
        """
        self._tracking_client.log_metric(run_id, key, value, timestamp, step)

    def log_param(self, run_id, key, value):
        """
        Log a parameter against the run ID. Value is converted to a string.
        """
        self._tracking_client.log_param(run_id, key, value)

    def set_experiment_tag(self, experiment_id, key, value):
        """
        Set a tag on the experiment with the specified ID. Value is converted to a string.

        :param experiment_id: String ID of the experiment.
        :param key: Name of the tag.
        :param value: Tag value (converted to a string).
        """
        self._tracking_client.set_experiment_tag(experiment_id, key, value)

    def set_tag(self, run_id, key, value):
        """
        Set a tag on the run with the specified ID. Value is converted to a string.

        :param run_id: String ID of the run.
        :param key: Name of the tag.
        :param value: Tag value (converted to a string)
        """
        self._tracking_client.set_tag(run_id, key, value)

    def delete_tag(self, run_id, key):
        """
        Delete a tag from a run. This is irreversible.

        :param run_id: String ID of the run
        :param key: Name of the tag
        """
        self._tracking_client.delete_tag(run_id, key)

    def log_batch(self, run_id, metrics=(), params=(), tags=()):
        """
        Log multiple metrics, params, and/or tags.

        :param run_id: String ID of the run
        :param metrics: If provided, List of Metric(key, value, timestamp) instances.
        :param params: If provided, List of Param(key, value) instances.
        :param tags: If provided, List of RunTag(key, value) instances.

        Raises an MlflowException if any errors occur.
        :return: None
        """
        self._tracking_client.log_batch(run_id, metrics, params, tags)

    def log_artifact(self, run_id, local_path, artifact_path=None):
        """
        Write a local file or directory to the remote ``artifact_uri``.

        :param local_path: Path to the file or directory to write.
        :param artifact_path: If provided, the directory in ``artifact_uri`` to write to.
        """
        self._tracking_client.log_artifact(run_id, local_path, artifact_path)

    def log_artifacts(self, run_id, local_dir, artifact_path=None):
        """
        Write a directory of files to the remote ``artifact_uri``.

        :param local_dir: Path to the directory of files to write.
        :param artifact_path: If provided, the directory in ``artifact_uri`` to write to.
        """
        self._tracking_client.log_artifacts(run_id, local_dir, artifact_path)

    def _record_logged_model(self, run_id, mlflow_model):
        """
        Record logged model info with the tracking server.

        :param run_id: run_id under which the model has been logged.
        :param mlflow_model: Model info to be recorded.
        """
        self._tracking_client._record_logged_model(run_id, mlflow_model)

    def list_artifacts(self, run_id, path=None):
        """
        List the artifacts for a run.

        :param run_id: The run to list artifacts from.
        :param path: The run's relative artifact path to list from. By default it is set to None
                     or the root artifact path.
        :return: List of :py:class:`mlflow.entities.FileInfo`
        """
        return self._tracking_client.list_artifacts(run_id, path)

    def download_artifacts(self, run_id, path, dst_path=None):
        """
        Download an artifact file or directory from a run to a local directory if applicable,
        and return a local path for it.

        :param run_id: The run to download artifacts from.
        :param path: Relative source path to the desired artifact.
        :param dst_path: Absolute path of the local filesystem destination directory to which to
                         download the specified artifacts. This directory must already exist.
                         If unspecified, the artifacts will either be downloaded to a new
                         uniquely-named directory on the local filesystem or will be returned
                         directly in the case of the LocalArtifactRepository.
        :return: Local path of desired artifact.
        """
        return self._tracking_client.download_artifacts(run_id, path, dst_path)

    def set_terminated(self, run_id, status=None, end_time=None):
        """Set a run's status to terminated.

        :param status: A string value of :py:class:`mlflow.entities.RunStatus`.
                       Defaults to "FINISHED".
        :param end_time: If not provided, defaults to the current time."""
        self._tracking_client.set_terminated(run_id, status, end_time)

    def delete_run(self, run_id):
        """
        Deletes a run with the given ID.
        """
        self._tracking_client.delete_run(run_id)

    def restore_run(self, run_id):
        """
        Restores a deleted run with the given ID.
        """
        self._tracking_client.restore_run(run_id)

    def search_runs(
        self,
        experiment_ids,
        filter_string="",
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=SEARCH_MAX_RESULTS_DEFAULT,
        order_by=None,
        page_token=None,
    ):
        """
        Search experiments that fit the search criteria.

        :param experiment_ids: List of experiment IDs, or a single int or string id.
        :param filter_string: Filter query string, defaults to searching all runs.
        :param run_view_type: one of enum values ACTIVE_ONLY, DELETED_ONLY, or ALL runs
                              defined in :py:class:`mlflow.entities.ViewType`.
        :param max_results: Maximum number of runs desired.
        :param order_by: List of columns to order by (e.g., "metrics.rmse"). The ``order_by`` column
                     can contain an optional ``DESC`` or ``ASC`` value. The default is ``ASC``.
                     The default ordering is to sort by ``start_time DESC``, then ``run_id``.
        :param page_token: Token specifying the next page of results. It should be obtained from
            a ``search_runs`` call.

        :return: A list of :py:class:`mlflow.entities.Run` objects that satisfy the search
            expressions. If the underlying tracking store supports pagination, the token for
            the next page may be obtained via the ``token`` attribute of the returned object.
        """
        return self._tracking_client.search_runs(
            experiment_ids, filter_string, run_view_type, max_results, order_by, page_token
        )

    # Registry API

    # Registered Model Methods

    @experimental
    def create_registered_model(self, name, tags=None, description=None):
        """
        Create a new registered model in backend store.

        :param name: Name of the new model. This is expected to be unique in the backend store.
        :param tags: A dictionary of key-value pairs that are converted into
                     :py:class:`mlflow.entities.model_registry.RegisteredModelTag` objects.
        :param description: Description of the model.
        :return: A single object of :py:class:`mlflow.entities.model_registry.RegisteredModel`
                 created by backend.
        """
        return self._get_registry_client().create_registered_model(name, tags, description)

    @experimental
    def rename_registered_model(self, name, new_name):
        """
        Update registered model name.

        :param name: Name of the registered model to update.
        :param new_name: New proposed name for the registered model.

        :return: A single updated :py:class:`mlflow.entities.model_registry.RegisteredModel` object.
        """
        self._get_registry_client().rename_registered_model(name, new_name)

    @experimental
    def update_registered_model(self, name, description=None):
        """
        Updates metadata for RegisteredModel entity. Input field ``description`` should be non-None.
        Backend raises exception if a registered model with given name does not exist.

        :param name: Name of the registered model to update.
        :param description: (Optional) New description.
        :return: A single updated :py:class:`mlflow.entities.model_registry.RegisteredModel` object.
        """
        if description is None:
            raise MlflowException("Attempting to update registered model with no new field values.")

        return self._get_registry_client().update_registered_model(
            name=name, description=description
        )

    @experimental
    def delete_registered_model(self, name):
        """
        Delete registered model.
        Backend raises exception if a registered model with given name does not exist.

        :param name: Name of the registered model to update.
        """
        self._get_registry_client().delete_registered_model(name)

    @experimental
    def list_registered_models(
        self, max_results=SEARCH_REGISTERED_MODEL_MAX_RESULTS_DEFAULT, page_token=None
    ):
        """
        List of all registered models

        :param max_results: Maximum number of registered models desired.
        :param page_token: Token specifying the next page of results. It should be obtained from
                           a ``list_registered_models`` call.
        :return: A PagedList of :py:class:`mlflow.entities.model_registry.RegisteredModel` objects
                 that can satisfy the search expressions. The pagination token for the next page
                 can be obtained via the ``token`` attribute of the object.
        """
        return self._get_registry_client().list_registered_models(max_results, page_token)

    @experimental
    def search_registered_models(
        self,
        filter_string=None,
        max_results=SEARCH_REGISTERED_MODEL_MAX_RESULTS_DEFAULT,
        order_by=None,
        page_token=None,
    ):
        """
        Search for registered models in backend that satisfy the filter criteria.

        :param filter_string: Filter query string, defaults to searching all registered
                models. Currently, it supports only a single filter condition as the name
                of the model, for example, ``name = 'model_name'`` or a search expression
                to match a pattern in the registered model name.
                For example, ``name LIKE 'Boston%'`` (case sensitive) or
                ``name ILIKE '%boston%'`` (case insensitive).
        :param max_results: Maximum number of registered models desired.
        :param order_by: List of column names with ASC|DESC annotation, to be used for ordering
                         matching search results.
        :param page_token: Token specifying the next page of results. It should be obtained from
                            a ``search_registered_models`` call.
        :return: A PagedList of :py:class:`mlflow.entities.model_registry.RegisteredModel` objects
                that satisfy the search expressions. The pagination token for the next page can be
                obtained via the ``token`` attribute of the object.

        .. code-block:: python
            :caption: Example

            import mlflow

            client = mlflow.tracking.MlflowClient()

            # Get search results filtered by the registered model name
            model_name="CordobaWeatherForecastModel"
            filter_string = "name='{}'".format(model_name)
            results = client.search_registered_models(filter_string=filter_string)
            print("-" * 80)
            for res in results:
                for mv in res.latest_versions:
                    print("name={}; run_id={}; version={}".format(mv.name, mv.run_id, mv.version))

            # Get search results filtered by the registered model name that matches
            # prefix pattern
            filter_string = "name LIKE 'Boston%'"
            results = client.search_registered_models(filter_string=filter_string)
            for res in results:
                for mv in res.latest_versions:
                print("name={}; run_id={}; version={}".format(mv.name, mv.run_id, mv.version))

            # Get all registered models and order them by ascending order of the names
            results = client.search_registered_models(order_by=["name ASC"])
            print("-" * 80)
            for res in results:
                for mv in res.latest_versions:
                    print("name={}; run_id={}; version={}".format(mv.name, mv.run_id, mv.version))

        .. code-block:: text
            :caption: Output

            ------------------------------------------------------------------------------------
            name=CordobaWeatherForecastModel; run_id=eaef868ee3d14d10b4299c4c81ba8814; version=1
            name=CordobaWeatherForecastModel; run_id=e14afa2f47a040728060c1699968fd43; version=2
            ------------------------------------------------------------------------------------
            name=BostonWeatherForecastModel; run_id=ddc51b9407a54b2bb795c8d680e63ff6; version=1
            name=BostonWeatherForecastModel; run_id=48ac94350fba40639a993e1b3d4c185d; version=2
            -----------------------------------------------------------------------------------
            name=AzureWeatherForecastModel; run_id=5fcec6c4f1c947fc9295fef3fa21e52d; version=1
            name=AzureWeatherForecastModel; run_id=8198cb997692417abcdeb62e99052260; version=3
            name=BostonWeatherForecastModel; run_id=ddc51b9407a54b2bb795c8d680e63ff6; version=1
            name=BostonWeatherForecastModel; run_id=48ac94350fba40639a993e1b3d4c185d; version=2
            name=CordobaWeatherForecastModel; run_id=eaef868ee3d14d10b4299c4c81ba8814; version=1
            name=CordobaWeatherForecastModel; run_id=e14afa2f47a040728060c1699968fd43; version=2

        """
        return self._get_registry_client().search_registered_models(
            filter_string, max_results, order_by, page_token
        )

    @experimental
    def get_registered_model(self, name):
        """
        :param name: Name of the registered model to update.
        :return: A single :py:class:`mlflow.entities.model_registry.RegisteredModel` object.
        """
        return self._get_registry_client().get_registered_model(name)

    @experimental
    def get_latest_versions(self, name, stages=None):
        """
        Latest version models for each requests stage. If no ``stages`` provided, returns the
        latest version for each stage.

        :param name: Name of the registered model to update.
        :param stages: List of desired stages. If input list is None, return latest versions for
                       for ALL_STAGES.
        :return: List of :py:class:`mlflow.entities.model_registry.ModelVersion` objects.
        """
        return self._get_registry_client().get_latest_versions(name, stages)

    @experimental
    def set_registered_model_tag(self, name, key, value):
        """
        Set a tag for the registered model.

        :param name: Registered model name.
        :param key: Tag key to log.
        :param value: Tag value log.
        :return: None
        """
        self._get_registry_client().set_registered_model_tag(name, key, value)

    @experimental
    def delete_registered_model_tag(self, name, key):
        """
        Delete a tag associated with the registered model.

        :param name: Registered model name.
        :param key: Registered model tag key.
        :return: None
        """
        self._get_registry_client().delete_registered_model_tag(name, key)

    # Model Version Methods

    @experimental
    def create_model_version(
        self, name, source, run_id, tags=None, run_link=None, description=None
    ):
        """
        Create a new model version from given source (artifact URI).

        :param name: Name for the containing registered model.
        :param source: Source path where the MLflow model is stored.
        :param run_id: Run ID from MLflow tracking server that generated the model
        :param tags: A dictionary of key-value pairs that are converted into
                     :py:class:`mlflow.entities.model_registry.ModelVersionTag` objects.
        :param run_link: Link to the run from an MLflow tracking server that generated this model.
        :param description: Description of the version.
        :return: Single :py:class:`mlflow.entities.model_registry.ModelVersion` object created by
                 backend.
        """
        tracking_uri = self._tracking_client.tracking_uri
        if not run_link and is_databricks_uri(tracking_uri) and tracking_uri != self._registry_uri:
            run_link = self._get_run_link(tracking_uri, run_id)
        new_source = source
        if is_databricks_uri(self._registry_uri) and tracking_uri != self._registry_uri:
            # Print out some info for user since the copy may take a while for large models.
            eprint(
                "=== Copying model files from the source location to the model"
                + " registry workspace ==="
            )
            new_source = _upload_artifacts_to_databricks(
                source, run_id, tracking_uri, self._registry_uri
            )
            # NOTE: we can't easily delete the target temp location due to the async nature
            # of the model version creation - printing to let the user know.
            eprint(
                "=== Source model files were copied to %s" % new_source
                + " in the model registry workspace. You may want to delete the files once the"
                + " model version is in 'READY' status. You can also find this location in the"
                + " `source` field of the created model version. ==="
            )
        return self._get_registry_client().create_model_version(
            name=name,
            source=new_source,
            run_id=run_id,
            tags=tags,
            run_link=run_link,
            description=description,
        )

    def _get_run_link(self, tracking_uri, run_id):
        # if using the default Databricks tracking URI and in a notebook, we can automatically
        # figure out the run-link.
        if is_databricks_default_tracking_uri(tracking_uri) and (
            is_in_databricks_notebook() or is_in_databricks_job()
        ):
            # use DBUtils to determine workspace information.
            workspace_host, workspace_id = get_workspace_info_from_dbutils()
        else:
            # in this scenario, we're not able to automatically extract the workspace ID
            # to proceed, and users will need to pass in a databricks profile with the scheme:
            # databricks://scope:prefix and store the host and workspace-ID as a secret in the
            # Databricks Secret Manager with scope=<scope> and key=<prefix>-workspaceid.
            workspace_host, workspace_id = get_workspace_info_from_databricks_secrets(tracking_uri)
            if not workspace_id:
                print(
                    "No workspace ID specified; if your Databricks workspaces share the same"
                    " host URL, you may want to specify the workspace ID (along with the host"
                    " information in the secret manager) for run lineage tracking. For more"
                    " details on how to specify this information in the secret manager,"
                    " please refer to the model registry documentation."
                )
        # retrieve experiment ID of the run for the URL
        experiment_id = self.get_run(run_id).info.experiment_id
        if workspace_host and run_id and experiment_id:
            return construct_run_url(workspace_host, experiment_id, run_id, workspace_id)

    @experimental
    def update_model_version(self, name, version, description=None):
        """
        Update metadata associated with a model version in backend.

        :param name: Name of the containing registered model.
        :param version: Version number of the model version.
        :param description: New description.

        :return: A single :py:class:`mlflow.entities.model_registry.ModelVersion` object.
        """
        if description is None:
            raise MlflowException("Attempting to update model version with no new field values.")

        return self._get_registry_client().update_model_version(
            name=name, version=version, description=description
        )

    @experimental
    def transition_model_version_stage(self, name, version, stage, archive_existing_versions=False):
        """
        Update model version stage.

        :param name: Registered model name.
        :param version: Registered model version.
        :param stage: New desired stage for this model version.
        :param archive_existing_versions: If this flag is set to ``True``, all existing model
            versions in the stage will be automically moved to the "archived" stage. Only valid
            when ``stage`` is ``"staging"`` or ``"production"`` otherwise an error will be raised.

        :return: A single :py:class:`mlflow.entities.model_registry.ModelVersion` object.
        """
        return self._get_registry_client().transition_model_version_stage(
            name, version, stage, archive_existing_versions
        )

    @experimental
    def delete_model_version(self, name, version):
        """
        Delete model version in backend.

        :param name: Name of the containing registered model.
        :param version: Version number of the model version.
        """
        self._get_registry_client().delete_model_version(name, version)

    @experimental
    def get_model_version(self, name, version):
        """
        :param name: Name of the containing registered model.
        :param version: Version number of the model version.
        :return: A single :py:class:`mlflow.entities.model_registry.ModelVersion` object.
        """
        return self._get_registry_client().get_model_version(name, version)

    @experimental
    def get_model_version_download_uri(self, name, version):
        """
        Get the download location in Model Registry for this model version.

        :param name: Name of the containing registered model.
        :param version: Version number of the model version.
        :return: A single URI location that allows reads for downloading.
        """
        return self._get_registry_client().get_model_version_download_uri(name, version)

    @experimental
    def search_model_versions(self, filter_string):
        """
        Search for model versions in backend that satisfy the filter criteria.

        :param filter_string: A filter string expression. Currently, it supports a single filter
                              condition either a name of model like ``name = 'model_name'`` or
                              ``run_id = '...'``.
        :return: PagedList of :py:class:`mlflow.entities.model_registry.ModelVersion` objects.

        .. code-block:: python
            :caption: Example

            import mlflow

            client = mlflow.tracking.MlflowClient()

            # Get all versions of the model filtered by name
            model_name = "CordobaWeatherForecastModel"
            filter_string = "name='{}'".format(model_name)
            results = client.search_model_versions(filter_string)
            print("-" * 80)
            for res in results:
                print("name={}; run_id={}; version={}".format(res.name, res.run_id, res.version))

            # Get the version of the model filtered by run_id
            run_id = "e14afa2f47a040728060c1699968fd43"
            filter_string = "run_id='{}'".format(run_id)
            results = client.search_model_versions(filter_string)
            print("-" * 80)
            for res in results:
                print("name={}; run_id={}; version={}".format(res.name, res.run_id, res.version))

        .. code-block:: text
            :caption: Output

            ------------------------------------------------------------------------------------
            name=CordobaWeatherForecastModel; run_id=eaef868ee3d14d10b4299c4c81ba8814; version=1
            name=CordobaWeatherForecastModel; run_id=e14afa2f47a040728060c1699968fd43; version=2
            ------------------------------------------------------------------------------------
            name=CordobaWeatherForecastModel; run_id=e14afa2f47a040728060c1699968fd43; version=2
        """
        return self._get_registry_client().search_model_versions(filter_string)

    @experimental
    def get_model_version_stages(self, name, version):  # pylint: disable=unused-argument
        """
        :return: A list of valid stages.
        """
        return ALL_STAGES

    @experimental
    def set_model_version_tag(self, name, version, key, value):
        """
        Set a tag for the model version.

        :param name: Registered model name.
        :param version: Registered model version.
        :param key: Tag key to log.
        :param value: Tag value to log.
        :return: None
        """
        self._get_registry_client().set_model_version_tag(name, version, key, value)

    @experimental
    def delete_model_version_tag(self, name, version, key):
        """
        Delete a tag associated with the model version.

        :param name: Registered model name.
        :param version: Registered model version.
        :param key: Tag key.
        :return: None
        """
        self._get_registry_client().delete_model_version_tag(name, version, key)
