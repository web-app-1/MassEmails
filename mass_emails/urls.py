from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('send_email/', views.send_mass_email, name='send_email'),
    path('process_emails/', views.process_emails, name='process_emails'),
    path('success/', views.success, name='success'),
    path('login/', auth_views.LoginView.as_view(template_name='mass_emails/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
]
