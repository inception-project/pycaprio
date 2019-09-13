# Pycaprio

Python client for the [INCEpTION](https://github.com/inception-project/inception) annotation tool.

At the moment, it serves as an API wrapper, supporting the AERO format INCEpTION serves.

## Installation
Pycaprio is hosted in [PyPi](https://pypi.org/project/pycaprio/) and can be installed via `pip`:
```
pip install pycaprio
```

## Basic usage
First, you must instantiate a `pycaprio` client:
```python
from pycaprio import Pycaprio
client = Pycaprio("http://your-inception-host.com", authentication=("remote-user", "password"))

# List projects
projects = client.api.projects()

# Export all projects in XMI format
from pycaprio.mappings import InceptionFormat
for project in projects:
    zip_content = client.api.export_project(project.project_id, format=InceptionFormat.XMI)
    with open(f"{project.project_name}.zip", 'wb') as zip_file:
        zip_file.write(zip_content)
```
