"""
Code generated by a tool. DO NOT EDIT.
https://sqldalmaker.sourceforge.net/
"""

from dal.project import Project


class _ProjectsDao:

    def __init__(self, ds):
        self.ds = ds

    def create_project(self, p):
        """
        (C)RUD: projects
        Generated values are passed to DTO.
        :param p: Project
        :return: None
        :raises Exception: if no rows inserted.
        """
        self.ds.create_one(p)

    def read_project(self, p_id):
        """
        C(R)UD: projects
        :param p_id: int
        :return: Project
        """
        return self.ds.read_one(Project, {'p_id': p_id})

    def delete_project(self, p_id):
        """
        CRU(D): projects
        :param p_id: int
        :return: int (the number of affected rows)
        """
        return self.ds.delete_one(Project, {'p_id': p_id})
