from apps.user.models import *
from apps.recipe.models import *
from rest_framework.exceptions import NotAuthenticated
from .serializers import *
from api.base.permissions import IsActiveUser
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from api.v1.recipe.serializers import RecipeListSerializer


class UserRecipeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = RecipeListSerializer
    permission_classes = [IsActiveUser]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Recipe.objects.none()
        if self.request.user.is_anonymous:
            raise NotAuthenticated("User is not authenticated")
        return Recipe.objects.filter(user=self.request.user)


class FavoriteUserRecipeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin, mixins.CreateModelMixin, GenericViewSet):
    serializer_class = FavoriteRecipeSerializer
    permission_classes = [IsActiveUser]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return FavoriteRecipe.objects.none()
        if self.request.user.is_anonymous:
            raise NotAuthenticated("User is not authenticated")
        return FavoriteRecipe.objects.filter(user=self.request.user)


class UserViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsActiveUser]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id).prefetch_related('points', 'favorite_recipes', 'recipes_user')

    def get_object(self):
        user = self.request.user
        if user.is_anonymous:
            raise NotAuthenticated("User is not authenticated")
        return user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# class UserNotificationViewSet(viewsets.ModelViewSet):
#     serializer_class = NotificationSerializer
#     permission_classes = [IsActiveUser]
#
#     def get_queryset(self):
#         return Notification.objects.filter(user=self.request.user)
