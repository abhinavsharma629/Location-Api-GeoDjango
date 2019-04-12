from django.db import models
from django.contrib.gis.db import models
from django_earthdistance.models import EarthDistanceQuerySet
from django.contrib.postgres.fields import JSONField
from django.contrib.gis.geos import GEOSGeometry


#Spatial Data
class spatialData(models.Model):
	key=models.CharField(max_length=200)
	place_name=models.CharField(max_length=200)
	city_name=models.CharField(max_length=200)
	latitude=models.FloatField(default=0.0, null=True, blank=True)
	longitude=models.FloatField(default=0.0,null=True, blank=True)
	latitude_longitude = models.PointField(srid=4326, null=True,blank=True, spatial_index=True, geography=True)
	accuracy=models.IntegerField(default=0,null=True, blank=True)


#Comparison Data For Postgres
class comparisonDataForPostgres(models.Model):
	centerlatitude=models.FloatField(default=0.0)
	centerlongitude=models.FloatField(default=0.0)
	latitude=models.FloatField(default=0.0)
	longitude=models.FloatField(default=0.0)
	location_key=models.CharField(max_length=200)
	radius=models.IntegerField(default=0)


#Comparison Data By Self
class comparisonDataBySelf(models.Model):
	centerlatitude=models.FloatField(default=0.0)
	centerlongitude=models.FloatField(default=0.0)
	latitude=models.FloatField(default=0.0)
	longitude=models.FloatField(default=0.0)
	location_key=models.CharField(max_length=200)
	radius=models.IntegerField(default=0)


#Geojson Data For A Place
class geojson(models.Model):
	location_name=models.CharField(primary_key=True, max_length=1000)
	data=models.GeometryField()

class geojsonThroughFile(models.Model):
	location_name=models.CharField(primary_key=True, max_length=1000)
	data=models.GeometryField()