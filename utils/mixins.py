from django.views.generic.base import View, ContextMixin
from django.core.exceptions import PermissionDenied
from typing import Dict

from .permissions import AllowAny


class PermissionMixin(View):
    permission_class = AllowAny

    def dispatch(self, request, *args, **kwargs):
        if not self._check_permissions(request):
            raise PermissionDenied
        return super(PermissionMixin, self).dispatch(request, *args, **kwargs)

    def _check_permissions(self, request) -> bool:
        return self.permission_class.has_permission(request)


class RequestContextMixin(ContextMixin):
    request = None

    def _user_is_admin(self) -> bool:
        user = self.request.user
        return user.is_authenticated and user.player.admin

    def _get_common_context(self) -> Dict:
        return {}

    def _get_admin_context(self) -> Dict:
        return {}

    def get_context_data(self, **kwargs) -> Dict:
        context = {}

        if self.request.user.is_authenticated:
            context['current_user'] = self.request.user

        return {
            **super(RequestContextMixin, self).get_context_data(**kwargs),
            **self._get_common_context(),
            **self._get_admin_context(),
            **context
        }


class MixinView(RequestContextMixin, PermissionMixin):
    pass