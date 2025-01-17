from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.get_registration_page, name='register'),
    path('login/', views.get_login_page, name='login'),
    path('check-login/', views.check_login, name='check_login'),
    path('user/addUser/', views.post_registration_data, name='add_user'),
    path('user/check-login', views.check_login, name='check_login'),
    path('expense/MainHome/', views.get_expense_main_home_page, name='main_home'),
]
