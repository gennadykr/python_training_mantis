from model.project import Project
import re

class ProjectHelper:
    def __init__(self, app):
        self.app = app

    def open_project_page(self):
        wd = self.app.wd
        if wd.current_url.endswith("/manage_proj_page.php") and \
                        len(wd.find_elements_by_css_selector("input[value='Create New Project']")) > 0:
            pass
        else:
            wd.get(self.app.base_url + "manage_proj_page.php")

    def returns_to_project_page(self):
        self.open_project_page()

    def fill_the_field(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def fill_the_form(self,project):
        wd = self.app.wd
        self.fill_the_field("name",project.name)

    def create(self, project):
        self.open_project_page()
        wd = self.app.wd
        wd.find_element_by_css_selector("input[value='Create New Project']").click()
        self.fill_the_form(project)
        wd.find_element_by_css_selector("input[value='Add Project']").click()
        self.returns_to_project_page()
        self.project_cache = None

    project_cache = None

    def get_project_list(self):
        if self.project_cache is None:
            self.open_project_page()
            wd = self.app.wd
            table = wd.find_elements_by_css_selector(".table-responsive")[0]
            rows = table.find_elements_by_css_selector("tbody tr")
            self.project_cache = []
            for row in rows:
                cell = row.find_elements_by_css_selector("td")[0]
                project_link = cell.find_element_by_css_selector("a")
                project_name = project_link.text
                project_url = project_link.get_attribute('href')
                m = re.search('(?<=project_id=)\d+', project_url)
                project_id = m.group(0)
                self.project_cache.append(Project(id=project_id, name=project_name))
        return list(self.project_cache)


    def delete_project(self,project):
        self.open_project_page()
        wd = self.app.wd
        wd.find_element_by_link_text(project.name).click()
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        wd.find_element_by_css_selector(".alert input[value='Delete Project']").click()
        self.returns_to_project_page()
        self.project_cache = None

