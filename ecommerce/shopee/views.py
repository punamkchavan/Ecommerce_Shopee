from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
import bcrypt
import jwt
from .models import UserData
from datetime import datetime
from .models import Product, Category,Order,OrderItem


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

# List all products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

#Add new products
def product_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image') 
    
        if name and category_id and price and stock:
            try:
                category = Category.objects.get(id=category_id) 
                product = Product(
                    name=name,
                    description=description,
                    category=category,
                    price=price,
                    stock=stock,
                    image=image
                )
                product.save()
                return redirect('admin_product_list') 
            except Category.DoesNotExist:
                return render(request, 'products/admin_productform.html', {'error': 'Invalid category'})
        else:
            return render(request, 'products/admin_productform.html', {'error': 'All required fields must be filled'})

    categories = Category.objects.all()
    return render(request, 'products/admin_productform.html', {'categories': categories})

#Edit the products
def product_edit(request, id):
    product = get_object_or_404(Product, id=id)  
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')
        
        if name and category_id and price and stock:
            try:
                category = Category.objects.get(id=category_id) 
                product.name = name
                product.description = description
                product.category = category
                product.price = price
                product.stock = stock
                
                if image:
                    product.image = image 
                
                product.save()
                return redirect('admin_product_list') 
            except Category.DoesNotExist:
                return render(request, 'products/admin_productform.html', {'error': 'Invalid category', 'product': product})
        else:
            return render(request, 'products/admin_productform.html', {'error': 'All required fields must be filled', 'product': product})

    categories = Category.objects.all()
    return render(request, 'products/admin_productform.html', {'product': product, 'categories': categories})

#Delete the products
def product_delete(request, id):
    product = get_object_or_404(Product, id=id) 
    
    if request.method == 'POST':   
        product.delete()   
        return redirect('admin_product_list')   
    return render(request, 'products/admin_product_delete.html', {'product': product})


