from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

class AccountTest(APITestCase):
    def test_user_registeration_success(self):
        url = reverse("register")
        data = {
            "username": "Ali",
            "password": "aliasghar",
            "password2": "aliasghar"
        }
        request = self.client.post(url, data)
        self.assertEqual(request.status_code, 201)

    def test_user_registration_unsuccess(self):
        url = reverse("register")
        data = {
            "username": "Ali",
            "password": "aliasghar",
            "password2": ""
        }
        request = self.client.post(url, data)
        self.assertEqual(request.status_code, 400)

    def test_user_login_success(self):
        url = reverse("login")
        user = User.objects.create_user(username="Ali", password="aliasghar")
        data = {
            "username": "Ali",
            "password": "aliasghar"
        }
        request = self.client.post(url, data)
        self.assertEqual(request.status_code, 200)

    def test_login_invalid_credentials(self):
        url = reverse("login")
        user = User.objects.create_user(username="Ali", password="aliasghar")
        data = {
            "username": "Ali",
            "password": "aliasghr"
        }
        request = self.client.post(url, data)
        self.assertEqual(request.status_code, 401)

    def test_logout_with_valid_refresh_tokne(self):
        url = reverse("logout")
        user = User.objects.create_superuser(username="ali", password="aliasghar")
        refresh = RefreshToken.for_user(user)
        request = self.client.post(url, {"refresh" : str(refresh)})
        self.assertEqual(request.status_code, 205)

    def test_logout_blacklist_refresh_token(self):
        url = reverse("logout")
        user = User.objects.create_superuser(username="ali", password="aliasghar")
        refresh = RefreshToken.for_user(user)
        request = self.client.post(url, {"refresh" : str(refresh)})
        self.assertEqual(request.status_code, 205)
        response = self.client.post(reverse("token_refresh"), {"refresh" : refresh})
        self.assertEqual(response.status_code, 401)
        