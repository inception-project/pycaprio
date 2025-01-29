__any__ = ['Role']

import typing
from pycaprio.core.mappings import RoleType

class Role:
    """
    INCEpTION's Permissions object
    """

    def __init__(self, project_id: int, userId:str, roles:typing.List[RoleType]):
        self.project_id = project_id
        self.userId = userId
        self.roles = roles

    def __repr__(self):
        return f"<Role #ProjectId: {self.project_id}, UserId: {self.userId}, Roles: {self.roles}>"

    def __str__(self):
        return repr(self)
