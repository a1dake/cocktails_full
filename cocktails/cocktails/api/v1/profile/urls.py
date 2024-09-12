from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


user_list = UserViewSet.as_view({
    'get': 'retrieve'
})

router = DefaultRouter()
router.register(r'recipe', UserRecipeViewSet, basename='user-recipe')
router.register(r'favorite', FavoriteUserRecipeViewSet, basename='favorite-user-recipe')
# router.register(r'notifications', UserNotificationViewSet, basename='user-notifications')

urlpatterns = [
    path('', user_list, name='user-profile'),
    path('', include(router.urls)),
]