"""

My hand-coded extension of generated class

"""
from typing import List

from dal._groups_dao import _GroupsDao
from dal.data_store import DataStore
from dal.group import Group
from dal.group_li import GroupLI


class GroupsDao(_GroupsDao):

    def __init__(self, ds: DataStore):
        super().__init__(ds)

    def get_all_groups(self) -> List[GroupLI]:
        return self.ds.get_all_raw(GroupLI)

    def rename(self, g_id, g_name):
        return self.ds.update_by_filter(Group, data={"g_name": g_name}, params={"g_id": g_id})