from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from wagtail.models import Page
from .models import BlogPage, Tag

def tag_view(request, tag):
    tag = Tag.objects.get(slug=tag)
    posts = BlogPage.objects.live().public().filter(tags__name=tag.name)
    
    return render(request, 'weblog/tag_index_page.html', {
        'tag': tag,
        'posts': posts,
    })

def toggle_like(request, page_id):
    """좋아요 토글 처리"""
    if request.method == 'POST':
        page = get_object_or_404(BlogPage, id=page_id)
        ip_address = request.META.get('REMOTE_ADDR')
        
        is_liked = page.toggle_like(ip_address)
        
        return JsonResponse({
            'success': True,
            'is_liked': is_liked,
            'like_count': page.like_count
        })
    return JsonResponse({'success': False}, status=400) 