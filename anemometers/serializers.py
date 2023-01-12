from datetime import datetime

from django.db.models import Avg
from rest_framework import serializers

from .models import Anemometer, Tag, WindReading


class AnemometerSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='name',
        required=False
    )
    daily_average = serializers.SerializerMethodField()
    weekly_average = serializers.SerializerMethodField()

    class Meta:
        model = Anemometer
        fields = ('id', 'name', 'coordinates', 'tags',
                  'daily_average', 'weekly_average')

    def get_daily_average(self, anemometer):
        """
        Get the average of wind speed for one Anemometer for today
        """
        today = datetime.now().date()
        reading = WindReading.objects.filter(
            anemometer=anemometer, reading_time__date=today)
        return reading.aggregate(Avg('wind_speed'))['wind_speed__avg']

    def get_weekly_average(self, anemometer):
        """
        Get the average of wind speed for one Anemometer for this week
        """
        today = datetime.now()
        week_number = today.strftime('%U')
        print(week_number)
        reading = WindReading.objects.filter(
            anemometer=anemometer, reading_time__week=week_number)
        return reading.aggregate(Avg('wind_speed'))['wind_speed__avg']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class WindReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindReading
        fields = ('anemometer', 'wind_speed',
                  'wind_direction', 'reading_time')
