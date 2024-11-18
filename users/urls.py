from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_client, name='register_client'),
    path('profile/', views.profile_view, name='profile'),
]