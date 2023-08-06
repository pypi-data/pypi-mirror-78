from .commands.AuthCommand import auth
from .commands.DeployCommand import deploy
# from .commands.CancelCommand import cancel
# from .commands.StatusCommand import status
from .commands.ProjectsCommand import projects
# from .commands.HistoryCommand import history


class CLI(object):
    """Deepserve.ai CLI. Register at deepserve.ai and deploy deep learning models with `deepserve deploy`"""

    def auth(self):
        """Connect your API token to Deepserve."""
        return auth()

    def deploy(self, project_name, file_path, notebook=None, api_key=None):
        """Deploy a finished model"""
        return deploy(project_name, file_path, notebook, api_key)

    # def cancel(self, project_name, api_key=None):
    #     """Cancel a deploy model"""
    #     return cancel(project_name, api_key)
    #
    # def status(self, project_name, api_key=None):
    #     """See the status of a deploy"""
    #     return status(project_name, api_key)
    #
    def projects(self, api_key=None):
        """See a list of projects"""
        return projects(api_key)
    #
    # def history(self, project_name, api_key=None):
    #     """View history for a project"""
    #     return history(project_name, api_key)
