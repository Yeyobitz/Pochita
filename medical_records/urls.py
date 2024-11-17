from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_medical_records, name='list_medical_records'),
    path('<int:pk>/', views.view_medical_record, name='view_medical_record'),
]
