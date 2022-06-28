# IPFabric

ipfabric-diagrams is a Python module for connecting to and graphing topologies against an IP Fabric instance.

[![Requirements Status](https://requires.io/github/community-fabric/python-ipfabric-diagrams/requirements.svg?branch=develop)](https://requires.io/github/community-fabric/python-ipfabric-diagrams/requirements/?branch=develop)

## About

Founded in 2015, [IP Fabric](https://ipfabric.io/) develops network infrastructure visibility and analytics solution to
help enterprise network and security teams with network assurance and automation across multi-domain heterogeneous
environments. From in-depth discovery, through graph visualization, to packet walks and complete network history, IP
Fabric enables to confidently replace manual tasks necessary to handle growing network complexity driven by relentless
digital transformation.

## Versioning
Starting with IP Fabric version 5.0.x the python-ipfabric and python-ipfabric-diagrams will need to
match your IP Fabric version.  The API's are changing and instead of `api/v1` they will now be `api/v5.0`.

Version 5.1 will have backwards compatability with version 5.0 however 6.0 will not support any 5.x versions.
By ensuring that your ipfabric SDK's match your IP Fabric Major Version will ensure compatibility and will continue to work.


## Installation

```
pip install ipfabric-diagrams
```

## Introduction

This package is used for diagramming via the API for IP Fabric v4.3.0.  
Examples can be located under [examples](examples/) directory.

## Authentication
Please take a look at [python-ipfabric](https://github.com/community-fabric/python-ipfabric#authentication) 
for all authentication options.

```python
from ipfabric_diagrams import IPFDiagram
ipf = IPFDiagram(base_url='https://demo3.ipfabric.io/', token='token', verify=False, timeout=15)
```

## Development

IPFabric uses poetry for the python packaging module. Install poetry globally:

```
pip install poetry
```

To install a virtual environment run the following command in the root of this directory.

```
poetry install
```

To test and build:

```
poetry run pytest
poetry build
```

Prior to pushing changes run:
```
poetry run black ipfabric_diagrams
poetry export -f requirements.txt -o requirements.txt --without-hashes
git add requirements.txt
```