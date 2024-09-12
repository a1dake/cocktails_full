from rest_framework import serializers
from apps.goods.models import *


__all__ = [
    'GoodsSerializer',
]


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'
