# li-memcached-client

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/liniribeiro/li-memcached-client/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/liniribeiro/li-memcached-client/tree/main)

li-memcached-client is a Python library for connecting into memcached, list, add, get and delete keys.

## Installation
To install the li-memcached-client package, use the following command:

```
pip3 install li-memcached-client
```

## Usage 
```
from li_memcached_client import LiMemcachedClient
client = LiMemcachedClient()
```
By default, it connects to localhost on port 11211. If you need to specify a host and/or port:

```
client = LiMemcachedClient(host='1.2.3.4', port='11211')
```

## Local Development
For local development, follow these steps:

1. Build the project:
```
poetry build
```
2. Install the project:
```
poetry install
```
3. Install twine for publishing:
```
python3 -m pip install --upgrade twine
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.  

## Contact
For any questions or issues, please contact Alini Ribeiro at aliniribeiroo@gmail.com. 


This documentation provides an overview of the li-memcached-stats library, including installation, configuration, usage, and development instructions.