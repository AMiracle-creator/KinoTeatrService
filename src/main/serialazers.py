from rest_framework import serializers

from .models import Task, TaskResult, ExtraData
from .models.states import TaskStatus, TaskType


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = ('id', 'name')
        read_only_fields = ('id', 'name')


class TaskSerializer(serializers.ModelSerializer):
    task_id = serializers.PrimaryKeyRelatedField(source='id', read_only=True)
    status = StatusSerializer(read_only=True)
    id = serializers.CharField(source='lk_id')
    logins = serializers.JSONField(source='data')
    type = serializers.PrimaryKeyRelatedField(source='task_type', queryset=TaskType.objects.all())

    def validate(self, attrs):
        logins = attrs.get('data')

        if not logins:
            raise serializers.ValidationError('task must have data')

        return attrs

    class Meta:
        model = Task
        fields = ['id', 'logins', 'type', 'task_id', 'status']
        read_only_fields = ('task_id', 'status')



class TaskResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskResult
        fields = ['task_id', 'link', 'comment']
        read_only_fields = ['task_id', 'link', 'comment']


class TaskTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    fields = serializers.ListField(source='type_fields.fields', allow_null=True)

    class Meta:
        model = TaskType
        fields = ['id', 'name', 'fields']


class TaskTypesWithExampleSerializer(serializers.Serializer):
    types = TaskTypeSerializer(many=True)
    examples = serializers.JSONField()


class ExtraDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraData
        fields = '__all__'
        read_only_fields = ('id',)
