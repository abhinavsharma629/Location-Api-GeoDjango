from rest_framework import serializers
from .models import spatialData, comparisonDataForPostgres, comparisonDataBySelf, geojson

class spatialDataSerializer(serializers.ModelSerializer):
	
	class Meta:
		model=spatialData  # what module you are going to serialize
		fields= '__all__'

class comparisonDataForPostgresSerializer(serializers.ModelSerializer):
	
	class Meta:
		model=comparisonDataForPostgres  # what module you are going to serialize
		fields= '__all__'

class comparisonDataBySelfSerializer(serializers.ModelSerializer):
	
	class Meta:
		model=comparisonDataBySelf  # what module you are going to serialize
		fields= '__all__'

class geojsonSerializer(serializers.ModelSerializer):
	
	class Meta:
		model=geojson  # what module you are going to serialize
		fields= '__all__'