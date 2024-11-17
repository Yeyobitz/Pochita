from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from users.views import custom_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('appointments/', include('appointments.urls')),
    path('medical_records/', include('medical_records.urls')),
    path('inventory/', include('inventory.urls')),
    path('billing/', include('billing.urls')),
    path('notifications/', include('notifications.urls')),
    path('reports/', include('reports.urls')),
    path('users/', include('users.urls')),  # URLs de la app `users`
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
]
