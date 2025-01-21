
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views 
urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.get_registration_page, name='register'),
    path('login/', views.get_login_page, name='login'),
    path('check-login/', views.check_login, name='check_login'),
    path('user/addUser/', views.post_registration_data, name='add_user'),
    path('user/check-login', views.check_login, name='check_login'),
    path('expense/MainHome/', views.get_expense_main_home_page, name='main_home'),
    path('admin/dashboard/', views.get_admin_dashboard_page, name='admin_home'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/edit/<int:id>/', views.product_edit, name='product_edit'),
    path('products/delete/<int:id>/', views.product_delete, name='product_delete'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
