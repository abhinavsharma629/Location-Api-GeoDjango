from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import spatialData, comparisonDataForPostgres, comparisonDataBySelf, geojson, geojsonThroughFile
from .serializers import spatialDataSerializer, comparisonDataForPostgresSerializer,comparisonDataBySelfSerializer
from django.utils import timezone
from django.db.models import Q
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
import requests
import mechanicalsoup
from bs4 import BeautifulSoup
import math
from django.http import JsonResponse
import time
from .request_params import request_param
from .request_params_Post import requestParamPost
from .requestparamForGeojson import requestparamForGeojson
import json
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import Polygon, MultiLineString, LineString, GEOSGeometry, MultiPoint, MultiPolygon
from django.db import connection


'''Post APi for Interview 1 question
Post lat,lng of any location with pin code+address+city and you can add new pin code in db. This api will be /post_location.
Remember to check if pin code already exists or if there are existing latitude+longitude THAT ARE CLOSE ENOUGH TO BE THE SAME
(dont assume that they will exactly be the same.)'''

class processPoints(APIView):
	def post(self,request):

		serializer= spatialDataSerializer(data=request.data)
		request_para=requestParamPost(request.data)
		split=request_para.split(',')
		
		if(len(split)<3):
			data={'Error message': split[0]}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)
			
		else:
			if serializer.is_valid():
				query1=spatialData.objects.filter(Q(key=split[0]))
				if(len(query1)>0):
					data={'Error message': "Pincode Already Exists"}
					return Response(data, status=status.HTTP_400_BAD_REQUEST)
				else:

					#Calculation of very nearby points
					for i in spatialData.objects.all():
						dlon =  i.longitude-float(split[1])
						dlat= i.latitude-float(split[0])
						dist = math.acos(math.sin(math.radians(i.latitude))
							*math.sin(math.radians(float(split[0])))
							+math.cos(math.radians(i.latitude))
							*math.cos(math.radians(float(split[0])))
							*math.cos(math.radians(i.longitude)
							-math.radians(float(split[1]))))*6371
						
						if(dist<=1):
							return JsonResponse({'Error message': "Very Close Place/s Already Exists"})

				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#Analyse points using Selfmade formula
