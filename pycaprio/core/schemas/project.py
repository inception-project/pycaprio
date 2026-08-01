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
    def load(self, project_dict: List[dict], many: Literal[True]) -> List[Project]: ...

    @overload
    def load(self, project_dict: dict, many: Literal[False] = False) -> Project: ...

    def load(self, project_dict: serialized_type, many: bool = False) -> deserialized_type:
        if many:
            return [self.load(project) for project in cast(List[dict], project_dict)]
        project_dict = cast(dict, project_dict)
        return Project(project_dict["id"], project_dict["name"], project_dict["title"])

    @overload
    def dump(self, project: List[Project], many: Literal[True]) -> List[dict]: ...

    @overload
    def dump(self, project: Project, many: Literal[False] = False) -> dict: ...

    def dump(self, project: deserialized_type, many: bool = False) -> serialized_type:
        if many:
            return [self.dump(p) for p in cast(List[Project], project)]
        project = cast(Project, project)
        return {"id": project.project_id, "name": project.project_name, "title": project.project_title}
