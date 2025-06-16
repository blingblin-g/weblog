from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from search import views as search_views
from weblog import views as weblog_views

app_name = 'weblog'

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("blog/", include("weblog.weblog.urls")),  # 앱의 urls.py를 include
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("", include(wagtail_urls)),
]

urlpatterns += [
    path('', weblog_views.blog_post_list, name='blog_post_list'),
    path('<slug:slug>/', weblog_views.blog_post_detail, name='blog_post_detail'),
]
