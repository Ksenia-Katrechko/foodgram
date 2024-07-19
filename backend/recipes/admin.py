from django.contrib import admin
from .models import (Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag, Favorite)


class IngredientInRecipeInLine(admin.TabularInline):
    model = IngredientInRecipe
    fk_name = 'recipe'


class FavoriteInline(admin.TabularInline):
    model = Favorite
    fk_name = 'recipe'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'cooking_time',
        'total_favorites',
    )
    search_fields = ('name', 'author__username', 'tags__name')
    list_filter = ('tags',)
    empty_value_display = '-пусто-'
    inlines = [IngredientInRecipeInLine, FavoriteInline]

    def total_favorites(self, obj):
        return obj.favorites.count()
    total_favorites.short_description = 'Total Favorites'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
