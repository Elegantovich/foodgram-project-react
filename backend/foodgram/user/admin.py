import recipe.models as models
from django.contrib import admin

LIST_MODELS = [
    models.User
]

admin.site.register(LIST_MODELS)
