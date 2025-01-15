from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from .models import UserData
import jwt


class AuthenticateUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_urls = [
            'register/', 'login/', 'home/', 'user_dashboard/', '/',
        ]
        print(request.path_info)
        
        if request.path_info in excluded_urls:
            return self.get_response(request)

        auth_header = request.headers.get('Authorization')
        print("auth_header", auth_header)
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return HttpResponseRedirect(reverse('home'))

        token = auth_header.split(' ')[1]
        print("token", token)

        try:
            decoded_token = jwt.decode(
                token,
                settings.SECRET_KEY,  # Using the secret key from settings
                algorithms=['HS256'],
                options={"verify_signature": False}  # Only decode without verifying signature for this example
            )
            print("decode", decoded_token)
            
            user_id = decoded_token.get('user_id')
            print("userId", user_id)

            if not user_id:
                return HttpResponseRedirect(reverse('home'))

            user_obj = UserData.objects.get(id=user_id)
            print("user_obj", user_obj)
            request.user = user_obj  # Attach the user object to the request

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, UserData.DoesNotExist) as e:
            print(str(e))  # Log the specific error message
            return HttpResponseRedirect(reverse('home'))

        return self.get_response(request)
