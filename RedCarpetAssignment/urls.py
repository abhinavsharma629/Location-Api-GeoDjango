from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from GeoLocation import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('GeoLocation.urls')),
    path('post_location', views.processPoints.as_view()),
    path('get_using_self', views.processPointsBySelf.as_view()),
    path('get_using_Postgres', views.processPointsByPostgres.as_view()),
    path('compareSelfWithPostgres', views.compareResults.as_view()),
    path('latitude_longitude', views.latitude_longitude.as_view()),
]
#binds functions to methods as_view()
#get ka get , post ko post method etc
urlpatterns=format_suffix_patterns(urlpatterns)