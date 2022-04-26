from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    username = models.CharField(
        unique=True,
        max_length=30,
        verbose_name='Login of user'
        )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Email post adress'
        )
    first_name = models.CharField(
        max_length=100,
        verbose_name='Name of user'
        )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Surname of user'
        )
    password = models.CharField(
        verbose_name='Password of account',
        max_length=100
        )

    User = 'user'
    Admin = 'admin'

    ROLES = (
        (User, 'user'),
        (Admin, 'admin')
    )

    role = models.CharField(
        choices=ROLES,
        default='user',
        max_length=5,
        verbose_name='Статус',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Name'
        )
    color = models.CharField(
        max_length=50,
        verbose_name='hex-code of color'
        )
    slug = models.SlugField(
        verbose_name='Slug of tag'
        )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Name of ingredient'
        )
    units_measurement = models.CharField(
        max_length=50,
        verbose_name='Units of measurement',
        )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Author'
        )
    name = models.CharField(
        max_length=50,
        verbose_name='Name of Recipe'
        )
    image = models.ImageField(
        verbose_name='Image of recipe'
        )
    description = models.TextField(
        verbose_name='Description'
        )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        related_name='recipes',
        verbose_name='Ingredients for recipe'
        )
    tag = models.ForeignKey(  # Вспомнить форматы связей
        Tag,
        max_length=50,
        verbose_name='Tag',
        on_delete=models.CASCADE,  # Вспомнить форматы удаления
        related_name='recipes'
        )
    cooking_time = models.IntegerField(
        verbose_name='Time of cooking'
        )  # Настроить формат в минутах

    def __str__(self):
        return self.name


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Подсписчик',
        related_name='follower'
        )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Автор',
        related_name='following')


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ingredient in Recipe'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Recipe'
    )
    quantity = models.IntegerField(
        verbose_name='Quantity of ingredients'
    )

    def __str__(self):
        return f'{self.ingredient} in {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite_subscriber",
        verbose_name='Пользователь'
        )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorite_recipe",
        verbose_name='Рецепт'
        )


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_recipe",
        verbose_name='Покупатель'
        )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="buyers",
        verbose_name='Рецепт'
        )
