from rest_framework.response import Response
from wagtail.api.v2.filters import FieldsFilter, OrderingFilter, SearchFilter
from wagtail.api.v2.views import PagesAPIViewSet

from .models import BlogPage


class BlogPageAPIViewSet(PagesAPIViewSet):
    """
    블로그 페이지를 위한 API 뷰셋
    """

    model = BlogPage

    # 필터 정의
    filter_backends = [
        FieldsFilter,
        OrderingFilter,
        SearchFilter,
    ]

    # 검색 필드
    search_fields = ["title", "intro", "body", "tags"]

    # 정렬 필드
    ordering_fields = ["title", "date", "first_published_at"]

    # 기본 필드
    meta_fields = ["slug", "first_published_at"]

    # 상세 필드
    body_fields = ["title", "date", "intro", "body", "tags"]

    # 블로그 글 목록
    def listing_view(self, request):
        queryset = self.get_queryset()
        self.check_query_parameters(queryset)

        # 검색 필터 적용
        queryset = self.filter_queryset(queryset)

        # 페이지네이션 적용
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # 개별 블로그 글 상세 보기
    def detail_view(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
