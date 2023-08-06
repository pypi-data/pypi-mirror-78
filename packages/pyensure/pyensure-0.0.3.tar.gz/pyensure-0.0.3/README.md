# pyensure
An odd solution to auto-download missing imports.

This is more of a proof-of-concept than a good idea.

## Installation
```
pip install pyensure
```

## Usage

```
from pyensure import hook, ensure_package

pytest = ensure_package('pytest') # will install pytest via pip to a temp location of missing

# or if you want to do something a bit more scary

hook()

import requests # will install requests via pip to a temp location of missing

# Note that hook() will actually overwrite the base __import__() method to ensure the package exists

# or if you just want to run a .py script and not worry  (as much) about depends
python -m pyensure <script> <args to script... >
```


## License
MIT License - Charles Machalow
