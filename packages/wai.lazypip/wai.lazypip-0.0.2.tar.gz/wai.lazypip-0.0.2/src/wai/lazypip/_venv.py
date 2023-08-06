# taken from here:
# https://stackoverflow.com/a/42580137/4698227

import sys


def is_venv():
    """
    Checks whether we are in a virtual environment or not.

    :return: whether within a virtual environment
    :rtype: bool
    """

    return (hasattr(sys, 'real_prefix')
            or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))
