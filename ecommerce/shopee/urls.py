
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views
urlpatterns = [
    path('home/',views.home_view,name='home'),
    path('register/',views.register_view,name='register'),
    path('', views.login_view, name='login'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('logout/', views.logout, name='logout'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
