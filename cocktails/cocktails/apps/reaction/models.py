from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.user.models import User
from base.fields import ForeignKey
from base.models import BaseModel
from services.notify import send_notification

__all__ = [
    'Like',
    'Comment',
    'Hit',
]


class BaseReactionModel(BaseModel):
    content_type = ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        abstract = True


class Like(BaseReactionModel):
    """
    Универсальная модель для лайков. Можно привязывать к любой модели.
    """
    RELATED_NAME = 'likes'

    user = ForeignKey(User, related_name=RELATED_NAME)
    value = models.BooleanField(verbose_name='Значение (лайк/дизлайк)')

    class Meta:
        indexes = [models.Index(fields=["content_type", "object_id"])]
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Comment(BaseReactionModel):
    """
    Универсальная модель для комментариев. Можно привязывать к любой модели.
    """
    RELATED_NAME = 'comments'

    user = ForeignKey(User, related_name=RELATED_NAME)
    text = models.TextField(verbose_name='Комментарий')
    likes = GenericRelation(Like)

    class Meta:
        indexes = [models.Index(fields=["content_type", "object_id"])]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


@receiver([post_save], sender=Comment)
def send_quest_review_notification(sender, instance: Comment, **kwargs):
    from apps.recipe.models import Recipe
    if not isinstance(instance.content_object, Recipe):
        return

    user_ids = User.objects.filter(
        quest_managers__quest__stages__id=instance.content_object.stage_id,  # noqa
    ).values_list('id', flat=True).distinct()
    for user_id in user_ids:
        send_notification.delay(
            user_id,
            f'Ученик {instance.user.profile.full_name} оставил комментарий к материалу '  # noqa
            f'"{instance.content_object.title}".',
            f'The student {instance.user.profile.full_name} left a comment on the material '  # noqa
            f'"{instance.content_object.title}".',
        )


class Hit(BaseReactionModel):
    """
    Универсальная модель для просмотров. Можно привязывать к любой модели.
    """
    RELATED_NAME = 'hits'

    user = ForeignKey(User, related_name=RELATED_NAME)

    class Meta:
        indexes = [models.Index(fields=["content_type", "object_id"])]
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Просмотры'
