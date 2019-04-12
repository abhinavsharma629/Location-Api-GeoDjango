from django.urls import path
from . import views

urlpatterns = [
    path('addPoint', views.addPoint, name='addPoint'),
    path('geoJsonScrape/<address>', views.dataScrapeFromOpenStreetMapApi, name='dataScrapeFromOpenStreetMapApi'),
    path('geoJsonParse', views.geoJsonParseThroughFile, name='geoJsonParseThroughFile'),
]