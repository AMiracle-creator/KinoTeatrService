from main.models import BaseModel
from django.db import models

from main.models.states import FormatContentModel, MetricsNameModel


class ContentModel(BaseModel):
    id = models.BigAutoField(primary_key=True, db_column='id_content')
    resource = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    project_name = models.CharField(max_length=200)
    format_content = models.ForeignKey(FormatContentModel, null=True, on_delete=models.SET_NULL,
                                       db_column='id_format_content')
    name_content = models.CharField(max_length=100)
    url = models.URLField(null=True)
    success = models.BooleanField(default=False)
    success_date_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content'


class MetricsModel(BaseModel):
    material = models.ForeignKey(ContentModel, null=True, on_delete=models.SET_NULL)
    metrics_name = models.ForeignKey(MetricsNameModel, null=True, on_delete=models.SET_NULL,
                                     db_column='id_metrics_name')
    value = models.BigIntegerField(null=True)
    time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'metrics'