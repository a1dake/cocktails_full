import logging
from django.db import models
from apps.user.models import User
from base.fields import *
from base.models import BaseModel, CreatedUpdatedModel
from django.contrib.postgres.fields import ArrayField


__all__ = [
    'IngredientCategory',
    'Ingredient',
    'Tool',
    'Recipe',
    'FavoriteRecipe',
    'RecipeIngredient',
]

logger = logging.getLogger(__name__)


class IngredientCategory(CreatedUpdatedModel):
    name = models.CharField(max_length=255, unique=True, db_index=True, verbose_name='Название категории')

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория ингредиента'
        verbose_name_plural = 'Категории ингредиентов'

    def __str__(self):
        return self.name


class Ingredient(CreatedUpdatedModel):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    category = models.ForeignKey(
        IngredientCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ingredients',
        verbose_name='Категория'
    )
    is_alcoholic = models.BooleanField(default=False, verbose_name='Алкогольный?')

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tool(CreatedUpdatedModel):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    history = models.TextField(null=True, blank=True, verbose_name='История')
    how_to_use = models.TextField(null=True, blank=True, verbose_name='Как использовать')
    photo = models.ImageField(upload_to='tool_photos/', null=True, blank=True, verbose_name='Фото')
    links = ArrayField(models.URLField(), null=True, blank=True, verbose_name='Ссылки')

    class Meta:
        ordering = ['id']
        verbose_name = 'Инструмент'
        verbose_name_plural = 'Инструменты'

    def __str__(self):
        return '{}'.format(self.name)


class Recipe(BaseModel):
    MODERATION_STATUS_CHOICES = [
        ('Draft', 'Черновик'),
        ('Pending', 'На модерации'),
        ('Approved', 'Одобрено'),
        ('Rejected', 'Отклонено'),
        ('Archive', 'Архив')
    ]

    title = models.CharField(max_length=255, db_index=True, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    instruction = models.JSONField(null=True, blank=True, verbose_name='Инструкция')
    isEnabled = models.BooleanField(default=False, verbose_name='Доступен?')
    photo = models.ImageField(upload_to='recipes/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes_user', verbose_name='Пользователь')
    tools = models.ManyToManyField(Tool, blank=True, related_name='recipes_tool', verbose_name='Инструменты')

    moderation_status = models.CharField(
        max_length=10,
        choices=MODERATION_STATUS_CHOICES,
        default='Draft',
        verbose_name='Статус модерации'
    )

    video_url = models.URLField(null=True, blank=True, verbose_name='Ссылка на видео')

    class Meta:
        ordering = ['id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return '{}'.format(self.title)


class RecipeIngredient(models.Model):
    TYPES = [
        ('ml', 'мл'),
        ('l', 'л'),
        ('tsp', 'ч. л.'),
        ('tbsp', 'ст. л.'),
        ('cup', 'ст.'),
        ('pt', 'пинта'),
        ('qt', 'кварта'),
        ('gal', 'галлон'),
        ('fl oz', 'унция жидкостная'),
        ('mg', 'мг'),
        ('g', 'г'),
        ('kg', 'кг'),
        ('t', 'т'),
        ('oz', 'унция'),
        ('lb', 'фунт'),
    ]
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredient_recipes')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Количество')
    type = models.CharField(
        max_length=10,
        choices=TYPES,
        default='ml',
        verbose_name='Мера'
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f'{self.quantity} of {self.ingredient.name} in {self.recipe.title}'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'