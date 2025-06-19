# accounts/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # for login/logout
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('accounts/logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
]
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # 👈 Place this BEFORE username route
    path('profile/<str:username>/', views.profile_view, name='profile'),  # 👈 Last
]
