from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from weblog.models import BlogPage, BlogIndexPage
from wagtail.images.models import Image


class HomePage(Page):
    intro = RichTextField(blank=True)
    body = StreamField([
        ('markdown', blocks.TextBlock(help_text='Markdown text')),
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True, blank=True)
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='home_cover_images'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('cover_image'),
        FieldPanel('body'),
    ]

    def get_latest_posts(self):
        """최신 블로그 포스트 5개를 가져옵니다."""
        return BlogPage.objects.live().public().order_by('-date')[:5]

    def get_blog_indexes(self):
        """모든 블로그 인덱스 페이지를 가져옵니다."""
        return BlogIndexPage.objects.live().public()
