from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class UserAccount(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Base User'),
        related_name='user_account'
    )

    about = models.TextField(
        verbose_name=_('About'),
        null=True, blank=True
    )

    birthday = models.DateField(
        verbose_name=_('Birthday'),
        null=True, blank=True
    )
