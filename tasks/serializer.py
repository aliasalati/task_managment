from rest_framework import serializers

from .models import Task

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ["owner", "title", "description", "priority", "due_date", "status", "created_at"]
        read_only_fields = ["owner", "created_at"]
