from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
import bcrypt
import jwt
from .models import UserData
from datetime import datetime
from .models import Product, Category,Order,OrderItem
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework_simplejwt.tokens import RefreshToken


#Dashboard_view
def dashboard_view(request):
    return render(request, 'dashboard.html')

#Regisration_view
def get_registration_page(request):
    return render(request, 'register.html')
def get_login_page(request):
    return render(request, 'login.html')
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
    
#Login_view
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
                    'email': user.email,
                    'role': user.role
                }

                token = jwt.encode(payload, '8jR2sWnC4xQzHtUyL6vPbM9aZ3gD7eF1sK0oL7jX8wO9tR0hY5sF1iE3oQ1cK6gW2hS4aJ5bP9eV0jU4iO2qD6rH3lN9mS7tP1rY2gT8bA1uO3zR', algorithm='HS256')

                return JsonResponse({
                    'message': 'success',
                    'token': token,
                    'role': user.role
                }, status=201)

            else:
                return JsonResponse({'message': 'Failed'}, status=401)
        except UserData.DoesNotExist:
            return JsonResponse({'message': 'NotExist'}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Internal Server Error'}, status=500)
    else:
        return JsonResponse({'message': 'Method Not Allowed'}, status=405) 
                 
#User_Dashboard
def get_expense_main_home_page(request):
    return render(request, 'mainHome.html')

#Admin_Dashboard
def get_admin_dashboard_page(request):
   return render(request, 'admin_dashboard.html')


#Admin side functions----------------------------------------------------------------------------------------
#Admin_Order_view
@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated])
def admin_order_view(request):
    if request.method == "GET":
        search_query = request.GET.get("search", "")
        if search_query:
            orders = Order.objects.filter(customer_name__icontains=search_query)
        else:
            orders = Order.objects.all()

        orders_data = [
            {
                "id": order.id,
                "customer_name": order.customer_name,
                "total_items": order.total_items,
                "total_price": order.total_price,
                "status": order.status,
                "created_at": order.created_at.isoformat(),
            }
            for order in orders
        ]
        return Response(orders_data, status=HTTP_200_OK)

    elif request.method == "DELETE":
        order_id = request.data.get("id")
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        return Response({"message": "Order deleted successfully."}, status=HTTP_200_OK)

    elif request.method == "POST":
        order_id = request.data.get("id")
        if order_id:  
            order = get_object_or_404(Order, id=order_id)
            order.customer_name = request.data.get("customer_name", order.customer_name)
            order.total_items = request.data.get("total_items", order.total_items)
            order.total_price = request.data.get("total_price", order.total_price)
            order.status = request.data.get("status", order.status)
            order.save()
            return Response({"message": "Order updated successfully."}, status=HTTP_200_OK)
        else:  
            Order.objects.create(
                customer_name=request.data["customer_name"],
                total_items=request.data["total_items"],
                total_price=request.data["total_price"],
                status=request.data["status"],
            )
            return Response({"message": "Order created successfully."}, status=HTTP_200_OK)

    return Response({"error": "Invalid request method."}, status=HTTP_400_BAD_REQUEST)