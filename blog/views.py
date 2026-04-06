from django.shortcuts import render, get_object_or_404
from django.db.models import F

from core.models import SiteSettings
from .models import BlogCategory, Post, Tag


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


def tag_posts(request, slug):
    settings = SiteSettings.objects.first()
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(is_published=True, tags=tag)
    
    categories = BlogCategory.objects.all()

    context = {
        'settings': settings,
        'tag': tag,
        'posts': posts,
        'categories': categories,
    }

    return render(request, 'blog/blog_list.html', context)


def post_detail(request, slug):
    settings = SiteSettings.objects.first()
    post = get_object_or_404(Post, slug=slug, is_published=True)

    # Increment views
    Post.objects.filter(pk=post.pk).update(views=F('views') + 1)
    post.refresh_from_db()

    # Related posts (from same category)
    related = Post.objects.filter(
        is_published=True,
        category=post.category
    ).exclude(pk=post.pk)[:3]
    
    # If not enough related in current category, get from others
    if related.count() < 3:
        more_related = Post.objects.filter(
            is_published=True
        ).exclude(pk__in=[post.pk] + [p.pk for p in related]).order_by('?')[:3 - related.count()]
        related = list(related) + list(more_related)

    faqs = post.faqs.all()

    context = {
        'settings': settings,
        'post': post,
        'related': related,
        'faqs': faqs,
    }

    return render(request, 'blog/post_detail.html', context)
