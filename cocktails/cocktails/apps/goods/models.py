import logging
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from base.fields import *
from base.models import BaseModel, CreatedUpdatedModel
from django.contrib.postgres.fields import ArrayField


__all__ = [
    'Goods',
]

logger = logging.getLogger(__name__)


class Goods(CreatedUpdatedModel):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='tool_photos/', null=True, blank=True, verbose_name='Фото')
    links = models.JSONField(null=True, blank=True, verbose_name='Ссылки')

    class Meta:
        ordering = ['id']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return '{}'.format(self.name)