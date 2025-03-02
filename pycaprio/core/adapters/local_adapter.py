from pycaprio.core.interfaces.adapter import BaseInceptionAdapter


class LocalInceptionAdapter(BaseInceptionAdapter):
    """
    Adapter for handling local INCEpTION projects stored as ZIP files.
    """

    def __init__(self, local_projects_dir: str):
        """
        Initializes the adapter with a directory containing ZIP files of exported INCEpTION projects.
        """
        self.local_projects_dir = local_projects_dir