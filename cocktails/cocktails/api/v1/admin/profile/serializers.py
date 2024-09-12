from rest_framework import serializers
from apps.user.models import *
from apps.recipe.models import *
from api.v1.recipe.serializers import RecipeDetailSerializer

__all__ = [
    'AdminUserRecipeSerializer',
    'AdminPointSerializer',
    'AdminReferralSerializer',
    'AdminUserSerializer',
    'AdminFavoriteRecipeSerializer',
    'AdminUserListSerializer'
]


class AdminUserRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class AdminPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['points']


class AdminReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = '__all__'


class AdminFavoriteRecipeSerializer(serializers.ModelSerializer):
    recipe = RecipeDetailSerializer()

    class Meta:
        model = FavoriteRecipe
        fields = ['recipe']


class AdminUserSerializer(serializers.ModelSerializer):
    points = AdminPointSerializer(many=True, read_only=True)
    referral = AdminReferralSerializer(many=True, read_only=True)
    recipes = AdminUserRecipeSerializer(many=True, read_only=True)
    favorite = AdminFavoriteRecipeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class AdminUserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'