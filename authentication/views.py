from django.shortcuts import render
from django.http import JsonResponse
from oauth2_provider.views import TokenView
from .models import UserLogin
from .utils import send_fcm_notification
from django.contrib.auth import authenticate


class CustomTokenView(TokenView):
    def post(self, request, *args, **kwargs):

        # Adding the username field if its missing
        
        # data = request.POST.copy()
        # if 'username' not in data:
        #     data['username'] = data.get('email')
        # request.POST = data

        username_or_phone = request.POST.get('username')
        user_pin = request.POST.get('password')
        fcm_key = request.POST.get('fcm_key')

        # Authenticate using either email or phone number
        user = authenticate(request, username=username_or_phone, password=user_pin)
        if user is None:
            return JsonResponse({'error': 'Invalid email/phone number or PIN'}, status=400)
        
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


# Views to register device to FCM and get the registration token

# import requests
# import json
# from django.http import HttpResponse


# def index(request):
#     return render(request, 'index.html')


# def send_notification(registration_ids , message_title , message_desc):
#     fcm_api = ""
#     project_id = ''

#     url = 'https://fcm.googleapis.com/v1/projects/' + project_id + '/messages:send'
    
#     headers = {
#         'Authorization': f'Bearer {fcm_api}',
#         'Content-Type': 'application/json; UTF-8',
#     }

#     payload = {
#         'message': {
#             'token': registration_ids[0],
#             'notification': {
#                 'title': "Hi",
#                 'body': "Bye"
#             },
#         }
#     }

#     result = requests.post(url, data=json.dumps(payload), headers=headers)
#     print(result.json())


# def send(request):
#     resgistration  = []
#     send_notification(resgistration , 'Code Keen added a new video' , 'Code Keen new video alert')
#     return HttpResponse("sent")


# def showFirebaseJS(request):
#     data='importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
#          'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
#          'var firebaseConfig = {' \
#          '        apiKey: "",' \
#          '        authDomain: "",' \
#          '        databaseURL: "",' \
#          '        projectId: "",' \
#          '        storageBucket: "",' \
#          '        messagingSenderId: "",' \
#          '        appId: "",' \
#          '        measurementId: ""' \
#          ' };' \
#          'firebase.initializeApp(firebaseConfig);' \
#          'const messaging=firebase.messaging();' \
#          'messaging.setBackgroundMessageHandler(function (payload) {' \
#          '    console.log(payload);' \
#          '    const notification=JSON.parse(payload);' \
#          '    const notificationOption={' \
#          '        body:notification.body,' \
#          '        icon:notification.icon' \
#          '    };' \
#          '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
#          '});'

#     return HttpResponse(data,content_type="text/javascript")
