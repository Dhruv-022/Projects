from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Prefix Match Pass-Through: Captures the implicit empty starting point, 
    # chops off zero characters, and hands the full intact URL down to your login folder.
    path('', include('system.urls')),
]