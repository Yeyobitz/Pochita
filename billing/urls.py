from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_invoices, name='list_invoices'),
    path('create/', views.create_invoice, name='create_invoice'),
    path('view/<int:pk>/', views.view_invoice, name='view_invoice'),
    path('delete/<int:pk>/', views.delete_invoice, name='delete_invoice'),
]

