from typing import List

from dal._groups_dao import _GroupsDao
from dal.group_li import GroupLI


class GroupsDao(_GroupsDao):

    def __init__(self, ds):
        super().__init__(ds)

    def get_all_groups(self) -> List[GroupLI]:
        return self.ds.get_all_raw(GroupLI)
