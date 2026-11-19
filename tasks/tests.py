from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from datetime import datetime, timedelta
from .models import Task

class TaskTestAPI(APITestCase):
    def test_list_only_user_tasks(self):
        url = reverse("task-list-create")
        user1 = User.objects.create_user(username="user1", password="user_1")
        user2 = User.objects.create_user(username="user2", password="user_2")
        Task.objects.create(owner=user1, title="task_1", description="the first task", due_date=datetime.now() + timedelta(days=2))
        Task.objects.create(owner=user1, title="task_2", description="the first task", due_date=datetime.now() + timedelta(days=2))
        Task.objects.create(owner=user2, title="task_3", description="the first task", due_date=datetime.now() + timedelta(days=2))
        token = RefreshToken.for_user(user1)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token.access_token}"
        )
        request = self.client.get(url)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 2)

    def test_create_task(self):
        url = reverse("task-list-create")
        user = User.objects.create_user(username="user1", password="user_1")
        token = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token.access_token}"
        )
        data = {"owner" : 1, "title" : "task_1", "description" : "the first task", "due_date" : datetime.now() + timedelta(days=2)}
        request = self.client.post(url, data)
        self.assertEqual(request.status_code, 201)

    def test_retrieve_task(self):
        user = User.objects.create_user(username="user1", password="user_1")
        token = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token.access_token}"
        )
        task = Task.objects.create(owner=user, title="task_1", description="the first task", due_date=datetime.now() + timedelta(days=2))

        request = self.client.get(reverse("task-detail", kwargs={"pk" : task.id}))
        self.assertEqual(request.status_code, 200)

    def test_update_task(self):
        user = User.objects.create_user(username="user1", password="user_1")
        token = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token.access_token}"
        )
        task = Task.objects.create(owner=user, title="task_1", description="the first task", due_date=datetime.now() + timedelta(days=2))
        request = self.client.patch(reverse("task-detail", kwargs={"pk":task.id}), {"title" : "updated title"})
        self.assertEqual(request.status_code, 200)

    def test_delete_task(self):
        user = User.objects.create_user(username="user1", password="user_1")
        token = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token.access_token}"
        )
        task = Task.objects.create(owner=user, title="task_1", description="the first task", due_date=datetime.now() + timedelta(days=2))
        request = self.client.delete(reverse("task-detail", kwargs={"pk" : task.id}))
        self.assertEqual(request.status_code, 204)