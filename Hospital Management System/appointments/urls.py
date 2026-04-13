from django.urls import path
from .views import doctor_dashboard, patient_dashboard
from . import views

urlpatterns = [
    path('doctor/', doctor_dashboard, name='doctor_dashboard'),
    path('patient/', patient_dashboard, name='patient_dashboard'),
    path('book/', views.book_appointment, name='book_appointment'),
]