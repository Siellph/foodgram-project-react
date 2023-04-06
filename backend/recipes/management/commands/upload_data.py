import csv
from foodgram import settings
from django.core.management import BaseCommand
from recipes.models import Ingredient, Tag

MODELS_FILES = {
    Ingredient: 'ingredients.csv',
    Tag: 'tags.csv'
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        for model, file in MODELS_FILES.items():
            with open(f'{settings.BASE_DIR}/data/{file}',
                      encoding='utf-8') as table:
                reader = csv.DictReader(table)
                model.objects.bulk_create(model(**data) for data in reader)
            self.stdout.write(self.style.SUCCESS(
                f'=== {file} успешно загружен ===')
            )
        self.stdout.write(self.style.SUCCESS('=== Загрузка завершена ==='))
