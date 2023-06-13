import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Load ingredients to DB"

    def handle(self, *args, **options):
        with open('C:/Рустам/Dev/foodgram-project-react/data/ingredients.csv',
                  encoding='utf-8') as fixture:
            reader = csv.reader(fixture)
            for row in reader:
                name, measurement_unit = row
                Ingredient.objects.get_or_create(
                    name=name, measurement_unit=measurement_unit)
