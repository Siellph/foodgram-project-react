from recipes.models import Recipe
from rest_framework import serializers


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Создание рецепта"""


class RecipeShowInfoSerializer(serializers.ModelSerializer):
    """Отображение основной информации о рецепте"""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'coocking_time'
            )
