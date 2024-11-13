class Project:
    """
    INCEpTION's Project object
    """

    def __init__(self, project_id: int, project_name: str, project_title: str):
        self.project_id = project_id
        self.project_name = project_name
        self.project_title = project_title

    def __eq__(self, other):
        return isinstance(other, Project) and \
               other.project_id == self.project_id and \
               other.project_name == self.project_name

    def __repr__(self):
        return f"<Project #{self.project_id}: {self.project_name}>"

    def __str__(self):
        return repr(self)
