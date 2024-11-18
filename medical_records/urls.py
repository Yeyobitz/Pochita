from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_medical_records, name='list_medical_records'),
    path('<int:pk>/', views.view_medical_record, name='view_medical_record'),
    path('create/', views.create_medical_record, name='create_medical_record'),
    path('api/clients/<int:client_id>/pets/', views.get_client_pets, name='get_client_pets'),
]




