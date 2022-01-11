from django.db import models

from main.models import StateBaseModel, BaseModel


class TaskStatus(StateBaseModel):

    class Meta:
        db_table = 'task_status'


class TaskType(StateBaseModel):

    class Meta:
        db_table = 'task_type'


class FormatContentModel(BaseModel):
    id = models.BigAutoField(primary_key=True, db_column='id_format_content')
    name = models.CharField(max_length=100, db_column='format_name')

    class Meta:
        db_table = 'format_content'


class MetricsNameModel(BaseModel):
    id = models.BigAutoField(primary_key=True, db_column='id_metrics_name')
    name = models.CharField(max_length=150, db_column='metrics_name')

    class Meta:
        db_table = 'metrics_name'
