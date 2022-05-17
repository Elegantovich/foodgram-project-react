import recipe.models as models
from django.contrib import admin

LIST_MODELS = [
    models.Recipe,
    models.Ingredient,
    models.IngredientRecipe,
    models.Tag,
    models.TagRecipe
]

admin.site.register(LIST_MODELS)
