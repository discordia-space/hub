from django.db import models
from django.urls import reverse

from typing import List


class Player(models.Model):
    """
    define R_BUILDMODE     0x1
    define R_ADMIN         0x2
    define R_BAN           0x4
    define R_FUN           0x8
    define R_SERVER        0x10
    define R_DEBUG         0x20
    define R_POSSESS       0x40
    define R_PERMISSIONS   0x80
    define R_STEALTH       0x100
    define R_REJUVINATE    0x200
    define R_VAREDIT       0x400
    define R_SOUNDS        0x800
    define R_SPAWN         0x1000
    define R_MOD           0x2000
    define R_MENTOR        0x4000
    define R_HOST          0x8000
    """
    ckey = models.CharField(max_length=255)
    rank = models.CharField(max_length=64, default='player')
    admin = models.BooleanField(default=False)
    # TODO: reimplement flags with proper permissions
    flags = models.IntegerField(default=0)

    registered = models.DateField(null=True, blank=True)
    cid = models.CharField(max_length=64, blank=True)
    byond_version = models.CharField(max_length=16, blank=True)
    first_seen = models.DateTimeField(blank=True, null=True)
    last_seen = models.DateTimeField(blank=True, null=True)
    last_ip = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        ordering = ["-last_seen"]

    def known_ip_addresses(self) -> List[str]:
        return [connection.ip for connection in self.connections.all()]

    def __str__(self) -> str:
        return self.ckey

    def get_absolute_url(self) -> str:
        return reverse('player-details', kwargs={'ckey': self.ckey})


class Connection(models.Model):
    server = models.CharField(max_length=64)
    player = models.ForeignKey(Player, related_name='connections')
    ip = models.GenericIPAddressField()
    cid = models.CharField(max_length=64)

    active = models.BooleanField(default=True)
    duration = models.TimeField(blank=True, null=True)
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-login_time"]

    def save(self, *args, **kwargs) -> None:
        if self.logout_time:
            self.duration = self.logout_time - self.login_time
            self.active = False
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return "Connection at {} from {} by {}.".format(self.login_time, self.ip, self.player.ckey)


class Note(models.Model):
    player = models.ForeignKey(Player, related_name='notes')
    admin = models.ForeignKey(Player, related_name='created_notes')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "Note for {}: {}".format(self.player.ckey, self.text)
