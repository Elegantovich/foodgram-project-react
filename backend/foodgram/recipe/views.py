from .models import Recipe
from api.serializers import RecipeSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets
from rest_framework.permissions import AllowAny


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination
    queryset = Recipe.objects.all()
    lookup_field = 'pk'


