from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializer import TaskSerializer
from .filters import TaskFilter
from .models import Task
from .pagination import TaskPagination

class ListCreateTask(ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TaskPagination
    filter_backends = [DjangoFilterBackend,
                       SearchFilter,
                       OrderingFilter]
    filter_class = TaskFilter
    filterset_fields = [
        "title",
        "description",
        "status",
        "priority"
    ]
    ordering_fields = [
        "created_at",
        "priority",
    ]
    search_fields = [
        "title", "description"
    ]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)