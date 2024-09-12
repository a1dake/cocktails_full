from django.urls import path, include

app_name = 'admin_api'

urlpatterns = [
    path('goods/', include('api.v1.admin.goods.urls')),
    path('recipe/', include('api.v1.admin.recipe.urls')),
    path('profile/', include('api.v1.admin.profile.urls')),
    path('auth/', include('api.v1.admin.auth.urls')),
]
