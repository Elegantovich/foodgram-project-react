from recipe.models import User, Recipe, Tag, Ingredient
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'password')
        model = User


class AuthSerializer(UserSerializer):

    class Meta:
        fields = ('password', 'email')
        model = User


class UserRoleSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role')
        model = User


class TokenSerializer(UserSerializer):

    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password')


class PasswordSerializer(AuthSerializer):

    class Meta:
        fields = ('id', 'new_password', 'current_password')
        model = User


class RecipeSerializer(serializers.ModelSerializer):

    author = UserSerializer()

    class Meta:
        fields = '__all__'
        model = Recipe


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        exclude = ('quantity', )


class FavouriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
