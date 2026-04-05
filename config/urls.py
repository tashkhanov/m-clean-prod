from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from core.sitemaps import StaticPagesSitemap, ServiceSitemap, PostSitemap
from core.views import maintenance

sitemaps = {
    'static': StaticPagesSitemap,
    'services': ServiceSitemap,
    'posts': PostSitemap,
}


def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Disallow: /admin/\n"
        "Disallow: /api/\n"
        "\n"
        "Sitemap: https://m-clean.kz/sitemap.xml\n"
    )
    return HttpResponse(content, content_type='text/plain')


urlpatterns = [
    path('admin/maintenance/', maintenance, name='admin_maintenance'),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('services.urls')),
    path('', include('leads.urls')),
    path('', include('blog.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
