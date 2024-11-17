from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('appointments/', include('appointments.urls')),
    path('medical_records/', include('medical_records.urls')),
    path('inventory/', include('inventory.urls')),
    path('billing/', include('billing.urls')),
    path('notifications/', include('notifications.urls')),
    path('reports/', include('reports.urls')),
]
