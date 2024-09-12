from django.contrib import admin

from apps.common.models import *
from base.admin import BaseAdmin


@admin.register(Ads)
class AdsAdmin(BaseAdmin):
    list_display = ['title', 'description', 'target_audience', 'images', 'url']
    search_fields = ['title', 'target_audience', 'url']
    list_filter = (
        'target_audience',
    )


@admin.register(FAQ)
class FAQAdmin(BaseAdmin):
    list_display = ['question', 'answer']
    search_fields = ['question', 'answer']


@admin.register(Document)
class DocumentAdmin(BaseAdmin):
    list_display = ['title', 'document_type', 'file']
    search_fields = ['title', 'document_type']
    list_filter = (
        'document_type',
    )


@admin.register(Config)
class ConfigAdmin(BaseAdmin):
    list_display = ['name', 'code', 'text']
    search_fields = ['name', 'code', 'value', 'description']
    readonly_fields = ['code']
    can_delete = False
    can_add = False

    @staticmethod
    def text(obj: Config):
        return obj.value[:100]