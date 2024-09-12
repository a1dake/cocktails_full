from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from .serializers import *
from base.pagination import BasePagination
from rest_framework.permissions import AllowAny
from apps.recipe.models import *


class IngredientCategoryViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = IngredientCategory.objects.all()
    serializer_class = AdminIngredientCategorySerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        self.serializer_class = AdminIngredientCategorySerializer
        return super().list(request, *args, **kwargs)


class IngredientViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = AdminIngredientSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = AdminIngredientSerializer
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.serializer_class = AdminIngredientSerializer
        return super().list(request, *args, **kwargs)


class ToolViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Tool.objects.all()
    serializer_class = AdminViewToolSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        self.serializer_class = AdminViewToolSerializer
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = AdminViewToolSerializer
        return super().retrieve(request, *args, **kwargs)


class RecipeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [AllowAny]
    pagination_class = BasePagination

    def list(self, request, *args, **kwargs):
        self.serializer_class = AdminRecipeSerializer
        return super().list(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = AdminUpdateRecipeSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = AdminCreateRecipeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            recipe = serializer.save()
            return Response(AdminRecipeSerializer(recipe, context={'request': request}).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        recipe = self.get_object()
        serializer = AdminRecipeSerializer(recipe, context={'request': request})
        return Response(serializer.data)