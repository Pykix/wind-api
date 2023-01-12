from django.contrib.gis.db import models as gis_models
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Anemometer(gis_models.Model):
    name = gis_models.CharField(max_length=255)
    coordinates = gis_models.PointField()
    tags = gis_models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return self.name


class WindReading(models.Model):
    anemometer = models.ForeignKey(
        Anemometer, on_delete=models.CASCADE, related_name="wind_readings")
    wind_speed = models.FloatField()
    wind_direction = models.FloatField()
    reading_time = models.DateTimeField()

    class Meta:
        ordering = ['-reading_time']

    def __str__(self) -> str:
        return f'{self.anemometer.name} - {self.wind_speed} - {self.reading_time}'
