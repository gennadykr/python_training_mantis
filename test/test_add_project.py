from model.project import Project
import pytest

testdata = [
    Project(name="name1"),
    Project(name="name2"),
]

@pytest.mark.parametrize("project", testdata, ids=[repr(x) for x in testdata])
def test_add_project(app, project):
    old_projects = app.project.get_project_list()
    if project in old_projects:
        app.project.delete_project(project)
        old_projects = app.project.get_project_list()

    app.project.create(project)
    new_projects = app.project.get_project_list()

    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
