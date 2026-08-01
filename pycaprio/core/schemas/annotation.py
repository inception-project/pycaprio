import datetime
from typing import List
from typing import Literal
from typing import Union
from typing import cast
from typing import overload

from pycaprio.core.interfaces.schema import BaseInceptionSchema
from pycaprio.core.interfaces.schema import serialized_type
from pycaprio.core.mappings import DATE_FORMAT_ISO8601
from pycaprio.core.mappings import NO_DOCUMENT
from pycaprio.core.mappings import NO_PROJECT
from pycaprio.core.objects.annotation import Annotation

deserialized_type = Union[List[Annotation], Annotation]


class AnnotationSchema(BaseInceptionSchema[Annotation]):
    """
    Schema to serialize/deserialize Annotations.
    Documentation is described in 'BaseInceptionSchema'.
    """

    @overload
    def load(self, serialized_object_or_list: List[dict], many: Literal[True]) -> List[Annotation]: ...

    @overload
    def load(self, serialized_object_or_list: dict, many: Literal[False] = False) -> Annotation: ...

    def load(self, serialized_object_or_list: serialized_type, many: bool = False) -> deserialized_type:
        if many:
            return [self.load(annotation) for annotation in cast(List[dict], serialized_object_or_list)]

        serialized_annotation = cast(dict, serialized_object_or_list)
        datetime_timestamp = None
        if serialized_annotation["timestamp"]:
            datetime_timestamp = datetime.datetime.strptime(serialized_annotation["timestamp"], DATE_FORMAT_ISO8601)

        return Annotation(
            NO_PROJECT, NO_DOCUMENT, serialized_annotation["user"], serialized_annotation["state"], datetime_timestamp
        )

    @overload
    def dump(self, deserialized_object_or_list: List[Annotation], many: Literal[True]) -> List[dict]: ...

    @overload
    def dump(self, deserialized_object_or_list: Annotation, many: Literal[False] = False) -> dict: ...

    def dump(self, deserialized_object_or_list: deserialized_type, many: bool = False) -> serialized_type:
        if many:
            return [self.dump(a) for a in cast(List[Annotation], deserialized_object_or_list)]
        annotation = cast(Annotation, deserialized_object_or_list)
        str_timestamp = None
        if annotation.timestamp:
            str_timestamp = annotation.timestamp.strftime(DATE_FORMAT_ISO8601)
        return {"user": annotation.user_name, "state": annotation.annotation_state, "timestamp": str_timestamp}
