from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_appointments, name='list_appointments'),
    path('create/', views.create_appointment, name='create_appointment'),
    path('<int:pk>/update/', views.update_appointment, name='update_appointment'),
    path('appointment/<int:pk>/cancel/', views.cancel_appointment, name='cancel_appointment'),

]
