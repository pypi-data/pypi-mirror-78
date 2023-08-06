""" Generic utilities
"""
import os
import logging
from sermos_utils.constants import ENV_VAR_ACCESS_KEY, ENV_VAR_PKG_NAME

logger = logging.getLogger(__name__)


def normalized_pkg_name(pkg_name: str, dashed: bool = False):
    """ We maintain consistency by always specifying the package name as
        the "dashed version".

        Python/setuptools will replace "_" with "-" but resource_filename()
        expects the exact directory name, essentially. In order to keep it
        simple upstream and *always* provide package name as the dashed
        version, we do replacement here to 'normalize' both versions to
        whichever convention you need at the time.

        if `dashed`:
            my-package-name --> my-package-name
            my_package_name --> my-package-name

        else:
            my-package-name --> my_package_name
            my_package_name --> my_package_name
    """
    if dashed:
        return str(pkg_name).replace('_', '-')
    return str(pkg_name).replace('-', '_')


def get_access_key(access_key: str = None):
    """ Verify access key provided, get from environment if None.

        Raise if neither provided nor found.

        Arguments:
            access_key (optional): Access key, issued by Sermos, that
                dictates the environment into which this request will be
                deployed. Defaults to checking the environment for
                `SERMOS_ACCESS_KEY`. If not found, will exit.
    """
    access_key = access_key if access_key\
        else os.environ.get(ENV_VAR_ACCESS_KEY, None)
    if access_key is None:
        msg = "Unable to find `access-key` in CLI arguments nor in "\
            "environment under `{}`".format(ENV_VAR_ACCESS_KEY)
        logger.error(msg)
        raise ValueError(msg)
    return access_key


def get_client_pkg_name(pkg_name: str = None):
    """ Verify the package name provided and get from environment if None.

        Raise if neither provided nor found.

        Arguments:
          pkg_name (optional): Directory name for your Python
                    package. e.g. my_package_name . If none provided, will check
                    environment for `SERMOS_CLIENT_PKG_NAME`. If not found,
                    will exit.
    """
    pkg_name = pkg_name if pkg_name\
        else os.environ.get(ENV_VAR_PKG_NAME, None)
    if pkg_name is None:
        msg = "Unable to find `pkg-name` in CLI arguments nor in "\
            "environment under `{}`".format(ENV_VAR_PKG_NAME)
        logger.error(msg)
        raise ValueError(msg)
    return pkg_name
