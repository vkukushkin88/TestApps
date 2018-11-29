from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.models import User

# Create your models here.


class Post(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Base User'),
        related_name='user_post'
    )

    text = models.TextField(
        verbose_name=_('text port'),
        blank=True, null=True
    )

    link = models.URLField(
        verbose_name=_("Link"),
        max_length=128,
        blank=True, null=True
    )

    likes = models.ManyToManyField(
        User,
        related_name='user_likes',
    )

    def add_once(self, user):
        if not self.likes.filter(id=user.id):
            self.likes.add(user)
