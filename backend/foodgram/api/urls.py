from django.urls import include, path
from rest_framework.routers import DefaultRouter
from djoser.views import TokenDestroyView
from user.views import RecieveToken, UserViewSet
from recipe.views import (RecipeViewSet, IngredientViewSet, TagViewSet,
                          FavouriteViewSet)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('auth/token/login/', RecieveToken.as_view()),
    path('auth/token/logout/', TokenDestroyView.as_view()),
    path('recipes/<int:recipe_id>/favorite/',
         FavouriteViewSet.as_view()),
    path('', include(router.urls))
]
