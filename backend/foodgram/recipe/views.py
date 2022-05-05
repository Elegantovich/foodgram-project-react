from api.permissions import AdminOrReadOnly, AdminUserOrReadOnly
from api.serializers import (FavouriteRecipeSerializer, IngredientSerializer,
                             RecipeSerializer, ShoppingListRecipeSerializer,
                             TagSerializer)
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingList, Tag)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    queryset = Recipe.objects.all()
    lookup_field = 'pk'

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AdminUserOrReadOnly]
        return [permission() for permission in permission_classes]


class ListRetrieveViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class IngredientViewSet(ListRetrieveViewSet):
    permission_classes = (AdminOrReadOnly,)
    serializer_class = IngredientSerializer
    pagination_class = PageNumberPagination
    queryset = Ingredient.objects.all()
    lookup_field = 'pk'


class TagViewSet(ListRetrieveViewSet):
    serializer_class = TagSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AdminUserOrReadOnly]
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
        user = request.user
        shopping_list = user.shopping_recipe.all()
        buy_list = {}
        for item_of_list in shopping_list:
            recipe = item_of_list.recipe
            ingredients = IngredientInRecipe.objects.filter(recipe=recipe)
            for ingredient in ingredients:
                quantity = ingredient.quantity
                name = ingredient.ingredient.name
                units_measurement = ingredient.ingredient.units_measurement
                if name not in buy_list:
                    buy_list[name] = {
                        'units_measurement': units_measurement,
                        'quantity': quantity
                    }
                else:
                    buy_list[name]['quantity'] = (buy_list[name]['quantity']
                                                  + quantity)

        wishlist = []
        for item in buy_list:
            wishlist.append(f'{item} - {buy_list[item]["quantity"]}'
                            f'{buy_list[item]["units_measurement"]}\n')
        response = HttpResponse(wishlist)
        return response

    def post(self, request, recipe_id):
        user = request.user
        print(user, recipe_id)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                'Recipe already exist in shopping list!',
                status=status.HTTP_400_BAD_REQUEST)
        ShoppingList.objects.create(user=user, recipe=recipe)
        serializer = ShoppingListRecipeSerializer(recipe)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        shopping_obj = get_object_or_404(ShoppingList, user=user,
                                         recipe=recipe)
        if not shopping_obj:
            return Response(
                'Recipe is not found!',
                status=status.HTTP_400_BAD_REQUEST)
        shopping_obj.delete()
        return Response(
            'Recipe removed!', status=status.HTTP_204_NO_CONTENT)
