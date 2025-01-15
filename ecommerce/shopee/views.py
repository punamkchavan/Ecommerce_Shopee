from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import UserRegistrationForm
from .models import UserData
import jwt
from django.conf import settings
from datetime import datetime, timedelta
from .forms import LoginForm
from django.contrib.auth import authenticate

# Create your views here.

#Home_view
def home_view(req):
    return render(req,'home.html')

#JWT_Token_view
def generate_jwt_token(user):
    """
    Helper function to generate JWT token after successful registration.
    """
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=1),  # Set expiration for 1 day
        'iat': datetime.utcnow(),  # Issued at
    }

    # Generate the JWT token using the secret key from settings.py
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token
#registration_view
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create new user
            user = form.save()

            # Generate JWT token for the new user
            token = generate_jwt_token(user)

            # Return the token in a JsonResponse
            return JsonResponse({'message': 'Registration successful', 'token': token})

    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

#Login_view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Extract credentials
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Try to authenticate the user
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # Generate JWT token for the authenticated user
                token = generate_jwt_token(user)

                # Return the token in a JsonResponse
                return JsonResponse({'message': 'Login successful', 'token': token})

            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=400)
        else:
            return JsonResponse({'message': 'Invalid form data'}, status=400)
    
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

#User_Dashboard_view
def user_dashboard(request):
    # Logic for user dashboard
    return render(request, 'user_dashboard.html')
#def user_dashboard(request):
    #if not request.user.is_authenticated:
        # If there's no user object attached to the request (means JWT was not valid), redirect to home
        #return redirect('home')

    # Now you can access request.user and display the authenticated user's data
    #user = request.user
    #return render(request, 'user_dashboard.html', {'user': user})

#Logout_view
def logout(request):
    # You can clear the JWT token stored in the client's browser (e.g., in cookies or local storage)
    response = redirect('home')
    
    # Clear any JWT-related session data or cookies here if you're storing it
    # Example: response.delete_cookie('jwt_token')
    
    return response

