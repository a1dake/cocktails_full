from rest_framework import serializers
from apps.recipe.models import *
from apps.recipe.models import FavoriteRecipe
from django.db import transaction


__all__ = [
    'SelectionRecipeSerializer',
    'IngredientCategorySerializer',
    'IngredientSerializer',
    'ViewToolSerializer',
    'ToolSerializer',
    'UpdateRecipeSerializer',
    'ListRecipeIngredientSerializer',
    'RecipeIngredientSerializer',
    'CreateRecipeSerializer',
    'RecipeDetailSerializer',
    'RecipeListSerializer',
]


class SelectionRecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_ingredients(self, obj):
        ingredients = obj.recipe_ingredients.all()
        return [
            {
                'id': ingredient.ingredient.id,
                'name': ingredient.ingredient.name,
                'quantity': ingredient.quantity,
                'type': ingredient.type
            }
            for ingredient in ingredients
        ]


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.SerializerMethodField()

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'name', 'quantity', 'type']

    def get_name(self, obj):
        return obj.ingredient.name


class ListRecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.IntegerField(source='ingredient.name')
    count = serializers.CharField(source='quantity')
    type = serializers.CharField()

    class Meta:
        model = RecipeIngredient
        fields = ['name', 'count', 'type']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientCategorySerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = IngredientCategory
        fields = '__all__'


class ViewToolSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = Tool
        fields = '__all__'

    def get_recipes(self, obj):
        return [recipe.title for recipe in obj.recipes_tool.all()]


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = '__all__'


class CreateRecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(source='recipe_ingredients', many=True)
    tools = serializers.PrimaryKeyRelatedField(queryset=Tool.objects.all(), many=True, write_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients')
        tools_data = validated_data.pop('tools', [])
        with transaction.atomic():
            recipe = Recipe.objects.create(**validated_data)

            for ingredient_data in ingredients_data:
                ingredient = ingredient_data['ingredient']
                if not ingredient:
                    raise serializers.ValidationError(f"Ingredient with id {ingredient_id} does not exist.")
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=ingredient_data['quantity'],
                    type=ingredient_data['type']
                )

            if tools_data:
                recipe.tools.set(tools_data)

        return recipe


class UpdateRecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(source='recipe_ingredients', many=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients')
        instance = super().update(instance, validated_data)

        instance.recipe_ingredients.all().delete()

        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.create(
                recipe=instance,
                ingredient_id=ingredient_data['ingredient']['id'],
                quantity=ingredient_data['quantity'],
                type=ingredient_data['type']
            )

        return instance


class RecipeDetailSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    tools = ToolSerializer(many=True)
    user = serializers.StringRelatedField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request is None:
            raise KeyError('request')
        user = request.user
        if user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(user=user, recipe=obj).exists()


class RecipeListSerializer(serializers.ModelSerializer):
    ingredient_count = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()
    tools = ToolSerializer(many=True)
    is_favorite = serializers.SerializerMethodField()
    image = serializers.ImageField(source='photo', allow_null=True, required=False)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(user=user, recipe=obj).exists()

    def get_ingredient_count(self, obj):
        return obj.recipe_ingredients.count()

    def get_ingredients(self, obj):
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(recipe_ingredients, many=True).data