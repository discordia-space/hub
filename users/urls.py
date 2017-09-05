from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^register/$', UserRegistration.as_view(), name='user-registration'),
    url(r'^settings/$', UserSettings.as_view(), name='user-settings'),
    url(r'^settings/edit/$', UserSettingEdit.as_view(), name='user-settings-edit'),
    url(r'^login/$', UserLogin.as_view(), name='user-login'),
    url(r'^logout/$', UserLogout.as_view(), name='user-logout'),
]
