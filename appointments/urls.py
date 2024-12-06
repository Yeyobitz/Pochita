from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_appointments, name='list_appointments'),
    path('create/', views.create_appointment, name='create_appointment'),
    path('update/<int:appointment_id>/', views.update_appointment, name='update_appointment'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('check-availability/', views.check_availability, name='check_availability'),
]
