from datetime import datetime

# from django.shortcuts import get_object_or_404  # , get_list_or_404
import django
from django.http import HttpResponse
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from dal.data_store import create_ds
from dal.group import Group
from dal.group_li import GroupLI
from dal.groups_dao import GroupsDao
from dal.task import Task
from dal.tasks_dao import TasksDao

django.setup()

_ds = create_ds()

dao_g = GroupsDao(_ds)
dao_t = TasksDao(_ds)


class GroupLISerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupLI
        fields = '__all__'  # '__all__' cannot be used with HyperlinkedModelSerializer


class NewGroupSerializer(serializers.ModelSerializer):
    g_name = serializers.CharField(required=True, max_length=256)

    class Meta:
        model = Group
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):  # HyperlinkedModelSerializer

    g_id = serializers.IntegerField(required=False, allow_null=True)  # for a new one
    g_name = serializers.CharField(required=True, max_length=256)

    class Meta:
        model = Group
        fields = '__all__'


# list item without comments:

class TaskLISerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ['t_id', 'g_id', 't_priority', 't_date', 't_subject']


class NewTaskSerializer(serializers.ModelSerializer):  # HyperlinkedModelSerializer

    t_subject = serializers.CharField(required=True, max_length=256)

    class Meta:
        model = Task
        fields = ['t_subject']


class TaskSerializer(serializers.ModelSerializer):  # HyperlinkedModelSerializer

    t_id = serializers.IntegerField(required=True)
    g_id = serializers.IntegerField(required=True)
    t_priority = serializers.IntegerField(required=True)
    t_date = serializers.DateField(required=True)
    t_subject = serializers.CharField(required=True, max_length=256)
    t_comments = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Task
        fields = '__all__'


class GroupListView(APIView):
    @staticmethod
    def get(request):
        queryset = _ds.get_all_raw(GroupLI)
        serializer = GroupLISerializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = NewGroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return HttpResponse(status=status.HTTP_201_CREATED)


class GroupView(APIView):
    @staticmethod
    def get(request, g_id):
        queryset = dao_g.read_group(g_id)
        serializer = GroupSerializer(queryset, many=False)
        return Response(serializer.data)

    @staticmethod
    def put(request, g_id):
        queryset = dao_g.read_group(g_id)
        # queryset = ds().read_one(Group, {'g_id': g_id})
        serializer = GroupSerializer(queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        _ds.update_one(serializer)
        return HttpResponse(status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, g_id):
        _ds.delete_by_filter(Task, {'g_id': g_id})
        dao_g.delete_group(g_id)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class GroupTasksView(APIView):
    @staticmethod
    def get(request, g_id):
        queryset = _ds.filter(Task, {'g_id': g_id}).order_by('t_date', 't_id').all()
        serializer = TaskLISerializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, g_id):
        sz = NewTaskSerializer(data=request.data)
        sz.is_valid(raise_exception=True)  # to make validated_data available
        task = Task(**sz.validated_data)
        task.g_id = g_id
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d")
        task.t_date = dt_string
        task.t_priority = 1
        task.t_comments = ''
        task.save()
        return HttpResponse(status=status.HTTP_201_CREATED)


class TaskView(APIView):
    @staticmethod
    def get(request, t_id):
        queryset = dao_t.read_task(t_id)
        serializer = TaskSerializer(queryset, many=False)
        resp = Response(serializer.data)
        return resp

    @staticmethod
    def put(request, t_id):
        # request.data['t_id'] = t_id
        # sz = TaskSerializer(data=request.data)
        queryset = dao_t.read_task(t_id)  # failed to save without queryset (errors)
        sz = TaskSerializer(queryset, data=request.data)
        sz.is_valid(raise_exception=True)
        _ds.update_one(sz)
        return HttpResponse(status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, t_id):
        dao_t.delete_task(t_id)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
