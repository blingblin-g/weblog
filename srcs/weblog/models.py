from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from django.db import models
from django.utils import timezone
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks
from wagtail.images.models import Image

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

class BlogPage(Page):
    date = models.DateField("Post date", default=timezone.now)
    intro = models.CharField(max_length=250)
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    body_markdown = models.TextField(blank=True)
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('cover_image'),
        FieldPanel('body_markdown'),
        FieldPanel('body'),
    ] 