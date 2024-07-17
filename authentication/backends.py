# backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

UserLogin = get_user_model()

class UserLoginBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserLogin.objects.get(email=username)
        except UserLogin.DoesNotExist:
            try:
                user = UserLogin.objects.get(user_mobile=username)
            except UserLogin.DoesNotExist:
                return None

        if user.check_user_pin(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return UserLogin.objects.get(pk=user_id)
        except UserLogin.DoesNotExist:
            return None
