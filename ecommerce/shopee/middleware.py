from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import UserData
import jwt
from django.conf import settings

class AuthenticateUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_urls = [
            '/register/', '/login/', '/check-login/',
             '/','/favicon.ico', '/user/addUser/','/user/check-login','/expense/MainHome/','/expense/MainHome'
        ]
        print(request.path_info)
        if request.path_info in excluded_urls:
            return self.get_response(request)

        auth_header = request.headers.get('Authorization')
        print("auth_header",auth_header)
        if not auth_header or not auth_header.startswith('Bearer '):
            return HttpResponseRedirect(reverse('dashboard'))

        token = auth_header.split(' ')[1]
        print("token",token)

        try:
            decoded_token = jwt.decode(token,'8jR2sWnC4xQzHtUyL6vPbM9aZ3gD7eF1sK0oL7jX8wO9tR0hY5sF1iE3oQ1cK6gW2hS4aJ5bP9eV0jU4iO2qD6rH3lN9mS7tP1rY2gT8bA1uO3zR',algorithms=['HS256'], options={"verify_signature": False})
            print("decode",decoded_token)
            user_id = decoded_token.get('user_id')
            print("userId",user_id)

            if not user_id:
                return HttpResponseRedirect(reverse('dashboard'))

            user_obj = UserData.objects.get(id=user_id)
            print("user_obj",user_obj)
            request.user = user_obj  # Attach the user object to the request

        except jwt.ExpiredSignatureError:
            print("ExpiredSignatureError")
            return HttpResponseRedirect(reverse('dashboard'))
        except jwt.InvalidTokenError:
            print("InvalidTokenError")
            return HttpResponseRedirect(reverse('dashboard'))
        except UserData.DoesNotExist:
            print("UserData.DoesNotExist")
            return HttpResponseRedirect(reverse('dashboard'))

        return self.get_response(request)
