from django.urls import path
from . import views

app_name = 'weblog'

urlpatterns = [
    path('', views.blog_post_list, name='blog_post_list'),
    path('<slug:slug>/', views.blog_post_detail, name='blog_post_detail'),
]
