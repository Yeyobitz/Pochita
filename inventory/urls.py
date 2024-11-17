from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_inventory, name='list_inventory'),  # Listar productos del inventario
    path('update/<int:pk>/', views.update_inventory, name='update_inventory'),  # Actualizar producto existente
    path('add/', views.update_inventory, name='add_inventory'),  # Agregar nuevo producto (usa la misma vista)
]
