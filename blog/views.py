from django.shortcuts import render, get_object_or_404

from core.models import SiteSettings
from .models import BlogCategory, Post


def blog_list(request):
    settings = SiteSettings.objects.first()
    category_slug = request.GET.get('category')

    categories = BlogCategory.objects.all()
    posts = Post.objects.filter(is_published=True)

    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    context = {
        'settings': settings,
        'categories': categories,
        'posts': posts,
        'active_category': category_slug,
    }

    return render(request, 'blog/blog_list.html', context)


def post_detail(request, slug):
    settings = SiteSettings.objects.first()
    post = get_object_or_404(Post, slug=slug, is_published=True)

    # Related posts
    related = Post.objects.filter(
        is_published=True,
        category=post.category
    ).exclude(pk=post.pk)[:3]

    context = {
        'settings': settings,
        'post': post,
        'related': related,
    }

    return render(request, 'blog/post_detail.html', context)
