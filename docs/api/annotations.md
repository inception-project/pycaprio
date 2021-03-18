## The Annotation object

Pycaprio uses the `Annotation` object to model INCEpTION's documents, and has the following properties:

* `project_id`: Id of the project in which the annotated document is located (integer).
* `document_id`: Id of the annotated document (integer).
* `user_name`: Annotator's username (string).
* `annotation_state`: State in which the annotation is in (string, possible values in `pycaprio.core.mappings.AnnotationStatus`).
* `timestamp`: Annotation's creation date.


### List annotations
Lists all the annotations in an INCEpTION's document.

You can provide a `Project` instance instead of a `project_id` as well.
You can provide a `Document` instance instead of a `document_id` as well.

Example:
```python
annotations = client.api.annotations(1, 4) # Annotations in document #4 in project #1
print(annotations) # [<Annotation by test-user (Project: 1, Document: 4)>, <Annotation by leonardo-dicaprio (Project: 1, Document: 4)>]
```

### Download annotation
Downloads a document's annotation content.

You can specify the annotation's format via `annotation_format` (defaults to `webanno`).

You can provide a `Project` instance instead of a `project_id` as well.
You can provide a `Document` instance instead of a `document_id` as well.

Example:

```python
from pycaprio.mappings import InceptionFormat
annotation_content = client.api.annotation(1, 4, 'test-user', annotation_format=InceptionFormat.WEBANNO) # Downloads test-user's annotations on document 4 on project 1

with open("downloaded_annotation", 'wb') as annotation_file:
    annotation_file.write(annotation_content)
```

### Upload annotation
Uploads an annotation to a document in INCEpTION. It requires the Id of the project, the Id of the document, the annotator's username and the annotation's content (io stream).

You can specify the annotation's format via `annotation_format` (defaults to `webanno`) and its state via `annotation_state` (defaults to `NEW`).

You can provide a `Project` instance instead of a `project_id` as well.
You can provide a `Document` instance instead of a `document_id` as well.


Example:

```python
from pycaprio.mappings import InceptionFormat, AnnotationState
with open("annotation", 'rb') as annotation_file:
    new_annotation = client.api.create_annotation(1, 4, 'leonardo-dicaprio', annotation_file, annotation_format=InceptionFormat.WEBANNO, annotation_state=AnnotationState.IN_PROGRESS)
print(new_annotation) # <Annotation by leonardo-dicaprio (Project: 1, Document: 4)>
```

### Delete annotation
Deletes an annotation from a project.

You can provide a `Project` instance instead of a `project_id` as well.
You can provide a `Document` instance instead of a `document_id` as well.


Example:

```python
client.api.delete_annotation(1, 4, 'leonardo-dicaprio') # Deletes annotation made by leonardo-dicaprio on document #4 from project #1
```

### Update annotation state
Updates the state of an annotation. Requires INCEpTION 0.19.0+.

**Note**: This endpoint is not AERO compliant, meaning this could not work in other AERO-compatible annotation tools.

You can provide a `Project` instance instead of a `project_id` as well.
You can provide a `Document` instance instead of a `document_id` as well.


Example:

```python
from pycaprio.mappings import AnnotationState
client.api.update_annotation_state(1, 4, 'leonardo-dicaprio', AnnotationState.LOCKED) # Updates the state to 'LOCKED'
```
