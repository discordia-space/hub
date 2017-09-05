from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.generic import ListView, DetailView, UpdateView, View
from typing import Dict, List

from .models import Ban
from .forms import BanForm
from utils.permissions import IsAdmin
from utils.mixins import MixinView


class BanListView(MixinView, ListView):
    """
    /bans/
    """
    paginate_by = 'page'

    def get_queryset(self):
        return Ban.objects.all()

    def get_template_names(self) -> List[str]:
        if self._user_is_admin():
            self.template_name = "bans/ban_list.html"
        else:
            self.template_name = "bans/unauthorized/ban_list.html"
        return [self.template_name]


class BanDetailView(MixinView, DetailView):
    """
    /bans/(?P<id>\d+)/
    """
    def get_object(self, queryset=None) -> Ban:
        return get_object_or_404(Ban, pk=self.kwargs['id'])

    def _get_common_context(self) -> Dict:
        return {
            'ban': self.get_object(),
            'player': self.get_object().target
        }

    def get_template_names(self) -> List[str]:
        if self._user_is_admin():
            self.template_name = "bans/ban_detail.html"
        else:
            self.template_name = "bans/unauthorized/ban_detail.html"
        return [self.template_name]


class BanEditView(MixinView, UpdateView):
    """
    /bans/(?P<id>\d+)/edit/
    """
    permission_class = IsAdmin
    form_class = BanForm
    template_name = "bans/ban_edit.html"

    def get_object(self, queryset=None) -> Ban:
        return get_object_or_404(Ban, pk=self.kwargs['id'])


class BanLiftView(MixinView, DetailView):
    """
    /bans/(?P<id>\d+)/lift/
    """
    permission_class = IsAdmin
    form_class = None
    template_name = None

    def get_object(self, queryset=None) -> Ban:
        return get_object_or_404(Ban, pk=self.kwargs['id'])

    def post(self, request, *args, **kwargs):
        ban = self.get_object()
        if ban.active:
            ban.lift(admin=request.user)
        previous_page = request.META['HTTP_REFERER']
        return redirect(previous_page)
