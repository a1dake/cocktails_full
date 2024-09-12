from rest_framework import serializers
from apps.user.models import *
from apps.recipe.models import *
from api.v1.recipe.serializers import RecipeDetailSerializer

__all__ = [
    'UserRecipeSerializer',
    'PointSerializer',
    'ReferralSerializer',
    'UserSerializer',
    # 'NotificationSerializer',
    'FavoriteRecipeSerializer'
]


class UserRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['points']


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = '__all__'


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    recipe = RecipeDetailSerializer()

    class Meta:
        model = FavoriteRecipe
        fields = ['recipe']


class UserSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)
    favorite_recipes_count = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_favorite_recipes_count(self, obj):
        return obj.favorite_recipes.count()

    def get_recipes_count(self, obj):
        return obj.recipes_user.count()


# class NotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notification
#         fields = '__all__'
