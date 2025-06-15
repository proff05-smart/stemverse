from django.urls import path
from . import views  # make sure you have this line if not already present
from .views import ProfileDetailView, ProfileUpdateView
urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('<str:username>/', ProfileDetailView.as_view(), name='profile'),
    path('<str:username>/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
]

