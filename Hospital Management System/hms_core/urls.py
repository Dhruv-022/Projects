# hms_core/urls.py
from django.contrib import admin
from django.urls import path, include
from users.views import signup_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', signup_view, name='signup'), # Root URL goes to Signup
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
    path('appointments/', include('appointments.urls')),
]