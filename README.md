# PyCaprio
![Python versions](https://img.shields.io/badge/Python-3.6%2C%203.7%2C%203.8-green.svg) [![PyPI version](https://badge.fury.io/py/pycaprio.svg)](https://badge.fury.io/py/pycaprio) [![Documentation Status](https://readthedocs.org/projects/pycaprio/badge/?version=latest)](https://pycaprio.readthedocs.io/en/latest/?badge=latest) [![CircleCI](https://circleci.com/gh/Savanamed/pycaprio.svg?style=svg)](https://circleci.com/gh/Savanamed/pycaprio) [![codecov](https://codecov.io/gh/Savanamed/Pycaprio/branch/master/graph/badge.svg)](https://codecov.io/gh/Savanamed/Pycaprio)

Python client for the [INCEpTION](https://github.com/inception-project/inception) annotation tool.

## Installation
At the moment, this fork of `Pycaprio` is only available here, in Github (see reasons in "Current state of Pycaprio" below):
```
python -m pip install git+https://github.com/JavierLuna/pycaprio.git@0.2.1#egg=pycaprio
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

Check the [documentation](https://pycaprio.readthedocs.io) if you want to know more.

## Current state of Pycaprio
Hi! I'm Javier and I am the maintainer of `pycaprio`.
I developed this library when I was working at [Savanamed](https://github.com/Savanamed) where I pushed for it to be open sourced
so the research community could also use INCEpTION's API a bit easier.

While I don't work for the company anymore, I'd like to continue maintaining this project.
Pycaprio is MIT licensed, so I created this fork and continue my work, but the `pycaprio` PyPi package is still owned by Savana.

Now, I don't want to just create a "pycaprio2" and tell you to update, so I've asked Savanamed for an ownership transfer of that package.
That will mean you can use the project as always and I can keep on maintaining it. That's a fair deal!

However, as the spanish proverb says, "Las cosas de palacio van despacio"/"Things at the palace go slowly" so
expect a bit of delay on that ownership transfer. I'll keep you posted.

Thank you for using the project!

Javier

## License
Pycaprio is under the MIT license. Check it out [here](https://opensource.org/licenses/MIT)
