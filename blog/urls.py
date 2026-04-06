from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/tag/<slug:slug>/', views.tag_posts, name='tag_posts'),
    path('blog/<slug:slug>/', views.post_detail, name='post_detail'),
]
