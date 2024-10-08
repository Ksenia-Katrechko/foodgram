from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import User
from accounts.serializers import UserSerializer
from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)
from .utils import add_ingredients, get_is_obj

COOKING_TIME_MORE_ZERO = 'Время готовки должно быть больше нуля!'
FAVORITE_ADDED = 'Рецепт уже добавлен в избранное!'
INGREDIENT_ADDED = 'Ингредиент не должен повторяться!'
TAG_ADDED = 'Тег не должен повторяться!'
SHOPLIST_ADDED = 'Рецепт уже добавлен в список покупок!'
INGREDIENT_MORE_ZERO = 'Количество ингредиента должно быть больше 0!'
INGREDIENTS_EMPTY = 'Рецепт должен содержать хотя бы один ингредиент!'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='ingredient.id',
        read_only=True
    )
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True,)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_ingredients(self, obj):
        ingredients = IngredientInRecipe.objects.filter(recipe=obj)
        return IngredientInRecipeSerializer(ingredients, many=True).data

    def get_is_in_shopping_cart(self, obj):
        return get_is_obj(self, obj, ShoppingCart)

    def get_is_favorited(self, obj):
        return get_is_obj(self, obj, Favorite)


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    ingredients = IngredientInRecipeSerializer(many=True, read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'name',
            'image',
            'ingredients',
            'text',
            'cooking_time',
        )

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags', [])
        data_list = []
        if not ingredients:
            raise serializers.ValidationError(INGREDIENTS_EMPTY)
        # Валидация, которая не позволит создать рецепт без ингредиентов.
        for ingredient in ingredients:
            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError(INGREDIENT_MORE_ZERO)
            if ingredient in data_list:
                raise serializers.ValidationError(INGREDIENT_ADDED)
            else:
                data_list.append(ingredient)
        for tag in tags:
            if tag in data_list:
                raise serializers.ValidationError(TAG_ADDED)
            else:
                data_list.append(tag)
        if data['cooking_time'] <= 0:
            raise serializers.ValidationError(COOKING_TIME_MORE_ZERO)
        # Валидация, которая не позволит создать рецепт без времени.
        del data_list
        data['ingredients'] = ingredients
        data['tags'] = tags
        return data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        return add_ingredients(
            recipe,
            ingredients=ingredients,
        )

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        instance = add_ingredients(
            instance,
            ingredients=ingredients,
        )
        return super().update(instance, validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = (
            'id',
            'recipe',
            'user'
        )

    def validate(self, data):
        user = data['user']
        recipe_id = data['recipe'].id
        if Favorite.objects.filter(user=user, recipe__id=recipe_id).exists():
            raise ValidationError(FAVORITE_ADDED)
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ShoppingCart
        fields = (
            'id',
            'recipe',
            'user'
        )

    def validate(self, data):
        user = data['user']
        recipe_id = data['recipe'].id
        if ShoppingCart.objects.filter(
            user=user,
            recipe__id=recipe_id
        ).exists():
            raise ValidationError(SHOPLIST_ADDED)
        return data
