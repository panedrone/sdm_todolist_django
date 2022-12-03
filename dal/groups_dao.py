from dal.group import Group
from dal._groups_dao import _GroupsDao


class GroupsDao(_GroupsDao):

    def __init__(self, ds):
        super().__init__(ds)

    def rename(self, g_id, g_name):
        self.ds.filter(Group, {"g_id": g_id}).update(**{"g_name": g_name})
