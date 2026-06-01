from django.urls import path
from .views import login_view, registration_view, dashboard_view, logout_view

urlpatterns = [
    # Strict Exact-Match Engine Routes
    path('', login_view),
    path('registration/', registration_view),
    path('dashboard/', dashboard_view),
    path('logout/', logout_view),
]