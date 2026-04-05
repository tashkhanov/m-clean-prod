from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('services/', views.services_page, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
]
