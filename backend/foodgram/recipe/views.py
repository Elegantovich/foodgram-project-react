from .models import Recipe, Ingredient, Tag, Favorite
from api.serializers import (RecipeSerializer, TagSerializer,
                             IngredientSerializer, FavouriteRecipeSerializer)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets, mixins, status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination
    queryset = Recipe.objects.all()
    lookup_field = 'pk'


class ListRetrieveViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class IngredientViewSet(ListRetrieveViewSet):
    serializer_class = IngredientSerializer
    pagination_class = LimitOffsetPagination
    queryset = Ingredient.objects.all()
    lookup_field = 'pk'


class TagViewSet(ListRetrieveViewSet):
    serializer_class = TagSerializer
    pagination_class = LimitOffsetPagination
    queryset = Tag.objects.all()
    lookup_field = 'pk'


class FavouriteViewSet(APIView):

    def post(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                'Recipe already exist in favorite list!',
                status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.create(user=user, recipe=recipe)
        serializer = FavouriteRecipeSerializer(recipe)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        favorite_obj = get_object_or_404(Favorite, user=user, recipe=recipe)
        if not favorite_obj:
            return Response(
                'Recipe is not found!',
                status=status.HTTP_400_BAD_REQUEST)
        favorite_obj.delete()
        return Response(
            'Recipe removed!', status=status.HTTP_204_NO_CONTENT)
