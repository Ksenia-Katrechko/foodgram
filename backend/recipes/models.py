from django.db import models
from accounts.models import User
from constants import DEFAULT_AMOUNT, MAX_LENGTH_NAME
# вынесла константы в отдельный файл


class Tag(models.Model):
    name = models.CharField(
        'название',
        unique=True,
        max_length=MAX_LENGTH_NAME,
        help_text='Название тега'
    )
    slug = models.SlugField(max_length=MAX_LENGTH_NAME)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'название',
        max_length=MAX_LENGTH_NAME,
        help_text='Название ингредиента'
    )
    measurement_unit = models.CharField(
        'единица измерения',
        max_length=MAX_LENGTH_NAME,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique_name_measurement_unit')
        ]
        # Проверки уникальности пары "название-единица измерения".

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        'название',
        max_length=MAX_LENGTH_NAME,
        help_text='Название рецепта'
    )
    text = models.TextField('текст', help_text='Здесь Ваш текст')
    pub_date = models.DateTimeField(
        'дата публикации', auto_now_add=True, db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор',
    )
    image = models.ImageField(
        upload_to='',
        blank=True, null=True,
        help_text='Можете загрузить картинку',
        verbose_name='картинка',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='теги',
        blank=True,
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',
        help_text='Время приготовления в минутах',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        related_name='recipes',
        verbose_name='ингредиент',
    )
    text = models.TextField('описание', help_text='Описание')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = 'Рецепты'
        verbose_name = 'Рецепт'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipe',
        verbose_name='Ингредиенты'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        default=DEFAULT_AMOUNT,
        verbose_name='Количество',
        help_text='Количество ингредиента',
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='favorite_unique')
        ]

    def __str__(self):
        return f'{self.ingredient}'


class UserRecipeRelation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='%(class)ss'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='%(class)ss'
    )

    class Meta:
        abstract = True
        ordering = ('recipe', 'user')
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_%(class)s'
            )
        ]

    def __str__(self):
        return f'{self.user}, {self.recipe}'

# Создала базовую модель и наследовала для Favorite, ShoppingCart


class Favorite(UserRecipeRelation):
    class Meta(UserRecipeRelation.Meta):
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        default_related_name = 'favorites'
        #  использовала default_related_name в классе меты дочернего класса


class ShoppingCart(UserRecipeRelation):
    class Meta(UserRecipeRelation.Meta):
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        default_related_name = 'shopping_carts'
        #  использовала default_related_name в классе меты дочернего класса
