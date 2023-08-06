pyDinemic
=========

The Python wrapper for libdinemic framework. This project is still under
development.


Compilation and Installation
----------------------------
Install following packages:
* libboost-python-dev
* redis-server
* gcc
* g++
* python3-dev

Download latest version of libdinemic from https://packages.dinemic.io/ and
install it.

To compile pydinemic call in this repository:
```
python3 setup.py build
```
To install module:
```
python3 setup.py install
```

In case of linking errors related to libboost_python, check the setup.py file
and update libraries to boost_python-py35 or boost_python3.

Using pydinemic
---------------
Example use of DModel:
```
import pydinemic

pydinemic.launch()

m = pyDinemic.DModel("MySimpleModel", [])
m.set("field", "value")
```

and use of DAction:

```
def my_listener(object_id, key, old_value, new_value):
    print("Changed value to " + new_value)

action = pydinemic.DAction()
action.set_on_authorized_update_callback(my_listener)
action.apply("MyModel:*:")
```
