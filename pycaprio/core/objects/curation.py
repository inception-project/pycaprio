import datetime


class Curation:
    """
    INCEpTION's Curation object
    """

    def __init__(
        self, project_id: int, document_id: int, user_name: str, document_state: str, timestamp: datetime.datetime
    ):
        self.project_id = project_id
        self.document_id = document_id
        self.user_name = user_name
        self.document_state = document_state
        self.timestamp = timestamp

    def __eq__(self, other):
        return (
            isinstance(other, Curation)
            and other.project_id == self.project_id
            and other.document_id == self.document_id
            and other.user_name == self.user_name
            and other.document_state == self.document_state
            and other.timestamp == self.timestamp
        )

    def __repr__(self):
        return f"<Curator #{self.user_name}: (State: {self.document_state}, Timestamp: {self.timestamp})>"

    def __str__(self):
        return repr(self)
