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
    path('partners/', views.partners_list, name='partners'),
    path('contacts/', views.contacts, name='contacts'),
    path('api/reviews/', views.load_more_reviews, name='load_more_reviews'),
    path('api/partners/<int:partner_id>/works/', views.get_partner_works, name='api_partner_works'),
    path('notice/', views.notice_page, name='notice'),
    path('info/<slug:slug>/', views.legal_page_detail, name='legal_detail'),
]
