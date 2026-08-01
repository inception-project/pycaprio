from typing import List
from typing import Literal
from typing import Union
from typing import cast
from typing import overload

from pycaprio.core.interfaces.schema import BaseInceptionSchema
from pycaprio.core.interfaces.schema import serialized_type
from pycaprio.core.mappings import NO_PROJECT
from pycaprio.core.objects.document import Document

deserialized_type = Union[List[Document], Document]


class DocumentSchema(BaseInceptionSchema[Document]):
    """
    Schema to serialize/deserialize Documents.
    Documentation is described in 'BaseInceptionSchema'.
    """

    @overload
    def load(self, serialized_object_or_list: List[dict], many: Literal[True]) -> List[Document]: ...

    @overload
    def load(self, serialized_object_or_list: dict, many: Literal[False] = False) -> Document: ...

    def load(self, serialized_object_or_list: serialized_type, many: bool = False) -> deserialized_type:
        if many:
            return [self.load(d) for d in cast(List[dict], serialized_object_or_list)]
        serialized_document = cast(dict, serialized_object_or_list)
        return Document(
            NO_PROJECT, serialized_document["id"], serialized_document["name"], serialized_document["state"]
        )

    @overload
    def dump(self, deserialized_object_or_list: List[Document], many: Literal[True]) -> List[dict]: ...

    @overload
    def dump(self, deserialized_object_or_list: Document, many: Literal[False] = False) -> dict: ...

    def dump(self, deserialized_object_or_list: deserialized_type, many: bool = False) -> serialized_type:
        if many:
            return [self.dump(d) for d in cast(List[Document], deserialized_object_or_list)]
        document = cast(Document, deserialized_object_or_list)
        return {"id": document.document_id, "name": document.document_name, "state": document.document_state}
