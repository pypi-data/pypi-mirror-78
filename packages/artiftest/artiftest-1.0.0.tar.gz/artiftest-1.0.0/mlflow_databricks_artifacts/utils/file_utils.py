import codecs
import errno
import gzip
import os
import posixpath

from six.moves.urllib.request import pathname2url
from six.moves.urllib.parse import unquote


def relative_path_to_artifact_path(path):
    if os.path == posixpath:
        return path
    if os.path.abspath(path) == path:
        raise Exception("This method only works with relative paths.")
    return unquote(pathname2url(path))


def yield_file_in_chunks(file, chunk_size=100000000):
    """
    Generator to chunk-ify the inputted file based on the chunk-size.
    """
    with open(file, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                yield chunk
            else:
                break
