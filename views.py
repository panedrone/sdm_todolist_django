from datetime import datetime

from django.shortcuts import get_object_or_404  # , get_list_or_404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from dal.data_store import ds
from dal.group import Group
from dal.group_li import GroupLI
from dal.task import Task


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
    # https://www.youtube.com/watch?v=b680A5fteEo
    @staticmethod
    def get(request):
        queryset = ds().get_all(GroupLI)  # get_all uses raw-sql, and this sql performs "order by"
        serializer = GroupLISerializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupView(APIView):
    @staticmethod
    def get(request, g_id):
        # https://www.youtube.com/watch?v=b680A5fteEo
        queryset = get_object_or_404(Group, g_id=g_id)  # raise Http404 if not found
        serializer = GroupSerializer(queryset, many=False)
        return Response(serializer.data)

    @staticmethod
    def put(request, g_id):
        obj = get_object_or_404(Group, g_id=g_id)
        serializer = GroupSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
        # if serializer.is_valid():
        #     serializer.g_id = g_id
        #     serializer.save()
        #     return Response(status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, g_id):
        Task.objects.filter(g_id=g_id).delete()
        get_object_or_404(Group, g_id=g_id).delete()  # raise Http404 if not found
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupTasksView(APIView):
    @staticmethod
    def get(request, g_id):
        queryset = Task.objects.filter(g_id=g_id).order_by('t_date', 't_id').all()
        serializer = TaskLISerializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, g_id):
        task = Task()
        # task.t_id = -1
        task.g_id = g_id
        now = datetime.now()
        # task.t_date = now
        dt_string = now.strftime("%Y-%m-%d")
        task.t_date = dt_string
        task.t_priority = 1
        task.t_comments = ''
        # ....................
        sz = TaskSerializer(data=request.data)
        sz.is_valid()  # to access data
        task.t_subject = sz.data['t_subject']
        sz = TaskSerializer(data=task.__dict__, many=False)
        if not sz.is_valid():
            return Response(sz.errors, status=status.HTTP_400_BAD_REQUEST)
        sz.save()
        return Response(status=status.HTTP_201_CREATED)


class TaskView(APIView):
    @staticmethod
    def get(request, t_id):
        # https://www.youtube.com/watch?v=b680A5fteEo
        queryset = get_object_or_404(Task, t_id=t_id)  # raise Http404 if not found
        serializer = TaskSerializer(queryset, many=False)
        return Response(serializer.data)

    @staticmethod
    def put(request, t_id):
        # https://stackoverflow.com/questions/69071531/how-to-use-django-serializer-to-update-an-instance
        obj = get_object_or_404(Task, t_id=t_id)
        task = TaskSerializer(obj, data=request.data, partial=True)
        # https://stackoverflow.com/questions/65155286/create-object-with-serializer-django-drf
        task.is_valid(raise_exception=True)
        # if not task.is_valid():
        #     return Response(task.errors, status=status.HTTP_400_BAD_REQUEST)
        # task.t_id = t_id
        task.save()
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, t_id):
        get_object_or_404(Task, t_id=t_id).delete()  # raise Http404 if not found
        return Response(status=status.HTTP_204_NO_CONTENT)
