from django.contrib.admin import (ModelAdmin, TabularInline, display, register,
                                  site)
from django.utils.html import format_html
from recipes.forms import TagForm
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)

site.site_header = 'Администрирование Foodgram'
EMPTY_VALUE_DISPLAY = 'Значение не указано'


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    save_on_top = True
    empty_value_display = EMPTY_VALUE_DISPLAY


class IngredientInline(TabularInline):
    model = RecipeIngredient
    extra = 2


@register(Tag)
class TagAdmin(ModelAdmin):
    form = TagForm
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'color')
    save_on_top = True
    empty_value_display = EMPTY_VALUE_DISPLAY

    @display(description='Colored')
    def color(self, obj: Tag):
        return format_html(
            '<span style="color: #{};">{}</span>',
            obj.color[1:], obj.color
        )

    color.short_description = 'Цветовой код тэга'


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'author', 'pub_date', 'display_tags', 'favorite')
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author', 'tags')
    readonly_fields = ('favorite',)
    fields = ('image',
              ('name', 'author'),
              'text',
              ('tags', 'cooking_time'),
              'favorite')
    inlines = (IngredientInline,)
    save_on_top = True
    empty_value_display = EMPTY_VALUE_DISPLAY

    def display_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])
    display_tags.short_description = 'Теги'

    def favorite(self, obj):
        return obj.favorite.count()
    favorite.short_description = 'Раз в избранном'


@register(RecipeIngredient)
class RecipeIngredientAdmin(ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('recipe', 'user')


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ('recipe', 'user')
