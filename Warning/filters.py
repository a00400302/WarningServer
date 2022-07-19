import django_filters
from django_filters.rest_framework import FilterSet

from .models import PushUser, WarningHistory


class ServerFilter(FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    enable = django_filters.BooleanFilter(field_name='enable')
    phone = django_filters.CharFilter(field_name='phone', lookup_expr='icontains')

    class Meta:
        model = PushUser
        fields = ['name', 'enable', 'phone']


TICKET_STATUS_CHOICES = (
    (1, '三轮车识别'),
    (2, '行人识别'),
)


class WaringFilter(FilterSet):
    type = django_filters.ChoiceFilter(field_name='type', choices=TICKET_STATUS_CHOICES)
    #开始时间
    start_date = django_filters.DateFilter(field_name='time', lookup_expr='gte')
    #结束时间
    end_date = django_filters.DateFilter(field_name='time', lookup_expr='lte')

    class Meta:
        model = WarningHistory
        fields = ['type']
