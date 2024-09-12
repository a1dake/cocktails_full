from django.contrib import admin
from apps.goods.models import *
from base.admin import BaseAdmin


@admin.register(Goods)
class GoodsAdmin(BaseAdmin):
    list_display = ('id', 'name', 'description', 'photo', 'links')
    search_fields = ('name', 'links')
    ordering = ('id', )