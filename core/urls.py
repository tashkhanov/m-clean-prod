from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('prices/', views.prices, name='prices'),
    path('technology/', views.technology, name='technology'),
    path('discounts/', views.discounts, name='discounts'),
    path('reviews/', views.reviews, name='reviews'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio/<slug:slug>/', views.portfolio_category, name='portfolio_category'),
    path('partners/', views.partners, name='partners'),
    path('contacts/', views.contacts, name='contacts'),
    path('api/reviews/', views.load_more_reviews, name='load_more_reviews'),
]
