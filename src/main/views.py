from django.http import Http404
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import status

from .models import Task, TaskResult, ExtraData
from .models.states import TaskType
from .modules.parser_starter import parser_starter
from .serialazers import TaskSerializer, TaskResultSerializer, TaskTypeSerializer, ExtraDataSerializer
from .tasks import start_parse


class MainApiView(APIView):
    """Class for checking api"""

    def get(self, request):
        return Response({'status': 'ok'})


class TaskViewSet(viewsets.ModelViewSet):
    """
        List, update, delete, get or create a task instance.
    """
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def create(self, request, *args, **kwargs):
        print("XXXX_ ", request.data)
        response = super().create(request, *args, **kwargs, status=status.HTTP_200_OK)

        print("ZZZZ_ ", response)
        items = request.data['logins']

        if type(items) != type([]):
            return Response({"message": 'items is not list'})

        parser_starter(response.data['task_id'], response.data['id'], items)

        return Response(status=status.HTTP_200_OK)



class TaskResultViewSet(ReadOnlyModelViewSet):
    """
        List, update, delete, get or create a task_result instance.
    """
    serializer_class = TaskResultSerializer
    queryset = TaskResult.objects.all()

    def get_object(self):
        sku_id = self.kwargs['pk']

        try:
            result = TaskResult.objects.get(task_id=sku_id)
            print(result)
            return result
        except TaskResult.DoesNotExist:
            raise Http404


class FileView(APIView):
    def get_task_result(self, id):
        try:
            return TaskResult.objects.get(id=id)
        except TaskResult.DoesNotExist:
            raise Http404

    def get(self, request, id, _=None):
        task_result = self.get_task_result(id)
        return redirect(task_result.link.url)


class ExtraDataViewSet(viewsets.ModelViewSet):
    """
        List, update, delete, get or create a extra_data instance.
    """
    serializer_class = ExtraDataSerializer
    queryset = ExtraData.objects.all()
