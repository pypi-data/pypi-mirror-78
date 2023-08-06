import json
import os
import posixpath

from mlflow.exceptions import MlflowException

try:
    from mlflow.store.artifact.dbfs_artifact_repo import DbfsRestArtifactRepository
    from mlflow.store.artifact.local_artifact_repo import LocalArtifactRepository
except ImportError:
    # Older versions of MLflow placed artifact repository implementations
    # in the top-level `mlflow.store` module, rather than the
    # `mlflow.store.artifact` module; `DbfsArtifactRepository` was also
    # renamed to `DbfsRestArtifactRepository`
    from mlflow.store.dbfs_artifact_repo import DbfsArtifactRepository as DbfsRestArtifactRepository
    from mlflow.store.local_artifact_repo import LocalArtifactRepository


def dbfs_artifact_repo_factory(artifact_uri):
    """
    Returns an ArtifactRepository subclass for storing artifacts on DBFS.

    This factory method is used with URIs of the form ``dbfs:/<path>``. DBFS-backed artifact
    storage can only be used together with the RestStore.

    In the special case where the URI is of the form
    `dbfs:/databricks/mlflow-tracking/<Exp-ID>/<Run-ID>/<path>',
    a DatabricksArtifactRepository is returned. This is capable of storing access controlled
    artifacts.

    :param artifact_uri: DBFS root artifact URI (string).
    :return: Subclass of ArtifactRepository capable of storing artifacts on DBFS.
    """
    # For some reason, we must import modules specific to this package within the
    # entrypoint function rather than the top-level module. Otherwise, entrypoint
    # registration fails with import errors
    from mlflow_databricks_artifacts.store.artifact_repo import DatabricksArtifactRepository
    from mlflow_databricks_artifacts.utils.databricks_utils import is_dbfs_fuse_available
    from mlflow_databricks_artifacts.utils.string_utils import strip_prefix
    from mlflow_databricks_artifacts.utils.uri import (
        get_databricks_profile_uri_from_artifact_uri,
        is_databricks_acled_artifacts_uri,
        is_databricks_model_registry_artifacts_uri,
        is_valid_dbfs_uri,
        remove_databricks_profile_info_from_artifact_uri,
    )

    if not is_valid_dbfs_uri(artifact_uri):
        raise MlflowException(
            "DBFS URI must be of the form dbfs:/<path> or "
            + "dbfs://profile@databricks/<path>, but received "
            + artifact_uri
        )

    cleaned_artifact_uri = artifact_uri.rstrip("/")
    db_profile_uri = get_databricks_profile_uri_from_artifact_uri(cleaned_artifact_uri)
    if is_databricks_acled_artifacts_uri(artifact_uri):
        return DatabricksArtifactRepository(cleaned_artifact_uri)
    elif (
        is_dbfs_fuse_available()
        and os.environ.get(USE_FUSE_ENV_VAR, "").lower() != "false"
        and not is_databricks_model_registry_artifacts_uri(artifact_uri)
        and (db_profile_uri is None or db_profile_uri == "databricks")
    ):
        # If the DBFS FUSE mount is available, write artifacts directly to
        # /dbfs/... using local filesystem APIs.
        # Note: it is possible for a named Databricks profile to point to the current workspace,
        # but we're going to avoid doing a complex check and assume users will use `databricks`
        # to mean the current workspace. Using `DbfsRestArtifactRepository` to access the current
        # workspace's DBFS should still work; it just may be slower.
        final_artifact_uri = remove_databricks_profile_info_from_artifact_uri(cleaned_artifact_uri)
        file_uri = "file:///dbfs/{}".format(strip_prefix(final_artifact_uri, "dbfs:/"))
        return LocalArtifactRepository(file_uri)
    return DbfsRestArtifactRepository(cleaned_artifact_uri)
