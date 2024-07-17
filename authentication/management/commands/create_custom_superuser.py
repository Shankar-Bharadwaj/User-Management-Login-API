from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import getpass

class Command(BaseCommand):
    help = 'Create a superuser with custom user model interactively'

    def handle(self, *args, **kwargs):
        UserLogin = get_user_model()

        # Prompt for email
        email = input('Email: ')
        if UserLogin.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f'Superuser with email {email} already exists'))
            return

        # Prompt for user PIN (password)
        user_pin = self.get_password()

        # Prompt for additional fields
        user_mobile = input('User Mobile: ')
        international_calling_code = input('International Calling Code: ')
        calling_country = input('Calling Country: ')

        # Create the superuser
        UserLogin.objects.create_superuser(
            email=email,
            user_pin=user_pin,
            user_mobile=user_mobile,
            international_calling_code=international_calling_code,
            calling_country=calling_country
        )
        self.stdout.write(self.style.SUCCESS(f'Superuser with email {email} created successfully'))

    def get_password(self):
        return getpass.getpass('Pin: ')
