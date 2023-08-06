# Outline API

[![PyPI version](https://badge.fury.io/py/outline_api.svg)](https://badge.fury.io/py/outline_api)

Outline API package

## Install

use pip to install the package:
```
pip install outline_api
```


## Using package

import the package and cerate a management object.

```python
from outline_api import (
    Manager,
    get_key_numbers, 
    get_active_keys)


apiurl = "http://127.0.0.1/apikey"
apicrt = "apicert"
manager = Manager(apiurl=apiurl, apicrt=apicrt)

new_key = manager.new()
if new_key is not None:
    print(new_key)

keys = get_key_numbers("127.0.0.1", "999")
print(keys)

active_keys = get_active_keys("127.0.0.1", "999")
print(active_keys)
```
