from django.db import models
from django.utils import timezone
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index

# Create your models here.


# 블로그 태그 모델
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage", related_name="tagged_items", on_delete=models.CASCADE
    )


# 블로그 인덱스 페이지 모델
class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    def get_context(self, request):
        # 컨텍스트 업데이트
        context = super().get_context(request)
        # 자식 페이지(블로그 게시물)를 날짜 역순으로 가져옴
        blogpages = self.get_children().live().order_by("-first_published_at")
        context["blogpages"] = blogpages
        return context


# 블로그 페이지 모델
class BlogPage(Page):
    date = models.DateTimeField("게시일", default=timezone.now)
    intro = models.CharField("소개", max_length=250)
    body = RichTextField("내용")
    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="썸네일 이미지",
    )
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("thumbnail"),
        FieldPanel("body"),
        FieldPanel("tags"),
    ]
