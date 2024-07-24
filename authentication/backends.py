import re
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

UserLogin = get_user_model()


class UserLoginBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not isinstance(username, str):
            return None
        email_validator = EmailValidator()
        # email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        mobile_pattern = r'^\d+$'

        try:
            email_validator(username)
            is_email = True
        except ValidationError:
            is_email = False

        if is_email:
            try:
                user = UserLogin.objects.get(email=username)
            except UserLogin.DoesNotExist:
                return None
        elif re.match(mobile_pattern, username):
            try:
                user = UserLogin.objects.get(user_mobile=username)
            except UserLogin.DoesNotExist:
                return None
        else:
            return None
        
        if user.check_user_pin(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return UserLogin.objects.get(pk=user_id)
        except UserLogin.DoesNotExist:
            return None
