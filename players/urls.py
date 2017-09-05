from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', PlayersList.as_view(), name='player-list'),
    url(r'^(?P<ckey>\w+)/$', PlayerDetail.as_view(), name='player-details'),
    url(r'^(?P<ckey>\w+)/notes/$', PlayerNotesList.as_view(), name='player-notes-list'),
    url(r'^(?P<ckey>\w+)/notes/new/$', PlayerNotesCreate.as_view(), name='player-notes-create'),
    url(r'^(?P<ckey>\w+)/notes/(?P<id>\d+)/$', PlayerNoteDetail.as_view(), name='player-notes-details'),
    url(r'^admins/$', AdminsList.as_view(), name='admin-list')
]