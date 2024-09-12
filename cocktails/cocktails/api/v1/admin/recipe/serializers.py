from rest_framework import serializers
from apps.recipe.models import *
from django.db import transaction


__all__ = [
    'AdminIngredientCategorySerializer',
    'AdminIngredientSerializer',
    'AdminViewToolSerializer',
    'AdminToolSerializer',
    'AdminUpdateRecipeSerializer',
    'AdminListRecipeIngredientSerializer',
    'AdminRecipeIngredientSerializer',
    'AdminCreateRecipeSerializer',
    'AdminRecipeSerializer',
]


class AdminRecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.SerializerMethodField()

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'name', 'quantity', 'type']

    def get_name(self, obj):
        return obj.ingredient.name


class AdminListRecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.IntegerField(source='ingredient.name')
    count = serializers.CharField(source='quantity')
    type = serializers.CharField()

    class Meta:
        model = RecipeIngredient
        fields = ['name', 'count', 'type']


class AdminIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class AdminIngredientCategorySerializer(serializers.ModelSerializer):
    ingredients = AdminIngredientSerializer(many=True, read_only=True)

    class Meta:
        model = IngredientCategory
        fields = '__all__'


class AdminViewToolSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tool
        fields = '__all__'


class AdminToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = '__all__'


class AdminCreateRecipeSerializer(serializers.ModelSerializer):
    ingredients = AdminRecipeIngredientSerializer(source='recipe_ingredients', many=True)
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


class AdminUpdateRecipeSerializer(serializers.ModelSerializer):
    ingredients = AdminRecipeIngredientSerializer(source='recipe_ingredients', many=True)

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


class AdminRecipeSerializer(serializers.ModelSerializer):
    ingredient_count = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()
    tools = AdminViewToolSerializer(many=True)
    image = serializers.ImageField(source='photo', allow_null=True, required=False)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_ingredient_count(self, obj):
        return obj.recipe_ingredients.count()

    def get_ingredients(self, obj):
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return AdminRecipeIngredientSerializer(recipe_ingredients, many=True).data