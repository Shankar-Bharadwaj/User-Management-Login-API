from django.shortcuts import render
from django.http import JsonResponse
from oauth2_provider.views import TokenView
from .models import UserManagement
from .utils import send_fcm_notification

class CustomTokenView(TokenView):
    def post(self, request, *args, **kwargs):
        # Extract email and fcm_key from the request
        email = request.POST.get('username')
        fcm_key = request.POST.get('fcm_key')
        
        try:
            user = UserManagement.objects.get(email=email)
        except UserManagement.DoesNotExist:
            return JsonResponse({'error': 'Invalid email or password'}, status=400)
        
        # Check for existing FCM key
        if user.fcm_key and user.fcm_key != fcm_key:
            send_fcm_notification(
                user.fcm_key,
                'Logged In on Another Device',
                'You have logged in on another device.',
                {'type': 'C'}
            )
        
        # Update the FCM key
        user.fcm_key = fcm_key
        user.save()
        
        # Call the original token endpoint logic
        response = super().post(request, *args, **kwargs)
        return response
