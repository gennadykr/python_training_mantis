from model.project import Project
import random


def test_delete_project(app):
    if len(app.project.get_project_list()) == 0:
        app.project.create(Project(name="test"))
    old_projects = app.soap.get_project_list()
    project = random.choice(old_projects)
    app.project.delete_project(project)
    new_projects = app.soap.get_project_list()
    old_projects.remove(project)
    assert old_projects == new_projects
