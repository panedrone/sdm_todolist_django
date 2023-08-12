from datetime import datetime

# from django.shortcuts import get_object_or_404  # , get_list_or_404
import django
from django.http import HttpResponse
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from dal.data_store import create_ds
from dal.project import Project
from dal.project_li import ProjectLi
from dal.projects_dao import ProjectsDao
from dal.task import Task
from dal.task_li import TaskLi
from dal.tasks_dao import TasksDao

django.setup()

_ds = create_ds()

dao_p = ProjectsDao(_ds)
dao_t = TasksDao(_ds)

DT_FORMAT = '%Y-%m-%d %H:%M:%S'


class ProjectLiSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLi
        fields = '__all__'  # '__all__' cannot be used with HyperlinkedModelSerializer


class ProjectSerializer(serializers.ModelSerializer):  # HyperlinkedModelSerializer

    p_id = serializers.IntegerField(required=False, allow_null=True)  # for a new one
    p_name = serializers.CharField(required=True, min_length=1, max_length=256)

    class Meta:
        model = Project
        fields = '__all__'


# list item without comments:

class TaskLiSerializer(serializers.HyperlinkedModelSerializer):
    t_id = serializers.IntegerField(required=True)
    t_date = serializers.DateTimeField(required=True, format=DT_FORMAT)
    t_priority = serializers.IntegerField(required=True)

    class Meta:
        model = TaskLi
        fields = ['t_id', 'p_id', 't_priority', 't_date', 't_subject']  # '__all__ not working here


class NewTaskSerializer(serializers.ModelSerializer):  # HyperlinkedModelSerializer

    t_subject = serializers.CharField(required=True, min_length=1, max_length=256)

    class Meta:
        model = Task
        fields = ['t_subject']  # mandatory


class TaskEditSerializer(serializers.ModelSerializer):  # HyperlinkedModelSerializer

    t_id = serializers.IntegerField(required=True)
    p_id = serializers.IntegerField(required=True)
    t_priority = serializers.IntegerField(required=True)
    t_date = serializers.DateTimeField(required=True, format=DT_FORMAT)
    t_subject = serializers.CharField(required=True, min_length=1, max_length=256)
    t_comments = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Task
        fields = '__all__'


class ProjectListView(APIView):
    @staticmethod
    def get(_):
        projects = dao_p.get_all_projects()
        sz = ProjectLiSerializer(projects, many=True)
        return Response(sz.data)

    @staticmethod
    def post(request):
        sz = ProjectSerializer(data=request.data)
        sz.is_valid(raise_exception=True)
        dao_p.create_project(sz)
        return HttpResponse(status=status.HTTP_201_CREATED)


class ProjectView(APIView):
    @staticmethod
    def get(_, p_id):
        project = dao_p.read_project(p_id)
        sz = ProjectSerializer(project)
        return Response(sz.data)

    @staticmethod
    def put(request, p_id):
        sz = ProjectSerializer(data=request.data, partial=True)
        sz.is_valid(raise_exception=True)
        dao_p.rename_project(p_id, sz.data['p_name'])
        return HttpResponse(status=status.HTTP_200_OK)

    @staticmethod
    def delete(_, p_id):
        _ds.delete_by_filter(Task, {'p_id': p_id})
        dao_p.delete_project(p_id)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class ProjectTasksView(APIView):
    @staticmethod
    def get(_, p_id):
        queryset = dao_t.get_by_project(p_id)
        sz = TaskLiSerializer(queryset, many=True)
        return Response(sz.data)

    @staticmethod
    def post(request, p_id):
        sz = NewTaskSerializer(data=request.data)
        sz.is_valid(raise_exception=True)  # to make validated_data available
        task = Task(**sz.validated_data)
        task.p_id = p_id
        now = datetime.now()
        dt_string = now.strftime(DT_FORMAT)
        task.t_date = dt_string
        task.t_priority = 1
        task.t_comments = ''
        dao_t.create_task(task)
        return HttpResponse(status=status.HTTP_201_CREATED)


class TaskView(APIView):
    @staticmethod
    def get(_, t_id):
        t = dao_t.read_task(t_id)
        sz = TaskEditSerializer(t, many=False)
        resp = Response(sz.data)
        return resp

    @staticmethod
    def put(request, t_id):
        sz = TaskEditSerializer(data=request.data)
        sz.is_valid(raise_exception=True)
        dao_t.update_task(t_id, sz.data)
        return HttpResponse(status=status.HTTP_200_OK)

    @staticmethod
    def delete(_, t_id):
        dao_t.delete_task(t_id)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
