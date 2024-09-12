from rest_framework import status
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import *
from base.pagination import BasePagination
from rest_framework.permissions import AllowAny
from .swagger import *
from apps.recipe.models import *
from django.db.models import Count, Q
from drf_yasg.utils import swagger_auto_schema
from .filters import RecipeFilterSet


class IngredientCategoryViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = IngredientCategory.objects.prefetch_related('ingredients')
    serializer_class = IngredientCategorySerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(**ingredient_category_list)
    def list(self, request, *args, **kwargs):
        self.serializer_class = IngredientCategorySerializer
        return super().list(request, *args, **kwargs)


class IngredientViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(**ingredient_retrieve)
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = IngredientSerializer
        return super().retrieve(request, *args, **kwargs)


class ToolViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Tool.objects.all()
    serializer_class = ViewToolSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(**tool_list)
    def list(self, request, *args, **kwargs):
        self.serializer_class = ViewToolSerializer
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(**tool_retrieve)
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ViewToolSerializer
        return super().retrieve(request, *args, **kwargs)


class RecipeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Recipe.objects.filter(isEnabled=True)
    permission_classes = [AllowAny]
    pagination_class = BasePagination
    serializer_class = RecipeListSerializer
    filterset_class = RecipeFilterSet

    @swagger_auto_schema(**recipe_list)
    def list(self, request, *args, **kwargs):
        # queryset = self.get_queryset()
        # query = request.query_params.get('query', '')
        # if query:
        #     queryset = queryset.filter(
        #         Q(title__icontains=query) |
        #         Q(recipe_ingredients__ingredient__name__icontains=query)
        #     ).distinct()
        #
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = RecipeListSerializer(page, many=True, context={'request': request})
        #     return self.get_paginated_response(serializer.data)
        #
        # serializer = RecipeListSerializer(queryset, many=True, context={'request': request})
        # return Response(serializer.data)
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(**recipe_update)
    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = UpdateRecipeSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @swagger_auto_schema(**recipe_delete)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(**recipe_selection)
    @action(detail=False, methods=['post'])
    def selection(self, request):
        ingredient_ids = request.data.get('ingredient_ids', [])
        if not ingredient_ids:
            return Response({"detail": "No ingredient ids provided."}, status=status.HTTP_400_BAD_REQUEST)

        ingredient_count = len(ingredient_ids)

        recipes_with_all_ingredients = Recipe.objects.filter(
            isEnabled=True,
            recipe_ingredients__ingredient__id__in=ingredient_ids
        ).annotate(
            matched_ingredients=Count('recipe_ingredients', filter=Q(recipe_ingredients__ingredient__id__in=ingredient_ids))
        ).filter(matched_ingredients=ingredient_count).distinct()

        recipes_with_some_ingredients = Recipe.objects.filter(
            isEnabled=True,
            recipe_ingredients__ingredient__id__in=ingredient_ids
        ).annotate(
            matched_ingredients=Count('recipe_ingredients', filter=Q(recipe_ingredients__ingredient__id__in=ingredient_ids))
        ).exclude(id__in=recipes_with_all_ingredients.values('id')).distinct().order_by('-matched_ingredients')

        serializer_all = SelectionRecipeSerializer(recipes_with_all_ingredients, many=True, context={'request': request})
        serializer_some = SelectionRecipeSerializer(recipes_with_some_ingredients, many=True, context={'request': request})

        return Response({
            'all_ingredients': serializer_all.data,
            'some_ingredients': serializer_some.data
        })

    @swagger_auto_schema(**recipe_create)
    def create(self, request, *args, **kwargs):
        serializer = CreateRecipeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            recipe = serializer.save()
            return Response(RecipeDetailSerializer(recipe, context={'request': request}).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**recipe_retrieve)
    def retrieve(self, request, *args, **kwargs):
        recipe = self.get_object()
        serializer = RecipeDetailSerializer(recipe, context={'request': request})
        return Response(serializer.data)