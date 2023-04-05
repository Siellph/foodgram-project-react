import base64

from django.core.files.base import ContentFile
from django.db import transaction
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .users import UsersInfoSerializer


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
    author = UsersInfoSerializer(read_only=True)
    image = ImageBase64Serializer()
    ingredients = AddIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'coocking_time')

    def validate(self, attrs):
        list_ingredients = [
            item['ingredient'] for item in attrs['ingredients']
        ]
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
        user = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            author=user,
            **validated_data
        )
        recipe.tags.set(tags)
        self.get_ingredients(recipe, ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        RecipeIngredient.objects.filter(recipe=instance).delete()
        instance.tags.set(tags)
        self.get_ingredients(instance, ingredients)
        return super().update(instance, validated_data)

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
    tags = TagSerializer(many=True)
    author = UsersInfoSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        read_only=True,
        many=True,
        source='recipe_ingredient'
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'coocking_time')

    def get_is_favorited(self, object):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return object.favorite.filter(user=user).exists()

    def get_is_in_shopping_cart(self, object):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return object.shopping_cart.filter(user=user).exists()


class FavoriteSerializer(serializers.ModelSerializer):
    """Добавление/удаление рецепта в/из избранного"""
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        user, recipe = data.get('user'), data.get('recipe')
        if self.Meta.model.objects.filter(user=user, recipe=recipe).exists():
            raise ValidationError({'error': 'Этот рецепт уже добавлен'})
        return data

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return RecipeShowInfoSerializer(instance.recipe, context=context).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Добавление/удаление ингредиентов из рецепта в список покупок"""
    class Meta(FavoriteSerializer.Meta):
        model = ShoppingCart


class RecipeShowInfoSerializer(serializers.ModelSerializer):
    """Отображение основной информации о рецепте"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'coocking_time')
