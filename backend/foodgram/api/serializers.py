from recipe.models import User, Recipe, Tag, Ingredient, ShoppingList, Follow
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'password')
        model = User


class UserRetrieveSerializer(UserSerializer):

    class Meta:
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
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


class PasswordSerializer(UserSerializer):

    class Meta:
        fields = ('id', 'password')
        model = User


class RecipeSerializer(serializers.ModelSerializer):

    author = UserSerializer()

    class Meta:
        fields = '__all__'
        model = Recipe


class RecipeSerializer2(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class ShowFollowsSerializer(UserSerializer):

    recipes = RecipeSerializer2(many=True)
    recipes_count = serializers.SerializerMethodField()

    def get_recipes_count(self, obj):
        all_recipes = Recipe.objects.filter(author=obj.id)
        return all_recipes.count()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'recipes', 'recipes_count')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class FavouriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingListRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')