from typing import Union

from typing import List

from pycaprio.core.interfaces.schema import BaseInceptionSchema
from pycaprio.core.objects.project import Project

serialized_type = Union[List[dict], dict]
deserialized_type = Union[List[Project], Project]


class ProjectSchema(BaseInceptionSchema):
    """
    Schema to serialize/deserialize Projects.
    Documentation is described in 'BaseInceptionSchema'.
    """

    def load(self, project_dict: serialized_type, many: bool = False) -> deserialized_type:
        if many:
            return [self.load(project, many=False) for project in project_dict]
        return Project(project_dict['id'], project_dict['name'])

    def dump(self, project: deserialized_type, many: bool = False) -> serialized_type:
        if many:
            return [self.dump(p, many=False) for p in project]
        return {'id': project.project_id, 'name': project.project_name}
