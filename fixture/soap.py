from model.project import Project
from suds.client import Client
from suds import WebFault


class SoapHelper:
    def __init__(self, app):
        self.app = app

    def get_project_list(self):
        username = self.app.config["webadmin"]["username"]
        password = self.app.config["webadmin"]["password"]
        client = Client("http://localhost/mantisbt-2.5.1/api/soap/mantisconnect.php?wsdl")
        return self.convert_projects_to_model(client.service.mc_projects_get_user_accessible(username, password))

    def convert_projects_to_model(self,projects):
        def convert(project):
            return Project(id=str(project.id), name=project.name)
        return list(map(convert,projects))