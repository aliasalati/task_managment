from django.urls import path

from .views import ListCreateTask, TaskDetailView

urlpatterns = [
    path("", ListCreateTask.as_view(), name="task-list-create"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail")
]