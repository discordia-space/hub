from django.contrib.auth.backends import ModelBackend

from .models import User


class CkeyLoginBackend(ModelBackend):
    """
    Authentication backend that provides possibility to login with ckey.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username:
            username = kwargs.get(User.USERNAME_FIELD)
        try:
            user = User.objects.get(ckey=username)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
