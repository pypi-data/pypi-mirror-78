# wai-lazypip

Allows installation of additional packages at runtime (from within virtual environments).
Uses `pip` underneath the hood for installing the packages.


## Installation

You can install the library with pip as follows:

```
pip install wai.lazypip
```


## Functionality

The following methods are available from module `wai.lazypip`:

* `check_module` - checks whether the module is present and, if a list of packages has 
  been provided, installs these and performs check again.
* `require_module` - like `check_module`, but instead of returning a boolean, will
  raise an Exception in case the module is not present.
* `check_fun` and `require_fun` work in a similar fashion, but checking for a function
  within the module.
* `check_attr` and `require_attr` check for an attribute within the module.
* `check_class` and `require_class` check for a class to be present within the module.

The list of packages to install is in the same format as you would normally pass
on to the `pip` command-line too, e.g.:

```
["matplotlib"]
["matploblib<3.3.0"]
```

It is also possible to provide additional arguments to pip (which get inserted after
the `install` argument).


## Examples

* checking whether we are in a virtual environment

  ```python
  from wai.lazypip import is_venv
  if is_venv():
      print("yep, in a virtual environment")
  else:
      print("sorry, not a virtual environment")
  ```

* checking for the `matplotlib` module and installing matplotlib older than 3.3.0 if
  not yet present in the virtual environment 

  ```python
  from wai.lazypip import check_module
  m = "matplotlib"
  p = [m + "<3.3.0"]
  print(m, check_module(m, p))
  ```

* checking whether the `matplotlib` module has method `validate_backend` and installing 
  matplotlib older than 3.3.0 if not yet present in the virtual environment 

  ```python
  from wai.lazypip import check_fun
  m = "matplotlib"
  f = "validate_backend"
  p = [m + "<3.3.0"]
  print(m, f, check_fun(m, f, p))
  ```
  
* checking whether the `matplotlib` module has attribute `URL_REGEX` and installing 
  matplotlib older than 3.3.0 if not yet present in the virtual environment 

  ```python
  from wai.lazypip import check_attr
  m = "matplotlib"
  a = "URL_REGEX"
  p = [m + "<3.3.0"]
  print(m, a, check_attr(m, a, p))
  ```
  
* checking whether the `matplotlib` module has method `validate_backend` and installing 
  matplotlib older than 3.3.0 if not yet present in the virtual environment 

  ```python
  from wai.lazypip import check_class
  m = "matplotlib"
  c = "MutableMapping"
  p = [m + "<3.3.0"]
  print(m, c, check_class(m, c, p))
  ```
  