from django.db import models


class BaseModel(models.Model):
    pass

    class Meta:
        abstract = True


class StateBaseModel(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        abstract = True
