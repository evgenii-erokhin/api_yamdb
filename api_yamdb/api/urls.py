from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments'
)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
