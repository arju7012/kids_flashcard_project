# users/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Use Django's built-in LoginView
    path(
        'login/', 
        auth_views.LoginView.as_view(template_name='users/login.html'), 
        name='login'
    ),
    # Use Django's built-in LogoutView
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]