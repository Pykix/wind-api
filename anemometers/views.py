from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.db.models.aggregates import Avg, Max, Min
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import AnemometerFilter
from .models import Anemometer, Tag, WindReading
from .paginations import (AllWindReadingPagination,
                          WindReadingFromAnemometerPagination)
from .serializers import (AnemometerSerializer, TagSerializer,
                          WindReadingSerializer)


class AnemometerViewSet(viewsets.ModelViewSet):
    """CRUD for Anemometers

    Args:
        viewsets (_type_): _description_
    """
    queryset = Anemometer.objects.all()
    serializer_class = AnemometerSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AnemometerFilter
    permission_classes = [IsAuthenticated]


class WindReadingForAAnemometerListView(ListAPIView):
    """List all wind readings from a given anemometer
    """
    serializer_class = WindReadingSerializer
    pagination_class = WindReadingFromAnemometerPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        anemometer = get_object_or_404(Anemometer, pk=self.kwargs['pk'])
        return WindReading.objects.filter(anemometer=anemometer)


class TagViewSet(viewsets.ModelViewSet):
    """CRUD for Tags
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


class WindReadingCreateListRetrieveView(mixins.CreateModelMixin,
                                        mixins.ListModelMixin,
                                        mixins.RetrieveModelMixin,
                                        viewsets.GenericViewSet):
    """Create, Retrieve and List wind readings
    """
    queryset = WindReading.objects.all()
    serializer_class = WindReadingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = AllWindReadingPagination


class WindStatisticView(ListAPIView):
    """List statistics (Min, Max, Average) for Anemometer following url parameters like lat, lon and radius
    """
    serializer_class = WindReadingSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)
        radius = request.query_params.get('radius', None)

        if not latitude or not longitude or not radius:
            return Response({'error': 'Missing parameters'}, status=400)

        point = Point(float(longitude), float(latitude))
        radius = Distance(nm=float(radius))

        anemometers = Anemometer.objects.filter(
            coordinates__distance_lte=(point, radius))

        wind_reading = WindReading.objects.filter(anemometer__in=anemometers)

        statistics = {
            "max": wind_reading.aggregate(Max('wind_speed'))['wind_speed__max'],
            "min": wind_reading.aggregate(Min('wind_speed'))['wind_speed__min'],
            "average": wind_reading.aggregate(Avg('wind_speed'))['wind_speed__avg']
        }

        return Response(statistics)
