from datetime import datetime

# from django.shortcuts import get_object_or_404  # , get_list_or_404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from dal.data_store import ds
from dal.group import Group
from dal.group_li import GroupLI
from dal.groups_dao import GroupsDao
from dal.task import Task
from dal.tasks_dao import TasksDao

dao_g = GroupsDao(ds())
dao_t = TasksDao(ds())


class GroupLISerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GroupLI
        fields = ['g_id', 'g_name', 'g_tasks_count']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['g_id', 'g_name']


# list item without comments:

class TaskLISerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ['t_id', 'g_id', 't_priority', 't_date', 't_subject']


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ['t_id', 'g_id', 't_priority', 't_date', 't_subject', 't_comments']


class GroupListView(APIView):
    @staticmethod
    def get(request):
        queryset = ds().get_all_raw(GroupLI)  # get_all uses raw-sql, and this sql performs "order by"
        serializer = GroupLISerializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = GroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ds().create_one(serializer)
        return Response(status=status.HTTP_201_CREATED)


class GroupView(APIView):
    @staticmethod
    def get(request, g_id):
        queryset = dao_g.read_group(g_id)
        serializer = GroupSerializer(queryset, many=False)
        return Response(serializer.data)

    @staticmethod
    def put(request, g_id):
        queryset = ds().read_one(Group, {'g_id': g_id})
        serializer = GroupSerializer(queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        ds().update_one(serializer)
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, g_id):
        ds().delete_by_filter(Task, {'g_id': g_id})
        dao_g.delete_group(g_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupTasksView(APIView):
    @staticmethod
    def get(request, g_id):
        queryset = ds().filter(Task, {'g_id': g_id}).order_by('t_date', 't_id').all()
        serializer = TaskLISerializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, g_id):
        task = Task()
        task.g_id = g_id
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d")
        task.t_date = dt_string
        task.t_priority = 1
        task.t_comments = ''
        # ....................
        sz = TaskSerializer(data=request.data)
        sz.is_valid()  # to make data available, no raise_exception=True
        task.t_subject = sz.data['t_subject']
        sz = TaskSerializer(data=task.__dict__, many=False)
        sz.is_valid(raise_exception=True)
        ds().create_one(sz)
        return Response(status=status.HTTP_201_CREATED)


class TaskView(APIView):
    @staticmethod
    def get(request, t_id):
        queryset = dao_t.read_task(t_id)
        serializer = TaskSerializer(queryset, many=False)
        return Response(serializer.data)

    @staticmethod
    def put(request, t_id):
        queryset = dao_t.read_task(t_id)
        sz = TaskSerializer(queryset, data=request.data, partial=True)
        sz.is_valid(raise_exception=True)
        ds().update_one(sz)
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, t_id):
        dao_t.delete_task(t_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
