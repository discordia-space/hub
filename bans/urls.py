from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', BanListView.as_view(), name='ban-list'),
    url(r'^(?P<id>\d+)/$', BanDetailView.as_view(), name='ban-detail'),
    url(r'^(?P<id>\d+)/edit/$', BanEditView.as_view(), name='ban-edit'),
    url(r'^(?P<id>\d+)/lift/$', BanLiftView.as_view(), name='ban-lift')
]
