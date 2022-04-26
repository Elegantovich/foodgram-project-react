import recipe.models as models
from django.contrib import admin

LIST_MODELS = [
    models.Recipe,
    models.Ingredient,
    models.Tag,
    models.IngredientInRecipe
]

admin.site.register(LIST_MODELS)
