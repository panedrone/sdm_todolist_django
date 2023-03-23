"""

My hand-coded extension of generated class

"""
from typing import List

from dal._projects_dao import _ProjectsDao
from dal.data_store import DataStore
from dal.project import Project
from dal.project_li import ProjectLI


class ProjectsDao(_ProjectsDao):

    def __init__(self, ds: DataStore):
        super().__init__(ds)

    def get_all_projects(self) -> List[ProjectLI]:
        return self.ds.get_all_raw(ProjectLI)

    def rename_project(self, p_id, p_name):
        return self.ds.update_by_filter(Project, data={"p_name": p_name}, params={"p_id": p_id})