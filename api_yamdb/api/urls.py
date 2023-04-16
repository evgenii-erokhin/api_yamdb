from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                       CommentsViewSet, ReviewViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register('v1/categories', CategoryViewSet)
router_v1.register('v1/genres', GenreViewSet)
router_v1.register('v1/titles', TitleViewSet)
router_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments'
)
router_v1.register(r'v1/titles/(?P<title_id>\d+)reviews',
                   ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router_v1.urls)),
]
