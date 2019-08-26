import datetime
from typing import Union

from typing import List

from pycaprio.core.interfaces.schema import BaseInceptionSchema
from pycaprio.core.mappings import DATE_FORMAT_ISO8601
from pycaprio.core.mappings import NO_DOCUMENT
from pycaprio.core.mappings import NO_PROJECT
from pycaprio.core.objects.annotation import Annotation

serialized_type = Union[List[dict], dict]
deserialized_type = Union[List[Annotation], Annotation]


class AnnotationSchema(BaseInceptionSchema):
    """
    Schema to serialize/deserialize Annotations.
    Documentation is described in 'BaseInceptionSchema'.
    """

    def load(self, serialized_annotation: serialized_type, many: bool = False):
        if many:
            return [self.load(annotation) for annotation in serialized_annotation]

        datetime_timestamp = datetime.datetime.strptime(serialized_annotation['timestamp'], DATE_FORMAT_ISO8601)

        return Annotation(NO_PROJECT, NO_DOCUMENT, serialized_annotation['user'], serialized_annotation['state'],
                          datetime_timestamp)

    def dump(self, annotation: deserialized_type, many: bool = False):
        if many:
            return [self.dump(a) for a in annotation]
        str_timestamp = annotation.timestamp.strftime(DATE_FORMAT_ISO8601)
        return {'user': annotation.user_name, 'state': annotation.annotation_state, 'timestamp': str_timestamp}
