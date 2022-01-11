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
    task_type_id = serializers.PrimaryKeyRelatedField(source='task_type', queryset=TaskType.objects.all())
    status = StatusSerializer(read_only=True)

    def validate(self, attrs):
        data = attrs.get('data')

        if not data:
            raise serializers.ValidationError('task must have data')

        if not data.keys() or not list(data.values())[0]:
            raise serializers.ValidationError('task must have loms')

        return attrs

    class Meta:
        model = Task
        fields = ['task_id', 'task_type_id', 'data', 'priority', 'fields', 'status']
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
