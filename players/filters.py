import django_filters

from .models import Player, Connection

class PlayerFilter(django_filters.FilterSet):
    ckey = django_filters.CharFilter(name='ckey', lookup_expr='icontains', label='ckey')
    ip = django_filters.CharFilter(method='filter_ip', label='ip')
    cid = django_filters.CharFilter(method='filter_cid', label='cid')

    class Meta:
        model = Player
        fields = ['ckey', 'ip', 'cid']

    def filter_ip(self, queryset, name, value):
        connections = Connection.objects.filter(ip=value).values_list('player', flat=True)
        return queryset.filter(id__in=connections)

    def filter_cid(self, queryset, name, value):
        connections = Connection.objects.filter(cid=value).values_list('player', flat=True)
        return queryset.filter(id__in=connections)
