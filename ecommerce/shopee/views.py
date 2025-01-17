from django.shortcuts import render, redirect
from django.http import JsonResponse
import bcrypt
import jwt
from .models import UserData
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt


#Dashboard_view
def dashboard_view(request):
    return render(request, 'dashboard.html')

def get_registration_page(request):
    return render(request, 'register.html')
def get_login_page(request):
    return render(request, 'login.html')

@csrf_exempt
def post_registration_data(request):
    if request.method == 'POST':
        body = request.POST
        name = body.get('nameInput')
        phone_no = body.get('phoneInput')
        email = body.get('emailInput')
        password = body.get('passwordInput')
        

        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user = UserData.objects.create(name=name, phone_no=phone_no, email=email, password=hashed_password,)
            user.save()
            return JsonResponse({'message': 'success'}, status=201)
        except Exception as e:
            if 'unique constraint' in str(e):
                return JsonResponse({'message': 'exist'}, status=409)
            else:
                print(e)
                return JsonResponse({'message': 'Internal Server Error'}, status=500)
    else:
        return JsonResponse({'message': 'Method Not Allowed'}, status=405)

@csrf_exempt
def check_login(request):
    if request.method == 'POST':
        body = request.POST
        email = body.get('email')
        password = body.get('password')

        try:
            user = UserData.objects.get(email=email)

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                payload = {
                    'user_id': user.id,
                    'email': user.email
                }

                token = jwt.encode(payload, '8jR2sWnC4xQzHtUyL6vPbM9aZ3gD7eF1sK0oL7jX8wO9tR0hY5sF1iE3oQ1cK6gW2hS4aJ5bP9eV0jU4iO2qD6rH3lN9mS7tP1rY2gT8bA1uO3zR', algorithm='HS256')
                return JsonResponse({'message': 'success', 'token': token}, status=201)
            else:
                return JsonResponse({'message': 'Failed'}, status=401)
        except UserData.DoesNotExist:
            return JsonResponse({'message': 'NotExist'}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Internal Server Error'}, status=500)
    else:
        return JsonResponse({'message': 'Method Not Allowed'}, status=405)
    
@csrf_exempt
def get_expense_main_home_page(request):
    return render(request, 'mainHome.html')