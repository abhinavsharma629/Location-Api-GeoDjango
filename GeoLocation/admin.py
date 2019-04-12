from django.contrib import admin
from .models import spatialData,comparisonDataForPostgres,comparisonDataBySelf, geojson, geojsonThroughFile

admin.site.register(spatialData)
admin.site.register(comparisonDataForPostgres)
admin.site.register(comparisonDataBySelf)
admin.site.register(geojson)
admin.site.register(geojsonThroughFile)