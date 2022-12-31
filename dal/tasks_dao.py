"""

My hand-coded extension of generated class

"""
from dal._tasks_dao import _TasksDao
from dal.task_li import TaskLI


class TasksDao(_TasksDao):

    def __init__(self, ds):
        super().__init__(ds)

    def get_by_group(self, g_id: int):
        return self.ds.filter(TaskLI, {'g_id': g_id}).order_by('t_date', 't_id').all()
