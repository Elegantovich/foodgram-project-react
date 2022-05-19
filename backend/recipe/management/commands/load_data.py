import json

from django.core.management.base import BaseCommand
from recipe.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('data/ingredients.json', 'rb') as f:
            data = json.load(f)
            for i in data:
                Ingredient.objects.create(
                    name=i['name'],
                    measurement_unit=i['measurement_unit']
                )
                print(i['name'], i['measurement_unit'])
