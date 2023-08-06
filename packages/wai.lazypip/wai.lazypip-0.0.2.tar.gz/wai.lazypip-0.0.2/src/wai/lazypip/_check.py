from importlib import import_module
from inspect import getmembers, isclass
import logging
import pip
import traceback
from ._venv import is_venv


def backup_root_logger():
    """
    Creates a backup of the root logger.

    :return: the backup
    :rtype: dict
    """
    result = dict()
    result['level'] = logging.root.level
    result['disabled'] = logging.root.disabled
    result['handlers'] = logging.root.handlers[:]
    return result


def restore_root_logger(backup):
    """
    Restores the root logger from the backup.

    :param backup: the backup (level/disable/handlers)
    :type backup: dict
    """

    logging.root.level = backup['level']
    logging.root.disabled = backup['disabled']
    logging.root.handlers = backup['handlers']


def install_packages(packages, pip_args=None):
    """
    Installs the required packages.

    :param packages: the pip packages list
    :type packages: list
    :param pip_args: additional arguments to pip
    :type pip_args: list
    """

    # calling pip.main changes the root logger setup
    backup = backup_root_logger()

    print("installing", packages)
    try:
        args = ["install"]
        if not pip_args is None:
            args.extend(pip_args)
        args.extend(packages)
        pip.main(args)
    except:
        print("Failed to install: %s" % ",".join(packages))
        print(traceback.format_exc())

    # restore original settings of root logger
    restore_root_logger(backup)


def check_module(module_name, packages=None, pip_args=None):
    """
    Checks whether a module is present and (tries to) install if packages have been provided.

    :param module_name: the module to check
    :type module_name: str
    :param packages: the list packages to install, no installation occurs if None
    :type packages: list
    :param pip_args: additional arguments to pip
    :type pip_args: list
    :return: whether the module is present (if packages listed, then if present after installation of these)
    :rtype: bool
    """

    try:
        import_module(module_name)
        return True
    except:
        if packages is not None and is_venv():
            install_packages(packages, pip_args=pip_args)
            return check_module(module_name)
        else:
            return False


def require_module(module_name, packages=None, pip_args=None):
    """
    Requires a module to be present, (tries to) install if packages have been provided, fails with an exception if
    not present.

    :param module_name: the module to check
    :type module_name: str
    :param packages: the list packages to install, no installation occurs if None
    :type packages: list
    :param pip_args: additional arguments to pip
    :type pip_args: list
    """

    if not check_module(module_name, packages=packages, pip_args=pip_args):
        raise Exception("Module %s is not present!" % module_name)


def check_fun(module_name, fun_name, packages=None, pip_args=None):
    """
    Checks whether a function is present in the specified module and (tries to) install if packages have been provided.

    :param module_name: the module to check
    :type module_name: str
    :param fun_name: the name of the function to check
    :type fun_name: str
    :param packages: the list packages to install, no installation occurs if None
    :type packages: list
    :param pip_args: additional arguments to pip
    :type pip_args: list
    :return: whether the module is present (if packages listed, then if present after installation of these)
    :rtype: bool
    """

    try:
        l = import_module(module_name)
        if hasattr(l, fun_name) and callable(getattr(l, fun_name)):
            return True
        else:
            return False
    except:
        if packages is not None and is_venv():
            install_packages(packages, pip_args=pip_args)
            return check_fun(module_name, fun_name)
        else:
            return False


def require_fun(module_name, fun_name, packages=None, pip_args=None):
    """
    Requires a function in a module to be present, (tries to) install if packages have been provided, fails with an
    exception if not present.

    :param module_name: the module to check
    :type module_name: str
    :param fun_name: the name of the function to check
    :type fun_name: str
    :param packages: the list packages to install, no installation occurs if None
    :type packages: list
    :param pip_args: additional arguments to pip
    :type pip_args: list
    :return: whether the module is present (if packages listed, then if present after installation of these)
    :rtype: bool
    """

    if not check_fun(module_name, fun_name, packages=packages, pip_args=pip_args):
        raise Exception("Module %s and/or function %s are not available!" % (module_name, fun_name))


def check_attr(module_name, attr_name, packages=None, pip_args=None):
    """
    Checks whether an attribute is present in the specified module and (tries to) install if packages have been provided.

    :param module_name: the module to check
    :type module_name: str
    :param attr_name: the name of the attribute to check
    :type attr_name: str
    :param packages: the list packages to install, no installation occurs if None
    :type packages: list
    :param pip_args: additional arguments to pip
    :type pip_args: list
    :return: whether the module is present (if packages listed, then if present after installation of these)
    :rtype: bool
    """

    try:
        l = import_module(module_name)
        if hasattr(l, attr_name):
            return True
        else:
            return False
    except:
        if packages is not None and is_venv():
            install_packages(packages, pip_args=pip_args)
            return check_attr(module_name, attr_name)
        else:
            return False


def require_attr(module_name, attr_name, packages=None, pip_args=None):
    """
    Requires an attribute in a module to be present, (tries to) install if packages have been provided, fails with an
    exception if not present.

    :param module_name: the module to check
    :type module_name: str
    :param attr_name: the name of the attribute to check
    :type attr_name: str
    :param packages: the list packages to install, no installation occurs if None
    :type packages: list
    :param pip_args: additional arguments to pip
    :type pip_args: list
    :return: whether the module is present (if packages listed, then if present after installation of these)
    :rtype: bool
    """

    if not check_attr(module_name, attr_name, packages=packages, pip_args=pip_args):
        raise Exception("Module %s and/or attribute %s are not available!" % (module_name, attr_name))


def check_class(module_name, class_name, packages=None, pip_args=None):
    """
    Checks whether a class is present in the specified module and (tries to) install if packages have been provided.

    :param module_name: the module to check
    :type module_name: str
    :param class_name: the name of the class to check
    :type class_name: str
    :param packages: the list packages to install, no installation occurs if None
    :type packages: list
    :param pip_args: additional arguments to pip
    :type pip_args: list
    :return: whether the module is present (if packages listed, then if present after installation of these)
    :rtype: bool
    """

    try:
        l = import_module(module_name)
        classes = tuple(x[1].__name__ for x in getmembers(l, isclass))
        if class_name in classes:
            return True
        else:
            return False
    except:
        if packages is not None and is_venv():
            install_packages(packages, pip_args=pip_args)
            return check_class(module_name, class_name)
        else:
            return False


def require_class(module_name, class_name, packages=None, pip_args=None):
    """
    Requires a class in a module to be present, (tries to) install if packages have been provided, fails with an
    exception if not present.

    :param module_name: the module to check
    :type module_name: str
    :param class_name: the name of the class to check
    :type class_name: str
    :param packages: the list packages to install, no installation occurs if None
    :type packages: list
    :param pip_args: additional arguments to pip
    :type pip_args: list
    :return: whether the module is present (if packages listed, then if present after installation of these)
    :rtype: bool
    """

    if not check_class(module_name, class_name, packages=packages, pip_args=pip_args):
        raise Exception("Module %s and/or class %s are not available!" % (module_name, class_name))
