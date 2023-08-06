# Paten

[![pytest](https://github.com/gsy0911/paten/workflows/pytest/badge.svg)](https://github.com/gsy0911/paten/actions?query=workflow%3Apytest)
[![codecov](https://codecov.io/gh/gsy0911/paten/branch/master/graph/badge.svg)](https://codecov.io/gh/gsy0911/paten)
[![PythonVersion](https://img.shields.io/badge/python-3.7|3.8-blue.svg)](https://www.python.org/downloads/release/python-377/)
[![PiPY](https://img.shields.io/badge/pypi-0.1.2-blue.svg)](https://pypi.org/project/paten/)


Paten is a framework for azure functions written in Python. Paten provides:

* A command line tool for creating, building, deploying azure functions.
* A decorator based API integrated with in/out bindings.

## install

install `paten` package.

```shell script
$ pip install paten
```

In addition, `Azure CLI` and `Azure Functions Core Tools` are required. 
See below to install the libraries.

* [Azure CLI](https://docs.microsoft.com/ja-jp/cli/azure/install-azure-cli?view=azure-cli-latest)
* [Azure Functions Core Tools](https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-run-local?tabs=macos%2Cpython%2Cbash)

## preparation

Before deploying to Azure, `az login` is required.

```shell script
$ az login

You have logged in. Now let us find all the subscriptions to which you have access...
```

## Quickstart

In your project directory, type below.
Directory {project_name} and example python scripts are created.

```shell script
$ paten new-app {project_name}
```

Then, modify `app.py`, like below.

```python
import azure.functions as func
from paten import Paten

app = Paten('{project_name}')


@app.http_trigger('req', methods=['GET'], route='/')
@app.out_http()
def example_http_function(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get('name')
    
    # response
    return func.HttpResponse(name)

```

Finally, to deploy to azure functions, type below in the directory `{project_name}`.
The files are generated in `./{project_name}/.paten` and your function app is deployed to azure.

```shell script
$ paten deploy
```

## support bindings

| services | trigger | in | out | 
|:--:|:--:|:--:|:--:|
| http | O | - | O |
| blob | O | X | X |
| queue | O | X | 0 |
| timer | O | - | - |
 
* O: supported
* X: not supported yet
* -: officially not supported