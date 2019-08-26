class Document:
    """
    INCEpTION's Document object
    """

    def __init__(self, project_id: int, document_id: int, document_name: str, document_state: str):
        self.project_id = project_id
        self.document_id = document_id
        self.document_name = document_name
        self.document_state = document_state

    def __eq__(self, other):
        return isinstance(other, Document) and \
               other.project_id == self.project_id and \
               other.document_id == self.document_id and \
               other.document_name == self.document_name and \
               other.document_state == self.document_state

    def __repr__(self):
        return f"<Document #{self.document_id}: {self.document_name} (Project: {self.project_id})>"

    def __str__(self):
        return repr(self)
