from django.shortcuts import render
from django.http import JsonResponse
from oauth2_provider.views import TokenView
from .models import UserLogin
from .utils import send_fcm_notification


class CustomTokenView(TokenView):
    def post(self, request, *args, **kwargs):
        # Extract email and fcm_key from the request
        email = request.POST.get('username')
        fcm_key = request.POST.get('fcm_key')
        
        try:
            user = UserLogin.objects.get(email=email)
        except UserLogin.DoesNotExist:
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


# Views to register device to FCM and get the registration token

# import requests
# import json
# from django.http import HttpResponse


# def index(request):
#     return render(request, 'index.html')


# def send_notification(registration_ids , message_title , message_desc):
#     fcm_api = "ya29.c.c0ASRK0GadGtWAGKm2zeurOWbPudOVjcQBdyRQYQqIvoi975H5kLfEUF5eKRxDx2Xjlp64zpIHrAIzZ0VGHRLZqze5P5t_L1vm_RQLFoGMkn0aBG7s0pBg_TFnon2cDIdGeKUtpg9mHqCfVsrjjuQ0dj4Caijq5nT8cGQXL9-Q1bvac0XnexgIvdAdqPBZ7fFlP9mrQFyUKesEbgUs826mn19Q_vChqEKq6sWIyfyATHJR558Rom-SZYdFeqGQ8a0EqdAEoTJW6nwRstO6BUdRzNJyGcHQHsmX9CIftACAI3ei40eAI6iSyBhfrr6ZZFAxIzbVCZGS6dR7h_NAI6AUrTlYHRT9Hd14tVnS_Tb6pCuK_upvtH7heOhutAN387Ax-m-xQriqv0St02gJlrSbfsvkuVsgRRben9XUukmQ11395-gsim67iXfbxlf34WeqB8yydBd6ucJgq6Z6rhYVzw7tIwmZ90cJFM_z2m6Jp6jMagzVh4a0Xl3nbjlb-k1ar9jd_Yy8ezQpqyb2wOqiSgz7qO3YVysYFkmxY3oZJx3djwIOFFRcpjnnXXUzo1Qlyf8MhMdk4_jMckwfIOs1l2gjd9laYjiI58zn3Wcyi85Yk79BchFnb-O6BRZJ_Bo4OgVu_yq7ltOmf7iokZu3xnnUOypSm3gVr4JxZ_j0nOXMco5jJY9tbU7Ubh6R2noc8066sB2oMJhUSVt63rurks_jqkz0Ug5psRS7vm90gXR43drod3cfhdFYZcMys61029lXsw_7VxYvVQqpUigQM9b19RrdVlp97WbnYgy2dFn5mrYbYto3jjnhgw5jrpkn2Xfwpxzi8dcMlXwciUFFSt6BqjicXwZ-zl1O2g6oteaXnQMc5pOgdcwdtYp2tjkVXcbYo3s5WVVRybSfzhMyn1ox206qdxBjIOuxVzx7x25g5qmZYqc0jc5ntvpWoQoYk3mw_Jl10RRlOMZhkVitwvmXd_sXjss321_oOegQV4XroQWcS_Q74jm"
#     project_id = 'my-app-3c1f9'

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
#     resgistration  = ['dO8LVySzZwTsdEMM80vwWH:APA91bHBo-0oKounxVz06hm9v1mkOeao48FrCW9GwGwtrf6wMADW7opj420nDej-StoYQKOwRNLQPiKBFAWBkpnd9zDtX-RXmpnQcOegxbZE31eKa_fsepNu1PQBzOo87HNPMqIlnAzW']
#     send_notification(resgistration , 'Code Keen added a new video' , 'Code Keen new video alert')
#     return HttpResponse("sent")


# def showFirebaseJS(request):
#     data='importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
#          'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
#          'var firebaseConfig = {' \
#          '        apiKey: "AIzaSyCoTv5p_S7wLMe2pFztfLSuMIK-1fo2rCc",' \
#          '        authDomain: "my-app-3c1f9.firebaseapp.com",' \
#          '        databaseURL: "https://my-app-3c1f9-default-rtdb.firebaseio.com",' \
#          '        projectId: "my-app-3c1f9",' \
#          '        storageBucket: "my-app-3c1f9.appspot.com",' \
#          '        messagingSenderId: "624069677006",' \
#          '        appId: "1:624069677006:web:0a1be95280c45ee1aae59f",' \
#          '        measurementId: "G-TVLD546RNT"' \
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
