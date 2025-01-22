
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
    path('new_dashboard/', views.get_admin_dashboard_page, name='admin_home'),
    path("ad_orders/",views.admin_order_view, name="admin_orders"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
