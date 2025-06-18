from django.shortcuts import render
from .models import BlogPage, BlogIndexPage

def blog_post_list(request):
    """블로그 포스트 목록을 보여주는 뷰"""
    if request.htmx:
        template_name = 'weblog/partials/blog_post_list.html'
    else:
        template_name = 'weblog/blog_post_list.html'
    
    blog_posts = BlogPage.objects.live().public().order_by('-date')
    return render(request, template_name, {'blog_posts': blog_posts})

def blog_post_detail(request, slug):
    """블로그 포스트 상세 페이지를 보여주는 뷰"""
    if request.htmx:
        template_name = 'weblog/partials/blog_post_detail.html'
    else:
        template_name = 'weblog/blog_post_detail.html'
    
    post = BlogPage.objects.get(slug=slug)
    return render(request, template_name, {'post': post}) 