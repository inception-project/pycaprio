from typing import Union

from typing import List

from pycaprio.core.interfaces.schema import BaseInceptionSchema
from pycaprio.core.mappings import NO_PROJECT
from pycaprio.core.objects.document import Document

serialized_type = Union[List[dict], dict]
deserialized_type = Union[List[Document], Document]


class DocumentSchema(BaseInceptionSchema):
    """
    Schema to serialize/deserialize Documents.
    Documentation is described in 'BaseInceptionSchema'.
    """

    def load(self, serialized_document, many: bool = False):
        if many:
            return [self.load(d) for d in serialized_document]
        return Document(
            NO_PROJECT, serialized_document["id"], serialized_document["name"], serialized_document["state"]
        )

    def dump(self, document, many: bool = False):
        if many:
            return [self.dump(d) for d in document]
        return {"id": document.document_id, "name": document.document_name, "state": document.document_state}
