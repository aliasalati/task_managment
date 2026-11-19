from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):

    class STATUS_CHOICES(models.TextChoices):
        PEDING = "peding", "Peding"
        IN_PROGRESS = "inprogress", "In Progress"
        COMPLETED = "completed", "Completed"

    class PRIORITY_CHOICES(models.IntegerChoices):
        LOW = 1, "Low"
        MEDIUM = 2, "Medium"
        HIGH = 3, "High"

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES.choices, default=PRIORITY_CHOICES.MEDIUM)
    status = models.CharField(choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.PEDING)
