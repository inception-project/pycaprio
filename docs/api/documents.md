## The Document object

Pycaprio uses the `Document` object to model INCEpTION's documents, and has the following properties:

* `project_id`: Id of the project in which the document is located (integer).
* `document_id`: Id of the document (integer).
* `document_name`: Name of the document (string).
* `document_state`: State in which the document is in (string, possible values in `pycaprio.core.mappings.DocumentStatus`).

### List documents
Lists all the documents in a project that are in INCEpTION.

Example:
```python
documents = client.api.documents(1) # In project #1
print(documents) # [<Document #4: Doc name (Project: 1)>, <Document #5: Doc name 2 (Project: 1)>]
```

### Download document
Downloads a document's content.
You can specify the annotation's format via `document_format` (defaults to `webanno`).

Example: 

```python
from pycaprio.mappings import InceptionFormat
document_content = client.api.document(1, 4, document_format=InceptionFormat.WEBANNO) # Downloads document 4 from project 1

with open("downloaded_document", 'wb') as document_file:
    document_file.write(document_content)
```

### Upload document
Uploads a document to a project in INCEpTION. It requires the Id of the project, the name of the document and the content of it (io stream).
You can specify the document's format via `document_format` (defaults to `webanno`).
You can specify the document's state via `document_state` (defaults to `NEW`).
 
Example:

```python
from pycaprio.mappings import InceptionFormat, DocumentState
with open("document", 'rb') as document_file:
    new_document = client.api.create_document(1, "Test document name", document_file, document_format=InceptionFormat.WEBANNO, document_state=DocumentState.IN_PROGRESS)
print(new_document) # <Document #5: Test document name (Project: 1)>
```

### Delete document
Deletes a document from a project.

Example:

```python
client.api.delete_document(1, 4) # Deletes document #4 from project #1
```
