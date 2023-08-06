import posixpath
from six.moves import urllib

from mlflow.exceptions import MlflowException

_INVALID_DB_URI_MSG = (
    "Please refer to https://mlflow.org/docs/latest/tracking.html#storage for "
    "format specifications."
)


def is_local_uri(uri):
    """Returns true if this is a local file path (/foo or file:/foo)."""
    scheme = urllib.parse.urlparse(uri).scheme
    return uri != "databricks" and (scheme == "" or scheme == "file")


def is_http_uri(uri):
    scheme = urllib.parse.urlparse(uri).scheme
    return scheme == "http" or scheme == "https"


def is_databricks_uri(uri):
    """
    Databricks URIs look like 'databricks' (default profile) or 'databricks://profile'
    or 'databricks://secret_scope:secret_key_prefix'.
    """
    scheme = urllib.parse.urlparse(uri).scheme
    return scheme == "databricks" or uri == "databricks"


def construct_db_uri_from_profile(profile):
    if profile:
        return "databricks://" + profile


# Both scope and key_prefix should not contain special chars for URIs, like '/'
# and ':'.
def validate_db_scope_prefix_info(scope, prefix):
    for c in ["/", ":", " "]:
        if c in scope:
            raise MlflowException(
                "Unsupported Databricks profile name: %s." % scope
                + " Profile names cannot contain '%s'." % c
            )
        if prefix and c in prefix:
            raise MlflowException(
                "Unsupported Databricks profile key prefix: %s." % prefix
                + " Key prefixes cannot contain '%s'." % c
            )
    if prefix is not None and prefix.strip() == "":
        raise MlflowException(
            "Unsupported Databricks profile key prefix: '%s'." % prefix
            + " Key prefixes cannot be empty."
        )


def get_db_info_from_uri(uri):
    """
    Get the Databricks profile specified by the tracking URI (if any), otherwise
    returns None.
    """
    parsed_uri = urllib.parse.urlparse(uri)
    if parsed_uri.scheme == "databricks":
        profile_tokens = parsed_uri.netloc.split(":")
        parsed_scope = profile_tokens[0]
        if len(profile_tokens) == 1:
            parsed_key_prefix = None
        elif len(profile_tokens) == 2:
            parsed_key_prefix = profile_tokens[1]
        else:
            # parse the content before the first colon as the profile.
            parsed_key_prefix = ":".join(profile_tokens[1:])
        validate_db_scope_prefix_info(parsed_scope, parsed_key_prefix)
        return parsed_scope, parsed_key_prefix
    return None, None


def get_databricks_profile_uri_from_artifact_uri(uri):
    """
    Retrieves the netloc portion of the URI as a ``databricks://`` URI,
    if it is a proper Databricks profile specification, e.g.
    ``profile@databricks`` or ``secret_scope:key_prefix@databricks``.
    """
    parsed = urllib.parse.urlparse(uri)
    if not parsed.netloc or parsed.hostname != "databricks":
        return None
    if not parsed.username:  # no profile or scope:key
        return "databricks"  # the default tracking/registry URI
    validate_db_scope_prefix_info(parsed.username, parsed.password)
    key_prefix = ":" + parsed.password if parsed.password else ""
    return "databricks://" + parsed.username + key_prefix


def remove_databricks_profile_info_from_artifact_uri(artifact_uri):
    """
    Only removes the netloc portion of the URI if it is a Databricks
    profile specification, e.g.
    ``profile@databricks`` or ``secret_scope:key_prefix@databricks``.
    """
    parsed = urllib.parse.urlparse(artifact_uri)
    if not parsed.netloc or parsed.hostname != "databricks":
        return artifact_uri
    return urllib.parse.urlunparse(parsed._replace(netloc=""))


def add_databricks_profile_info_to_artifact_uri(artifact_uri, databricks_profile_uri):
    """
    Throws an exception if ``databricks_profile_uri`` is not valid.
    """
    if not databricks_profile_uri or not is_databricks_uri(databricks_profile_uri):
        return artifact_uri
    artifact_uri_parsed = urllib.parse.urlparse(artifact_uri)
    # Do not overwrite the authority section if there is already one
    if artifact_uri_parsed.netloc:
        return artifact_uri

    scheme = artifact_uri_parsed.scheme
    if scheme == "dbfs" or scheme == "runs" or scheme == "models":
        if databricks_profile_uri == "databricks":
            netloc = "databricks"
        else:
            (profile, key_prefix) = get_db_info_from_uri(databricks_profile_uri)
            prefix = ":" + key_prefix if key_prefix else ""
            netloc = profile + prefix + "@databricks"
        new_parsed = artifact_uri_parsed._replace(netloc=netloc)
        return urllib.parse.urlunparse(new_parsed)
    else:
        return artifact_uri


def extract_and_normalize_path(uri):
    parsed_uri_path = urllib.parse.urlparse(uri).path
    normalized_path = posixpath.normpath(parsed_uri_path)
    return normalized_path.lstrip("/")


def is_databricks_acled_artifacts_uri(artifact_uri):
    _ACLED_ARTIFACT_URI = "databricks/mlflow-tracking/"
    artifact_uri_path = extract_and_normalize_path(artifact_uri)
    return artifact_uri_path.startswith(_ACLED_ARTIFACT_URI)


def is_databricks_model_registry_artifacts_uri(artifact_uri):
    _MODEL_REGISTRY_ARTIFACT_URI = "databricks/mlflow-registry/"
    artifact_uri_path = extract_and_normalize_path(artifact_uri)
    return artifact_uri_path.startswith(_MODEL_REGISTRY_ARTIFACT_URI)


def is_valid_dbfs_uri(uri):
    parsed = urllib.parse.urlparse(uri)
    if parsed.scheme != "dbfs":
        return False
    try:
        db_profile_uri = get_databricks_profile_uri_from_artifact_uri(uri)
    except MlflowException:
        db_profile_uri = None
    return not parsed.netloc or db_profile_uri is not None
