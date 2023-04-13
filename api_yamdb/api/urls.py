from django.urls import include, path
from rest_framework import routers

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

router = routers.DefaultRouter()
router.register('v1/categories', CategoryViewSet)
router.register('v1/genres', GenreViewSet)
router.register('v1/titles', TitleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
