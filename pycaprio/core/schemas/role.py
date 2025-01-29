from typing import Union
from typing import List
from pycaprio.core.interfaces.schema import BaseInceptionSchema
from pycaprio.core.objects.role import Role

serialized_type = Union[List[dict], dict]
deserialized_type = Union[List[Role], Role]


class RoleSchema(BaseInceptionSchema):
    """
    Schema to serialize/deserialize Roles.
    Documentation is described in 'BaseInceptionSchema'.
    """

    def load(self, roles_dict: serialized_type, many: bool = False) -> deserialized_type:
        if many:
            return [self.load(project, many=False) for project in roles_dict]
        return Role(project_id=roles_dict['project'], userId=roles_dict['user'], roles=roles_dict['role'])

    def dump(self, roles: deserialized_type, many: bool = False) -> serialized_type:
        if many:
            return [self.dump(p, many=False) for p in roles]
        return {'projectId': roles.project_id, 'user': roles.userId, 'role':roles.roles}
