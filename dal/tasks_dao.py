"""

My hand-coded extension of generated class

"""
from dal._tasks_dao import _TasksDao
from dal.task_li import TaskLI


class TasksDao(_TasksDao):

    def __init__(self, ds):
        super().__init__(ds)

    def get_by_project(self, p_id: int):
        fields = ['t_id', 't_date', 't_subject', 't_priority']
        params = {'p_id': p_id}
        tasks = self.ds.filter(TaskLI, params, fields).order_by('t_date', 't_id').all()
        return tasks
