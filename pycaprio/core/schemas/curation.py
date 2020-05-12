import datetime
from typing import Union
from typing import List
from pycaprio.core.mappings import DATE_FORMAT_ISO8601
from pycaprio.core.interfaces.schema import BaseInceptionSchema
from pycaprio.core.mappings import NO_PROJECT
from pycaprio.core.mappings import NO_DOCUMENT
from pycaprio.core.objects.curation import Curation

serialized_type = Union[List[dict], dict]
deserialized_type = Union[List[Curation], Curation]


class CurationSchema(BaseInceptionSchema):
    """
    Schema to serialize/deserialize curated document.
    Documentation is described in 'BaseInceptionSchema'.
    """

    def load(self, serialized_curation: serialized_type, many: bool = False):
        if many:
            return [self.load(curation) for curation in serialized_curation]

        datetime_timestamp = None
        if serialized_curation['timestamp']:
            datetime_timestamp = datetime.datetime.strptime(serialized_curation['timestamp'], DATE_FORMAT_ISO8601)

        return Curation(NO_PROJECT, NO_DOCUMENT, serialized_curation['user'], serialized_curation['state'],
                        datetime_timestamp)

    def dump(self, curation: deserialized_type, many: bool = False):
        if many:
            return [self.dump(a) for a in curation]
        str_timestamp = None
        if curation.timestamp:
            str_timestamp = curation.timestamp.strftime(DATE_FORMAT_ISO8601)
        return {'user': curation.user_name, 'state': curation.document_state, 'timestamp': str_timestamp}
