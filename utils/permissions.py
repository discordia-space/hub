

class BasePermission(object):
    """
    A base class from which all permission classes should inherit.
    """
    @classmethod
    def has_permission(self, request):
        return True


class AllowAny(BasePermission):
    @classmethod
    def has_permission(cls, request):
        return True


class IsAuthenticated(BasePermission):
    @classmethod
    def has_permission(cls, request):
        return request.user and request.user.is_authenticated


class IsAdmin(BasePermission):
    @classmethod
    def has_permission(cls, request):
        return request.user.is_authenticated and request.user.player.admin
