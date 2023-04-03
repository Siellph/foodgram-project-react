import base64

from django.core.files.base import ContentFile
from django.db import transaction
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .users import UsersShowInfoSerializer


class ImageBase64Serializer(serializers.ImageField):
    """Кодирование изображения в base64"""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='photo.' + ext)
        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с ингредиентами"""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AddIngredientSerializer(serializers.ModelSerializer):
    """Добавление ингредиентов"""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Подробое описание ингредиентов в рецепте"""
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id',
        read_only=True
    )
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Создание рецепта. Проверяет игредиенты.
    Ответ возвращает в GetRecipeSerializer"""
    author = UsersShowInfoSerializer(read_only=True)
    image = ImageBase64Serializer()
    ingredients = AddIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'coocking_time')

    def validate(self, attrs):
        list_ingredients = [item['ingredient'] for item in attrs['ingredients']]
        all_ingredients, distinct_ingredients = (
            len(list_ingredients), len(str(list_ingredients))
        )
        if all_ingredients != distinct_ingredients:
            raise ValidationError(
                {'error': 'Ингредиенты должны быть уникальными'}
            )
        return attrs

    def get_ingredients(self, recipe, ingredients):
        RecipeIngredient.objects.bulk_create(
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient.get('ingredient'),
                amount=ingredient.get('amount')
            ) for ingredient in ingredients
        )

    @transaction.atomic
    def create(self, validated_data):
        return

    @transaction.atomic
    def update(self, instance, validated_data):
        return

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return GetRecipeSerializer(instance, context=context).data


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с тегами"""
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('__all__',)


class GetRecipeSerializer(serializers.ModelSerializer):
    """Отображение полной информации о рецепте"""



class FavoriteSerializer(serializers.ModelSerializer):
    """Добавление/удаление рецепта в/из избранного"""
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Добавление/удаление ингредиентов из рецепта в список покупок"""
    class Meta(FavoriteSerializer.Meta):
        model = ShoppingCart


class RecipeShowInfoSerializer(serializers.ModelSerializer):
    """Отображение основной информации о рецепте"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'coocking_time')
