from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import QuerySet

from typing import Dict, Union, List

from players.filters import PlayerFilter
from utils.mixins import PermissionDenied, MixinView
from users.models import User
from .models import Player, Note, reverse
from .forms import PlayerForm, NoteCreateForm
from utils.permissions import *


class PlayersList(MixinView, ListView):
    """
    /players/
    """
    ordering = ['-last_seen', 'last_seen']
    filter_class = PlayerFilter

    def get_queryset(self) -> QuerySet:
        return Player.objects.all()

    def get_template_names(self) -> List[str]:
        if self._user_is_admin():
            self.template_name = "players/players_list.html"
        else:
            self.template_name = "players/unauthorized/players_list.html"
        return [self.template_name]

    def _get_common_context(self) -> Dict:
        return {
            'filter': self.filter_class(self.request.GET, self.get_queryset())
        }


class PlayerDetail(MixinView, DetailView):
    """
    /players/(?P<ckey>\w+)/
    """
    def _get_admin_context(self) -> Dict:
        if self._user_is_admin():
            return {
                'last_notes': self.get_object().notes.get_queryset()[:5]
        }
        return {}

    def _get_common_context(self) -> Dict:
        player = self.get_object()

        return {
            'player': player,
            'last_bans': player.bans.get_queryset()[:5]
        }

    def get_object(self, queryset=None) -> Player:
        return get_object_or_404(Player, ckey=self.kwargs['ckey'])

    def get_template_names(self) -> List[str]:
        if self._user_is_admin():
            self.template_name = "players/player_detail.html"
        else:
            self.template_name = "players/unauthorized/player_detail.html"
        return [self.template_name]


class PlayerNotesList(MixinView, ListView):
    """
    /players/(?P<ckey>\w+)/notes/
    """
    template_name = "players/note_list.html"
    permission_class = IsAdmin

    def _get_common_context(self) -> Dict:
        return {
            'player': self.get_object(),
            'notes': self.get_queryset()
        }

    def get_object(self) -> Player:
        return get_object_or_404(Player, ckey=self.kwargs['ckey'])

    def get_queryset(self) -> QuerySet:
        return self.get_object().notes.order_by('-created')


class PlayerNoteDetail(MixinView, DetailView):
    template_name = "players/note_detail.html"
    permission_class = IsAdmin

    def get_object(self, queryset=None) -> Note:
        player = get_object_or_404(Player, ckey=self.kwargs['ckey'])
        return get_object_or_404(Note, player=player, pk=self.kwargs['id'])

    def _get_common_context(self) -> Dict:
        return {
            'player': self.get_object(),
            'note': self.get_object(),
        }


class PlayerNotesCreate(MixinView, CreateView):
    form_class = NoteCreateForm
    template_name = "players/note_create.html"
    permission_class = IsAdmin

    def get_admin(self) -> Player:
        return self.request.user.player

    def get_object(self, queryset=None) -> Player:
        return get_object_or_404(Player, ckey=self.kwargs['ckey'])

    def get_success_url(self):
        return reverse('player-notes-list', kwargs={'ckey': self.get_object().ckey})

    def form_valid(self, form):
        form.instance.admin = self.get_admin()
        form.instance.player = self.get_object()
        return super(PlayerNotesCreate, self).form_valid(form)


class AdminsList(MixinView, ListView):
    template_name = "players/admins.html"

    def get_queryset(self):
        return Player.objects.filter(admin=True)

    def _get_common_context(self) -> Dict:
        return {
            'admins': self.get_queryset()
        }
