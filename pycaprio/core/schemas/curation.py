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
from pycaprio.core.objects.curation import Curation

deserialized_type = Union[List[Curation], Curation]


class CurationSchema(BaseInceptionSchema[Curation]):
    """
    Schema to serialize/deserialize curated document.
    Documentation is described in 'BaseInceptionSchema'.
    """

    @overload
    def load(self, serialized_object_or_list: List[dict], many: Literal[True]) -> List[Curation]: ...

    @overload
    def load(self, serialized_object_or_list: dict, many: Literal[False] = False) -> Curation: ...

    def load(self, serialized_object_or_list: serialized_type, many: bool = False) -> deserialized_type:
        if many:
            return [self.load(curation) for curation in cast(List[dict], serialized_object_or_list)]

        serialized_curation = cast(dict, serialized_object_or_list)
        datetime_timestamp = None
        if serialized_curation["timestamp"]:
            datetime_timestamp = datetime.datetime.strptime(serialized_curation["timestamp"], DATE_FORMAT_ISO8601)

        return Curation(
            NO_PROJECT, NO_DOCUMENT, serialized_curation["user"], serialized_curation["state"], datetime_timestamp
        )

    @overload
    def dump(self, deserialized_object_or_list: List[Curation], many: Literal[True]) -> List[dict]: ...

    @overload
    def dump(self, deserialized_object_or_list: Curation, many: Literal[False] = False) -> dict: ...

    def dump(self, deserialized_object_or_list: deserialized_type, many: bool = False) -> serialized_type:
        if many:
            return [self.dump(a) for a in cast(List[Curation], deserialized_object_or_list)]
        curation = cast(Curation, deserialized_object_or_list)
        str_timestamp = None
        if curation.timestamp:
            str_timestamp = curation.timestamp.strftime(DATE_FORMAT_ISO8601)
        return {"user": curation.user_name, "state": curation.document_state, "timestamp": str_timestamp}
