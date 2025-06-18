from django.urls import path
from . import views

app_name = 'weblog'

urlpatterns = [
    path('tag/<slug:tag>/', views.tag_view, name='tag'),
    path('like/<int:page_id>/', views.toggle_like, name='toggle_like'),
] 