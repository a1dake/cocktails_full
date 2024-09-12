from apps.user.models import *
from apps.recipe.models import *
from .serializers import *
from api.base.permissions import IsActiveUser
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from rest_framework import mixins


class AdminUserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = AdminUserSerializer
    permission_classes = [IsActiveUser]
    #permission_classes = [AllowAny]
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        self.serializer_class = AdminUserListSerializer
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = AdminUserSerializer
        return super().retrieve(request, *args, **kwargs)