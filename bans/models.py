from django.db import models
from django.urls import reverse
from typing import List
import datetime

from players.models import Player
from users.models import User


class Ban(models.Model):
    BAN_TYPE_CHOICES = (
        ('common', 'common'),
        ('job', 'job'),
        ('role', 'role'),
        ('mute', 'mute')
    )
    BAN_TAGS = ["rule#0", "multiacc", "griefing", "metagame", "breaking immersion", "illiteracy", "IC in OOC",
                "cooperation", "ERP"]

    type = models.CharField(max_length=32, choices=BAN_TYPE_CHOICES, default='common')

    target = models.ForeignKey(Player, related_name='bans')
    admin = models.ForeignKey(Player, related_name='applied_bans')

    server = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True, blank=True)
    cid = models.CharField(max_length=64, blank=True)

    reasons = models.TextField() # it should be checkboxes
    description = models.TextField()
    # jobs = models.TextField()

    permanent = models.BooleanField(default=False)
    duration = models.IntegerField(blank=True, null=True)
    applied_time = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(blank=True, null=True)

    unbanned = models.BooleanField(default=False)
    ubanned_time = models.DateTimeField(null=True, blank=True)
    ubanned_by = models.ForeignKey(Player, null=True, blank=True, related_name='lifted_bans')

    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-applied_time"]

    def save(self, *args, **kwargs) -> None:
        if self.expiration_time:
            self.duration = self.expiration_time - self.applied_time
        else:
            self.permanent = True

        if self.unbanned:
            self.active = False

        if self.expiration_time:
            if self.expiration_time < datetime.datetime.now():
                self.active = False
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return "Ban record for {} applied by {}.".format(self.target.ckey, self.admin.ckey)

    def get_reasons(self) -> List[str]:
        return self.reasons.split(',')

    def get_absolute_url(self) -> str:
        return reverse('ban-detail', kwargs={'id': self.id})

    def lift(self, admin: User) -> None:
        self.ubanned = True
        self.ubanned_by = admin.player
        self.ubanned_time = datetime.datetime.now()
        self.active = False
        self.save()
