## The Curation object

Pycaprio uses the `Curation` object to model INCEpTION's documents, and has the following properties:

* `project_id`: Id of the project in which the curated document is located (integer).
* `document_id`: Id of the curated document (integer).
* `document_state`: State in which the document is in (string, possible values in `pycaprio.core.mappings.DocumentStatus`).
* `timestamp`: Curation's creation date.

### List curated documents
Lists the curated documents in an INCEpTION project that have a document state specified with `document_state`.

You can provide a `Project` instance instead of a `project_id` as well.
You can provide a `Document` instance instead of a `document_id` as well.

Example:
```python
documents = client.api.curations(1,  document_state = DocumentState.CURATION_IN_PROGRESS) # Finished curations in project #1
print(documents) # [<Document #4: file.xmi (Project: 1)>]
```

### Download curated annotations
Downloads a curated document's annotation content.

You can specify the curation's format via `curation_format` (defaults to `webanno`).

You can provide a `Project` instance instead of a `project_id` as well.
You can provide a `Document` instance instead of a `document_id` as well.

Example:

```python
from pycaprio.mappings import InceptionFormat
# In case you want a specific curated document
curated annotation_content = client.api.curation(1, 4, curation_format=InceptionFormat.WEBANNO) # Downloads test-user's annotations from document 4 of project 1
with open("downloaded_annotation", 'wb') as annotation_file:
    annotation_file.write(annotation_content)

```
or for many files...

WEBANNO example:
```python
# To download all curated documents, in case not all document have been curated (will cause error), you need to select the ones that have a document_state associated with curation:
from pycaprio.core.mappings import InceptionFormat, DocumentState
documents = client.api.documents(1)
for document in documents:
    if document.document_state == DocumentState.CURATION_IN_PROGRESS:
        curated content = client.api.curation(1, document, curation_format=InceptionFormat.WEBANNO)
        with open(document.document_name, 'wb') as annotation_file:
            annotation_file.write(curated_content)
```


XMI example:
```python
# To download all curated documents, in case not all document have been curated (will cause error), you need to select the ones that have a document_state associated with curation:
from pycaprio.core.mappings import InceptionFormat, DocumentState
curations = []
documents = client.api.documents(1)
for document in documents:
    if document.document_state == DocumentState.CURATION_IN_PROGRESS:
        curated content = client.api.curation(1, document, curation_format=InceptionFormat.XMI)
        curations.append(curated content)
        for curation in curations:
            z = zipfile.ZipFile(io.BytesIO(curation))
            z.extractall('/your/path/')
```


### Upload curation
Uploads a curated document in INCEpTION. It requires the Id of the project, the Id of the document, the annotator's username and the annotation's content (io stream).

You can specify the curation's format via `curation_format` (defaults to `webanno`) and its state via `annotation_state` (defaults to `NEW`).

You can specify the document's state via `document_state`.
You can provide a `Project` instance instead of a `project_id` as well.
You can provide a `Document` instance instead of a `document_id` as well.

You need to specify `content` which depends on the annotation format specified in the download:

To curate a document outside of INCEpTION or to simply change the status of a document into a curator status, you could do the following:

 ```python
from pycaprio.mappings import InceptionFormat
# Get the annotations or a specific document as e.g. binary CAS
file = client.api.annotation(1, 4, 'test-user', curation_format=InceptionFormat.BIN)
# The below function then uploads the file with the new status
client.api.create_curation(1, 4, curation_format = InceptionFormat.BIN, content =  annotations, document_state = DocumentState.CURATION_IN_PROGRESS)
```

XMI format also works, but one has to unzip the file first and import only the plain XMI file
 ```python
from pycaprio.mappings import InceptionFormat
annotation_content = client.api.annotation(1, 4, 'test-user', curation_format=InceptionFormat.XMI)
z = zipfile.ZipFile(io.BytesIO(annotations))
z.extractall('/path/to/folder')
with open('/path/to/folder/file.xmi', 'rb') as f:
    file = f.read()
# The below function then uploads the file with the new status
client.api.create_curation(1, 4, curation_format = InceptionFormat.XMI, content =  file, document_state = DocumentState.CURATION_IN_PROGRESS)
```

### Delete curations
Deletes curated annotations from a document and puts it back to 'ANNOTATION-IN-PROGRESS'.

You can provide a `Project` instance instead of a `project_id` as well.
You can provide a `Document` instance instead of a `document_id` as well.


Example:

```python
client.api.delete_curation(1,4) # Deletes curated document #4 from project #1
```

