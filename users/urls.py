from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_client, name='register_client'),
    path('profile/', views.profile_view, name='profile'),
    path('validate_username/', views.validate_username, name='validate_username'),
    path('validate_email/', views.validate_email, name='validate_email'),
]