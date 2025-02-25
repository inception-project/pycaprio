import datetime


class Annotation:
    """
    INCEpTION's Annotation object
    """

    def __init__(
        self, project_id: int, document_id: int, user_name: str, annotation_state: str, timestamp: datetime.datetime
    ):
        self.project_id = project_id
        self.document_id = document_id
        self.user_name = user_name
        self.annotation_state = annotation_state
        self.timestamp = timestamp

    def __eq__(self, other):
        return (
            isinstance(other, Annotation)
            and other.project_id == self.project_id
            and other.document_id == self.document_id
            and other.user_name == self.user_name
            and other.annotation_state == self.annotation_state
            and other.timestamp == self.timestamp
        )

    def __repr__(self):
        return f"<Annotation by {self.user_name} (Project: {self.project_id}, Document: {self.document_id})>"

    def __str__(self):
        return repr(self)
