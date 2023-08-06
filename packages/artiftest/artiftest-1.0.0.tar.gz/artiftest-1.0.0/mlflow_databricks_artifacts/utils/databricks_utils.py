import os
import logging
import subprocess

from mlflow.exceptions import MlflowException
from databricks_cli.configure import provider

from mlflow_databricks_artifacts.utils.rest_utils import MlflowHostCreds
from mlflow_databricks_artifacts.utils.uri import get_db_info_from_uri

_logger = logging.getLogger(__name__)


def _get_dbutils():
    try:
        import IPython

        ip_shell = IPython.get_ipython()
        if ip_shell is None:
            raise _NoDbutilsError
        return ip_shell.ns_table["user_global"]["dbutils"]
    except ImportError:
        raise _NoDbutilsError
    except KeyError:
        raise _NoDbutilsError


class _NoDbutilsError(Exception):
    pass


def _fail_malformed_databricks_auth(profile):
    raise MlflowException(
        "Got malformed Databricks CLI profile '%s'. Please make sure the "
        "Databricks CLI is properly configured as described at "
        "https://github.com/databricks/databricks-cli." % profile
    )


def get_databricks_host_creds(server_uri=None):
    """
    Reads in configuration necessary to make HTTP requests to a Databricks server. This
    uses the Databricks CLI's ConfigProvider interface to load the DatabricksConfig object.
    If no Databricks CLI profile is found corresponding to the server URI, this function
    will attempt to retrieve these credentials from the Databricks Secret Manager. For that to work,
    the server URI will need to be of the following format: "databricks://scope:prefix". In the
    Databricks Secret Manager, we will query for a secret in the scope "<scope>" for secrets with
    keys of the form "<prefix>-host" and "<prefix>-token". Note that this prefix *cannot* be empty
    if trying to authenticate with this method. If found, those host credentials will be used. This
    method will throw an exception if sufficient auth cannot be found.

    :param server_uri: A URI that specifies the Databricks profile you want to use for making
    requests.
    :return: :py:class:`mlflow.rest_utils.MlflowHostCreds` which includes the hostname and
        authentication information necessary to talk to the Databricks server.
    """
    profile, path = get_db_info_from_uri(server_uri)
    if not hasattr(provider, "get_config"):
        _logger.warning(
            "Support for databricks-cli<0.8.0 is deprecated and will be removed"
            " in a future version."
        )
        config = provider.get_config_for_profile(profile)
    elif profile:
        config = provider.ProfileConfigProvider(profile).get_config()
    else:
        config = provider.get_config()
    # if a path is specified, that implies a Databricks tracking URI of the form:
    # databricks://profile-name/path-specifier
    if (not config or not config.host) and path:
        dbutils = _get_dbutils()
        if dbutils:
            # Prefix differentiates users and is provided as path information in the URI
            key_prefix = path
            host = dbutils.secrets.get(scope=profile, key=key_prefix + "-host")
            token = dbutils.secrets.get(scope=profile, key=key_prefix + "-token")
            if host and token:
                config = provider.DatabricksConfig.from_token(
                    host=host, token=token, insecure=False
                )
    if not config or not config.host:
        _fail_malformed_databricks_auth(profile)

    insecure = hasattr(config, "insecure") and config.insecure

    if config.username is not None and config.password is not None:
        return MlflowHostCreds(
            config.host,
            username=config.username,
            password=config.password,
            ignore_tls_verification=insecure,
        )
    elif config.token:
        return MlflowHostCreds(config.host, token=config.token, ignore_tls_verification=insecure)
    _fail_malformed_databricks_auth(profile)


def is_dbfs_fuse_available():
    with open(os.devnull, "w") as devnull_stderr, open(os.devnull, "w") as devnull_stdout:
        try:
            return (
                subprocess.call(
                    ["mountpoint", "/dbfs"], stderr=devnull_stderr, stdout=devnull_stdout
                )
                == 0
            )
        except Exception:  # pylint: disable=broad-except
            return False
