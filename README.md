# PyCaprio
![Python versions](https://img.shields.io/badge/Python-3.8%2C%203.9%2C%203.10%2C%203.11-green.svg)
[![PyPI version](https://badge.fury.io/py/pycaprio.svg)](https://badge.fury.io/py/pycaprio)
[![Documentation Status](https://readthedocs.org/projects/pycaprio/badge/?version=latest)](https://pycaprio.readthedocs.io/en/latest/?badge=latest)
[![Run Tests](https://github.com/inception-project/pycaprio/actions/workflows/run_tests.yml/badge.svg)](https://github.com/inception-project/pycaprio/actions/workflows/run_tests.yml)
[![codecov](https://codecov.io/gh/inception-project/pycaprio/graph/badge.svg?token=UUE49R7FEK)](https://codecov.io/gh/inception-project/pycaprio)

Python client for the [INCEpTION](https://github.com/inception-project/inception) annotation tool remote API.

## Installation
At the moment, this fork of `Pycaprio` is only available here, in GitHub (see reasons in "Current state of Pycaprio" below):
```
python -m pip install git+https://github.com/inception-project/pycaprio.git@0.2.1#egg=pycaprio
```

## Basic usage
The main object is the `Pycaprio` object, which will act as a client to interact with the API.
You will need your INCEpTION's host and an user with a [REMOTE role](https://inception-project.github.io//releases/0.11.0/docs/admin-guide.html#sect_remote_api).
Then, instantiate the Pycaprio client:
```python
from pycaprio import Pycaprio

pycaprio_client = Pycaprio("http://inception-host.com", ('username', 'password'))

# Create a project
pycaprio_client.api.create_project("Project name", "creator-username")
```

Check the [documentation](https://pycaprio.readthedocs.io) if you want to know more.

## Release

* Set the release version in `pyproject.toml` (e.g. `version = "0.3.1"`)
* Create a tag for the version e.g. `v0.3.1`
* Push the tag - this will trigger a GitHub action that requires approval
* Approve the action (or ask somebody who has the necessary permissions to approve)
* Wait until build is complete and release is on pypi
* Set the next dev version in `pyproject.toml` (e.g. `version = "0.4.0-dev"`)

## License
PyCaprio is under the MIT license. Check it out [here](https://opensource.org/licenses/MIT).

PyCaprio was originally developed by [Savanamed](https://github.com/Savanamed/pycaprio) and Javier Luna Molina.
It is now part of the INCEpTION project.
