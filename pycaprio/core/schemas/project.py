from typing import List
from typing import Literal
from typing import Union
from typing import cast
from typing import overload

from pycaprio.core.interfaces.schema import BaseInceptionSchema
from pycaprio.core.interfaces.schema import serialized_type
from pycaprio.core.objects.project import Project

deserialized_type = Union[List[Project], Project]


class ProjectSchema(BaseInceptionSchema[Project]):
    """
    Schema to serialize/deserialize Projects.
    Documentation is described in 'BaseInceptionSchema'.
    """

    @overload
    def load(self, serialized_object_or_list: List[dict], many: Literal[True]) -> List[Project]: ...

    @overload
    def load(self, serialized_object_or_list: dict, many: Literal[False] = False) -> Project: ...

    def load(self, serialized_object_or_list: serialized_type, many: bool = False) -> deserialized_type:
        if many:
            return [self.load(p) for p in cast(List[dict], serialized_object_or_list)]
        project_dict = cast(dict, serialized_object_or_list)
        return Project(project_dict["id"], project_dict["name"], project_dict["title"])

    @overload
    def dump(self, deserialized_object_or_list: List[Project], many: Literal[True]) -> List[dict]: ...

    @overload
    def dump(self, deserialized_object_or_list: Project, many: Literal[False] = False) -> dict: ...

    def dump(self, deserialized_object_or_list: deserialized_type, many: bool = False) -> serialized_type:
        if many:
            return [self.dump(p) for p in cast(List[Project], deserialized_object_or_list)]
        project = cast(Project, deserialized_object_or_list)
        return {"id": project.project_id, "name": project.project_name, "title": project.project_title}
