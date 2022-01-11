from django.contrib.postgres.fields import ArrayField
from django.db import models

from main.models import BaseModel
from main.models.states import TaskType, TaskStatus


class Task(BaseModel):
    task_type = models.ForeignKey(TaskType, null=True, on_delete=models.SET_NULL)
    status = models.ForeignKey(TaskStatus, null=True, on_delete=models.SET_NULL)
    data = models.JSONField()
    priority = models.IntegerField()
    fields = ArrayField(
        models.CharField(max_length=50)
    )

    def __str__(self):
        return f'id: {self.id or None}, task_type: {self.task_type}, status: {self.status}, ' \
               f'data: {self.data}, priority: {self.priority}, fields: {self.fields}'

    class Meta:
        db_table = 'task'


class TaskResult(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    link = models.FileField()
    comment = models.TextField(null=True)

    class Meta:
        db_table = 'task_result'


class TypeFields(models.Model):
    task_type = models.OneToOneField(TaskType, on_delete=models.CASCADE, related_name='type_fields')
    fields = ArrayField(
        models.CharField(max_length=50)
    )

    class Meta:
        db_table = 'task_type_fields'
