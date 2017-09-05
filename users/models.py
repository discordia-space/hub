from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings

from players.models import Player


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    ckey = models.CharField(max_length=255, unique=True)
    verified_ckey = models.BooleanField(default=False)

    discord = models.CharField(max_length=32, blank=True)
    github = models.CharField(max_length=38, blank=True)

    player = models.OneToOneField(Player, related_name='user', null=True)

    USERNAME_FIELD = 'ckey'

    objects = BaseUserManager

    def save(self, *args, **kwargs):
        if self.verified_ckey and not self.player:
            try:
                player = Player.objects.get(ckey=self.ckey)
                self.player = player
            except ObjectDoesNotExist:
                # TODO: something went really fucking wrong
                pass
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.ckey


class Permissions(models.Model):
    # TODO: clarify and rework needed properties
    bans = models.BooleanField(default=False)
    notes = models.BooleanField(default=False)
    permissions = models.BooleanField(default=False)
    logs = models.BooleanField(default=False)
    server = models.BooleanField(default=False)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='permissions')

    def __str__(self) -> str:
        return "Permissions for {}".format(str(self.user))


@receiver(post_save, sender=User)
def user_permissions_create(sender: User, instance: User, **kwargs) -> None:
    try:
        _ = instance.permissions
    except ObjectDoesNotExist:
        Permissions.objects.create(user=instance)
