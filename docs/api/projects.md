## The Project object

Pycaprio uses the `Project` object to model INCEpTION's projects, and has these properties:

* `project_id`: Id of the project (integer).
* `project_name`: Project name (string).


### List projects
Lists all the projects that are in INCEpTION.

Example:
```python
projects = client.api.projects()
print(projects) # [<Project #1: Project name>, <Project #2: Another project>]
```

### Fetch project
Fetches a project by its `project_id`.

Example: 

```python
project = client.api.project(1)
print(project) # <Project #1: Project name>
```

### Create project
Creates a project in INCEpTION. It requires the project's name and optionally the creator's username.
If no `creator_name` is provided, pycaprio will use the one of the user that is currently logged in to the API.

Example:

```python
new_project = client.api.create_project("New project name", creator_name="other user")
print(new_project) # <Project #3: New project name>
```

### Delete project
Deletes a project.

Example:

```python
client.api.delete_project(3)
```

### Export project
Exports a project into a zip. Pycaprio returns the zip's content in bytes to allow flexibility in use/storage.
You can specify the export file format using the `format` parameter. By default, it uses the `webanno` format. 

Example:

```python
from pycaprio.mappings import InceptionFormat
content = client.api.export_project(1, project_format=InceptionFormat.XMI) # type(content) is bytes
with open("exported_project.zip", 'wb') as zip_file:
    zip_file.write(content)
```

### Import project
Imports a project given a zip file's content.

Example:

```python
with open("exported_project.zip", 'rb') as zip_file:
    project = client.api.import_project(zip_file)
print(project) # <Project #1: Project name>
```
