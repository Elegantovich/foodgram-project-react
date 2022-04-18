from django.urls import include, path
from rest_framework.routers import DefaultRouter
from djoser.views import TokenDestroyView
from user.views import (RecieveToken, UserViewSet)
from recipe.views import RecipeViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('recipes', RecipeViewSet)
"""
router.register('categories', CategoryViewSet)
router.register('genres', GenresViewSet)
router.register(
    r'titles/(?P<title_id>[\d+]+)/reviews/(?P<review_id>[\d+]+)/comments',
    CommentViewSet,
    basename='comments'
)"""

urlpatterns = [
    path('auth/token/login/', RecieveToken.as_view()),
    path('auth/token/logout/', TokenDestroyView.as_view()),
    path('', include(router.urls))
]
