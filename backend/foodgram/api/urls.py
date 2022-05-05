from django.urls import include, path
from djoser.views import TokenDestroyView
from recipe.views import (AddShoppingViewSet, FavouriteViewSet,
                          IngredientViewSet, RecipeViewSet, TagViewSet)
from rest_framework.routers import DefaultRouter
from user.views import FollowViewSet, RecieveToken, UserViewSet

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
    path('recipes/<int:recipe_id>/shopping_cart/',
         AddShoppingViewSet.as_view()),
    path('recipes/download_shopping_cart/',
         AddShoppingViewSet.as_view()),
    path('users/<int:user_id>/subscribe/',
         FollowViewSet.as_view()),
    path('users/subscriptions/',
         FollowViewSet.as_view()),
    path('', include(router.urls))
]
