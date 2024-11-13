## The Project object

Pycaprio uses the `Project` object to model INCEpTION's projects, and has these properties:

* `project_id`: Id of the project (integer).
* `project_name`: Project name (string).
* `project_title`: Project title (string).

### List projects
Lists all the projects that are in INCEpTION.

Example:
```python
projects = client.api.projects()
print(projects) # [<Project #1: Project name>, <Project #2: Another project>]
```

### Fetch project
Fetches a project by its `id`.

You can provide a `Project` instance instead of an `int` as well.

Example:

```python
project = client.api.project(1) # Or updated_project = client.api.project(project)
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
Deletes a project by its `id`.

You can provide a `Project` instance instead of an `int` as well.

Example:

```python
client.api.delete_project(3)
client.api.delete_project(project)
```

### Export project
Exports a project into a zip. Pycaprio returns the zip's content in bytes to allow flexibility in use/storage.
You can specify the export file format using the `format` parameter. By default, it uses the `webanno` format.

You can provide a `Project` instance instead of an `int` as well.

Example:

```python
from pycaprio.mappings import InceptionFormat
content = client.api.export_project(project, project_format=InceptionFormat.XMI) # type(content) is bytes
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
