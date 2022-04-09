from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import serializers 

# restframework
from rest_framework.response import Response
from rest_framework.decorators import api_view

#models
from .models import Task

#serializer
from .serializer import TaskSerializer

# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    """ 
    Return all views created in this project
    """

    api_urls = {
        'List view': '/task-list/',
        'Detail View': '/task-detail/<str:pk>/',
        'Create': '/task-create/',
        'Update': '/task-update/<str:pk>/',
        'Delete': '/task-delete/<str:pk>/',
    }
    return Response(api_urls)

@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.all().order_by('-id')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

#In views based functions it should pass the query to a Serializer, in VBC is automatic
# also it should go argument many=True because is not only one model instance instead is a list of instance(queryset)
# A Response must be returned with the serializer.data because in .data exist the data serialized

@api_view(['GET'])
def taskDetail(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def taskCreate(request):
    serializer = TaskSerializer(data = request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST'])
def taskUpdate(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task ,data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def taskDelete(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()

    return Response('Task was succesfully deleted')