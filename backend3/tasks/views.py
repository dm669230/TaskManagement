from django.shortcuts import render
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import pandas as pd

# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer #ask what is seriallizer

    @action(detail=False, methods=['get']) # ask what it use for
    def export(self, request):
        user_id = request.GET.get('user_id')
        task = Task.objects.filter(user_id = user_id).values()
        df = pd.DataFrame(list(task))
        df.to_excel('task.xlsx', index=True)
        with open ('task.xlsx', 'rb') as f:
            data = f.read()
        response = Response(data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') 
        response['Content-Desposition'] = 'attachment; filename ="task.xlsx"'
        return response
