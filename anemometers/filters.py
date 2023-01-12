import django_filters

from .models import Anemometer


class AnemometerFilter(django_filters.FilterSet):
    tags = django_filters.BaseInFilter(field_name='tags__name')

    class Meta:
        model = Anemometer
        fields = ['tags']
