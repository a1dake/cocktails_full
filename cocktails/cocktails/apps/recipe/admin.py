from django.contrib import admin
from apps.recipe.models import *
from base.admin import BaseAdmin


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    fields = ('ingredient', 'quantity', 'type')
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'


@admin.register(Recipe)
class RecipeAdmin(BaseAdmin):
    fieldsets = (
        (None, {'fields': ('title', 'isEnabled', 'user', 'moderation_status')}),
        ('Информация', {'fields': ('video_url', 'description', 'instruction')}),
        ('Ингредиенты/Инструменты', {'fields': ('tools', )}),
    )
    list_filter = (
        'isEnabled',
        'moderation_status'
    )
    list_display = ('id', 'title', 'user', 'isEnabled', 'moderation_status', 'description', 'instruction', 'video_url')
    search_fields = ('title', 'user__username', 'user__email', 'user__phone')
    ordering = ('id',)
    inlines = [RecipeIngredientInline]

    change_list_template = 'admin/user_profile_change_list.html'


@admin.register(IngredientCategory)
class IngredientCategoryAdmin(BaseAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('id',)


@admin.register(Ingredient)
class IngredientAdmin(BaseAdmin):
    list_filter = (
        'category__name',
        'is_alcoholic'
    )
    list_display = ('id', 'name', 'description', 'category', 'is_alcoholic')
    search_fields = ('name', 'category__name')
    ordering = ('id',)


@admin.register(Tool)
class ToolAdmin(BaseAdmin):
    list_filter = ('name',)
    list_display = ('id', 'name', 'description', 'history', 'how_to_use', 'photo', 'links', 'get_recipes')
    search_fields = ('name',)
    ordering = ('id', )

    def get_recipes(self, obj):
        return [recipe.title for recipe in obj.recipes_tool.all()]
    get_recipes.short_description = 'Recipes'


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(BaseAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user__username', 'recipe__title')
    ordering = ('id',)
