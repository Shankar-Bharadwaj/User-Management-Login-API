import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request


def get_access_token(service_account_file):
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=["https://www.googleapis.com/auth/firebase.messaging"]
    )
    credentials.refresh(Request())
    return credentials.token


def send_fcm_notification(fcm_key, title, message, data=None):
    service_account_file = 'service-account-file.json'
    access_token = get_access_token(service_account_file)
    project_id = 'my-app-3c1f9'
    # print(access_token)

    url = 'https://fcm.googleapis.com/v1/projects/' + project_id + '/messages:send'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; UTF-8',
    }
    payload = {
        'message': {
            'token': fcm_key,
            'notification': {
                'title': title,
                'body': message
            },
            'data': data
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.json())
    return response.json()
