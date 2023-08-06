# CMCC-DIAS-Client
DIAS API Client for access and analysis of CMCC data

## Requirements
Python 3.7

### Installation  
Conda Installation
```bash
$ conda install -c ppos-cmcc diasapi 
```

Pip installation
```bash
$ pip install diasapi
```
Cloning the repository
```bash
$ git clone https://github.com/CMCC-Foundation/cmcc-dias-client
$ cd cmcc-dias-client
$ python setup.py install
```

### Configuration
To use the tool a file `$HOME/.diasapirc` must be created as following

```bash
url: http://dias.cmcc.scc:8282/api/v1
key: <uid>:<api-key>
```

### Examples

For some examples how to use the tool see [here](examples/)

