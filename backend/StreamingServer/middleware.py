import json
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class UserAuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'GET':
            user_token = request.headers.get('Authorization')
        elif request.method == 'POST':
            try:
                user_token = json.loads(request.body.decode("utf-8", "ignore")).get('headers', {}).get('Authorization')
            except json.decoder.JSONDecodeError:
                user_token = None

        try:
            if user_token:
                user = User.objects.get(auth_token=user_token)
                request.api_user = user

        except ObjectDoesNotExist as ex:
            print('User not found, token recieved: {}'.format(user_token))

        return self.get_response(request)
