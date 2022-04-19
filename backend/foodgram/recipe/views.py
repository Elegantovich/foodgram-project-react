from .models import Recipe, Ingredient, Tag, Favorite
from api.serializers import (RecipeSerializer, TagSerializer,
                             IngredientSerializer, FavouriteRecipeSerializer,
                             ShoppingListRecipeSerializer)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets, mixins, status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.http import HttpResponse


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


class AddShoppingViewSet(APIView):

    def get(self, request):
        buyer = request.user
        shopping_list = buyer.shopping_recipe.all()
        buying_list = {}

        for item_of_list in shopping_list:
            recipe = item_of_list.recipe
            ingredients = Recipe.objects.filter(recipe=recipe)
            for ingredient in ingredients:
                amount = ingredient.amount
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                if name not in buying_list:
                    buying_list[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount
                    }
                else:
                    buying_list[name]['amount'] = (buying_list[name]['amount']
                                                   + amount)
        wishlist = []
        for item in buying_list:
            wishlist.append(f'{item} - {buying_list[item]["amount"]} '
                            f'{buying_list[item]["measurement_unit"]} \n')
        wishlist.append('\n')
        wishlist.append('FoodGram, 2022')
        response = HttpResponse(wishlist, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="wishlist.txt"'
        return response

    def post(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                'Recipe already exist in shopping list!',
                status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.create(user=user, recipe=recipe)
        serializer = ShoppingListRecipeSerializer(recipe)
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

