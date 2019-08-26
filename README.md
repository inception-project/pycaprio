# PyCaprio
![Python versions](https://img.shields.io/badge/Python-3.6%2C%203.7-green.svg) ![PyPi](https://img.shields.io/badge/PyPi-0.0.1-brightgreen.svg) [![CircleCI](https://circleci.com/gh/Savanamed/pycaprio.svg?style=svg)](https://circleci.com/gh/Savanamed/pycaprio) [![codecov](https://codecov.io/gh/Savanamed/Pycaprio/branch/master/graph/badge.svg)](https://codecov.io/gh/Savanamed/Pycaprio)

Python client to the [INCEpTION](https://github.com/inception-project/inception) annotation tool.

## Installation
Pycaprio is on PyPi, you can install it via `pip`, `pipenv`, `poetry` or your favourite dependency management tool:
```
pip install pycaprio
```

## Basic usage
The main object is the `Pycaprio` object, which will act as a client to interact with the API.
You will need your INCEpTION's host and an user with a
 [REMOTE role](https://inception-project.github.io//releases/0.11.0/docs/admin-guide.html#sect_remote_api).
Then, instanciate the Pycaprio client:
```python

from pycaprio import Pycaprio

pycaprio_client = Pycaprio("http://inception-host.com", ('username', 'password'))

# Create a project
pycaprio_client.api.create_project("Project name", "creator-username")
```

And so on.
Although Pycaprio's API is simple and usable, proper documentation will roll in a few days.

## License
Pycaprio is under the MIT license. Check it out [here](https://opensource.org/licenses/MIT)
