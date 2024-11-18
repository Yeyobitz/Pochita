from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_inventory, name='list_inventory'),
    path('update/<int:pk>/', views.update_inventory, name='update_inventory'),
    path('add/', views.update_inventory, name='add_inventory'),
    path('delete/<int:pk>/', views.delete_inventory, name='delete_inventory'),
]