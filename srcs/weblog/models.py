from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from django.db import models
from django.utils import timezone
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks
from wagtail.images.models import Image
from taggit.models import Tag as TaggitTag
from taggit.managers import TaggableManager
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Tag(TaggitTag):
    class Meta:
        proxy = True

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('cover_image'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        blogpages = self.get_children().specific().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

class BlogPage(Page):
    date = models.DateField("Post date", default=timezone.now)
    intro = models.CharField(max_length=250)
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='blog_pages'
    )
    tags = TaggableManager(blank=True)
    view_count = models.PositiveIntegerField(default=0, verbose_name="조회수")
    like_count = models.PositiveIntegerField(default=0, verbose_name="좋아요 수")
    liked_ips = models.JSONField(default=list, blank=True, verbose_name="좋아요한 IP 목록")
    body = StreamField([
        ('markdown', blocks.TextBlock(help_text='Markdown text')),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('cover_image'),
        FieldPanel('category'),
        FieldPanel('tags'),
        FieldPanel('body'),
        FieldPanel('view_count'),
        FieldPanel('like_count'),
    ]

    def serve(self, request, *args, **kwargs):
        # 조회수 증가
        self.view_count += 1
        self.save()
        return super().serve(request, *args, **kwargs)

    def toggle_like(self, ip_address):
        """좋아요 토글 기능"""
        if ip_address in self.liked_ips:
            # 이미 좋아요를 누른 경우, 좋아요 취소
            self.liked_ips.remove(ip_address)
            self.like_count = max(0, self.like_count - 1)
            is_liked = False
        else:
            # 좋아요를 누르지 않은 경우, 좋아요 추가
            self.liked_ips.append(ip_address)
            self.like_count += 1
            is_liked = True
        self.save()
        return is_liked

class HomePage(Page):
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    intro = models.TextField(blank=True)

    page_ptr = models.OneToOneField(
        Page, on_delete=models.CASCADE, parent_link=True, related_name='weblog_homepage'
    )

    content_panels = Page.content_panels + [
        FieldPanel('cover_image'),
        FieldPanel('intro'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        # Get all categories
        context['categories'] = Category.objects.all()
        
        # Get recent posts
        context['recent_posts'] = BlogPage.objects.live().order_by('-first_published_at')[:5]
        
        return context 