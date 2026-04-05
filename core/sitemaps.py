from django.contrib.sitemaps import Sitemap

from services.models import Service
from blog.models import Post


class StaticPagesSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return [
            {'url': '/', 'priority': 1.0},
            {'url': '/about/', 'priority': 0.8},
            {'url': '/services/', 'priority': 0.9},
            {'url': '/blog/', 'priority': 0.7},
        ]

    def location(self, item):
        return item['url']


class ServiceSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Service.objects.filter(is_active=True)

    def location(self, obj):
        return f'/services/{obj.slug}/'


class PostSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_at

    def location(self, obj):
        return f'/blog/{obj.slug}/'