class processPointsBySelf(APIView):
	def get(self,request):
		#Using Self made formula to find points lying within a given radius
		
		request_para=request_param(request.query_params)
		split=str(request_para).split(',')

		if(len(split)<3):
			return Response({'Error message': split[0]}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

		else:
			pointsLyingInRange=spatialData.objects.all()
			if(len(pointsLyingInRange)!=0):
				latitude=float(split[1])
				longitude=float(split[2])
				radius=(int)(split[0])
				time1=0
				start=time.time()

				for i in pointsLyingInRange:
					#Origin Latitude and Longitude
					centerLatitude=i.latitude
					centerLongitude=i.longitude

					#Calculating distance of the origin till the current point
					dist = math.acos(math.sin(math.radians(centerLatitude))
						*math.sin(math.radians(latitude))
						+math.cos(math.radians(centerLatitude))
						* math.cos(math.radians(latitude))
						*math.cos(math.radians(centerLongitude)
						- math.radians(longitude)))* 6371

					#Calculating Total Time for each operation excluding the time for object creation
					time1+=(int)(time.time()-start)
					start=time.time()
					if(dist<=radius):
						obj,notif=comparisonDataBySelf.objects.get_or_create(centerlatitude=centerLatitude,
							centerlongitude=centerLongitude,latitude=str(latitude),
							longitude=str(longitude), location_key=i.key, radius=radius)
						if notif is True:
							obj.save()
				
				print("Time Taken By Self:-",(int)(time1))
				pointsLyingInRange=comparisonDataBySelf.objects.filter(Q(latitude=str(latitude)), Q(longitude=str(longitude)), Q(radius=radius))
				serializer= comparisonDataBySelfSerializer(pointsLyingInRange, many=True)
				return Response(serializer.data, status=status.HTTP_200_OK)

			else:
				return Response({'Error Message':'Insufficient Data in Database'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)



#Analyse points using Postgres earthdistance
class processPointsByPostgres(APIView):
	def get(self,request):
		#Using Postgres earthdistance to find points lying within a given radius
		start=time.time()
		request_para=request_param(request.query_params)
		split=str(request_para).split(',')
		
		if(len(split)<3):
			return Response({'Error message': split[0]}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

		else:
			pointsLyingInRange=spatialData.objects.all()
			if(len(pointsLyingInRange)!=0):
				#Converting to POINT object
				latitude=float(split[1])
				longitude=float(split[2])
				radius=(int)(split[0])
				point='POINT('+str(latitude)+' '+str(longitude)+')'
				pnt = GEOSGeometry(point, srid=4326)

				pointsLyingInRange = spatialData.objects.filter(latitude_longitude__distance_lte=(pnt, D(km=int(radius))))
				print("Time Taken:-",time.time()-start)

				for i in pointsLyingInRange:
					#Create Entry if not exists
					if(len(comparisonDataForPostgres.objects.filter(Q(latitude=str(latitude)), Q(longitude=str(longitude)),Q(location_key=i.key), Q(radius=radius)))==0):
							data=comparisonDataForPostgres(centerlatitude=i.latitude,centerlongitude=i.longitude,latitude=str(latitude), longitude=str(longitude), location_key=i.key, radius=radius)
							data.save()

				
				pointsLyingInRange=comparisonDataForPostgres.objects.filter(Q(latitude=str(latitude)), Q(longitude=str(longitude)), Q(radius=radius))
				
				serializer= comparisonDataForPostgresSerializer(pointsLyingInRange, many=True)
				return Response(serializer.data, status=status.HTTP_200_OK)
			
			else:
				return Response({'Error Message':'Insufficient Data in Database'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)




'''Final Api of Geojson Data
Given A Lat/Long Find in which places does it lie under'''

class latitude_longitude(APIView):
	def get(self,request):

		request_para=requestparamForGeojson(request.query_params)
		split=str(request_para).split(',')
		
		if(len(split)<2):
			return Response({'Error message': split[0]}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

		else:
			#HardCoded Query
			
			cursor = connection.cursor()
			lat_long=split[0]+" "+split[1]
			point1="POINT("+str(lat_long)+")'"
			cursor.execute('''SELECT location_name FROM "GeoLocation_geojsonthroughfile" WHERE ST_Intersects("GeoLocation_geojsonthroughfile".data, 'SRID=4326;'''+point1+''')''')
			
			#Fetching Location Name
			objArray=[]
			obj=cursor.fetchone()
			try:
				for i in obj:
					objArray.append(i)
				return Response({"Area Lies Within The Following Locations:- ":objArray}, status=status.HTTP_200_OK)
			except:
				return Response({"Area Lies Within The Following Locations:- ":"Not Stored In Database Yet"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)




#Additional Features

'''Final Api of Geojson Data
a Geojson is a json file which defines shapes of locations - for example the shape of delhi, gurgaon, etc.
This geojson is used to define delhi and its areas. https://gist.github.com/ramsingla/6202001?short_path=7d9a995
you can check it out by going to http://geojson.io and pasting the raw json on the right side (on tab marked JSON).
You will then parse this json, and load the boundaries latitude and longitude (geometry -> coordinates) into postgresql
in a new table. you can use any structure, but remember that one place will have lots of lat/long
(because it marks the boundaries).'''

def geoJsonParseThroughFile(request):

			try:
				with open('C:/Users/User/Desktop/map.geojson') as json_file:  
					data = json.load(json_file)
			
				tuj=[]
				tupl=[]
				c=0
				dataSize=data['features']

				#Parsing The Places In File And Creating Their Geometry
				for j in dataSize:
					data1=dataSize[c]['geometry']['coordinates']
					address=data['features'][c]['properties']['name']
					for i in data1:
						for j in i:
							tup=tuple(j)
							tupl.append(tup)
						tuple1=tuple(tupl)
						
						#Making A Polygon And Storing In Database
						polygon=Polygon(tuple1)
						poly = GEOSGeometry(polygon)
						tupl=[]
						z = geojsonThroughFile(location_name=address, data=poly)
						z.save()
						c+=1
				

				return JsonResponse({"Message":"Successfully Uploaded Geometry In Database"})
		
			except:
				return Response({"Message":"Some Error Occured"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)



#Comparing Accuracy Rates Of Self Analysed and Postgres earthdistance analysed data
class compareResults(APIView):
	def get(self,request):
		comparisonDataBySelf1=comparisonDataBySelf.objects.all()
		comparisonDataForPostgres1=comparisonDataForPostgres.objects.all()

		array=[]
		count=0
		accuracy=0
		accuracyRate={}
		c=1

		if(len(comparisonDataForPostgres1)>=len(comparisonDataBySelf1)):
			greater="comparisonDataForPostgres"
		else:
			greater="comparisonDataBySelf"

		for i in  (comparisonDataForPostgres1 if(greater=="comparisonDataForPostgres") else comparisonDataBySelf1):
			
			#Defining Information in string format splitted by ,
			numberinPostgres=comparisonDataForPostgres.objects.filter(Q(centerlatitude=i.centerlatitude),Q(centerlongitude=i.centerlongitude), Q(radius=i.radius))
			numberinSelf=comparisonDataBySelf.objects.filter(Q(centerlatitude=i.centerlatitude),Q(centerlongitude=i.centerlongitude), Q(radius=i.radius))
			#Finding Intersection
			for j in numberinPostgres:
				if(str(j.location_key) == str(k.location_key) for k in numberinSelf):
					count+=1
				
			#Calculating Accuracy Of Both Type Of Get API's
			try:
				
				accuracy+=(count/(len(numberinPostgres)+len(numberinSelf)))*100
			except:
				accuracy+=0
			
			count=0
			accuracyRate[c]=accuracy
			accuracy=0
			c=c+1

		return JsonResponse({"Accuracy Rates Of Self vs Postgres is:- ":accuracyRate})



#Add Point Using Latitude And Longitude Information And Save In Database else Delete if No Lat/Long Entry
def addPoint(request):
	try:
		for i in spatialData.objects.all():

			if(str(i.latitude)!="None" and str(i.longitude)!="None"):
				point='POINT('+str(i.latitude)+' '+str(i.longitude)+')'
				i.latitude_longitude=point
				i.save()
			else:
				i.delete()
	except:
		return Response({'Message': 'Some Error Occured'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
	return JsonResponse({'Message': 'Successfully Updated Database'})




'''Additional Feature For Final Api of Geojson Data
Add Boundaries To The Database By giving The Valid Name Of The Place.
Used OpenStreetMapApi for fetching the geojson Data'''

def dataScrapeFromOpenStreetMapApi(request, address):
	url="https://nominatim.openstreetmap.org/search.php?q="+address+"&polygon_geojson=1&format=json"
	response=requests.get(url)
	res=response.content.decode('utf-8')
	data = json.loads(res)
	data1=data
	c=0

	#Take Only Places Whose Boundaries Are Defined
	for i in data:
		if(i['class']=="boundary"):
			c=1
			break

	#If Boundaries Are Not Defined Then See if its a place
	if(c==0):
		for i in data:
			if(i['class']=="place"):
				c=1
				break
		
	if(c==0):
		for i in data:
			if(i['class']=="administrative"):
				c=1
				break

	if(c==1):

		data=i
		print(data)
		data=data['geojson']
		typeOfData=data['type']
		data=data['coordinates']
		tup=()
		tupl=[]
		tuple1=()
		

		if(typeOfData=="Polygon" or typeOfData=="MultiPolygon"):
			print("we")
			for i in data:
				for j in i:
					tup=tuple(j)
					tupl.append(tup)
				tuple1=tuple(tupl)

			polygon=Polygon(tuple1)
			poly = GEOSGeometry(polygon)
			z = geojson(location_name=address, data=poly)
			z.save()
			return JsonResponse({"Message":"Successfully Stored Geometry In Database"})


		elif(typeOfData=="LineString" or typeOfData=="MultiLineString"):

			for i in data:
				for j in i:
					print(j)
					tupl.append(j)
					

			line=LineString(tupl)
			poly = GEOSGeometry(line)
			z = geojson(location_name=address, data=poly)
			z.save()
			return JsonResponse({"Message":"Successfully Stored Geometry In Database"})
		
		else:
			return Response({"Message":"Enter a Valid Location(Place) Geometry In Database"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

	else:
		return Response({"Message":"Enter a Valid Location Geometry In Database"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
