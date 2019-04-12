from django.test import TestCase
from .models import spatialData, comparisonDataForPostgres, comparisonDataBySelf, geojson, geojsonThroughFile
from rest_framework.test import APITestCase
from .testdata import SecondApiTestDataSuccess, SecondApiTestDataFail, ThirdApiTestDataSuccess, ThirdApiTestDataFail

#For The First Post Api Of Interview Question 1
class Interview1APITestCase(APITestCase):

	def test_post_method_success(self):
			url1="http://127.0.0.1:8000/post_location"
			data={
				"latitude":45.66,
				"longitude":56.77,
				"key":"In/19002",
				"place_name":"Haridwar",
				"city_name":"Himachal Pradesh"
				}

			response=self.client.post(url1, data, format='json')
			self.assertEqual(response.status_code, 201)
			selfdb=spatialData.objects.all()
			self.assertEqual(selfdb.count(), 1)


	def test_post_method_fail(self):
			url1="http://127.0.0.1:8000/post_location"
			
			data={
				"latitude":45.66,
				"longitude":56.77,
				"key":"",
				"place_name":"Haridwar",
				"city_name":"Himachal Pradesh"
				}

			response=self.client.post(url1, data, format='json')
			self.assertEqual(response.status_code, 400)
			selfdb=spatialData.objects.all()
			self.assertEqual(selfdb.count(), 0)


			data={
				"latitude":90.66,
				"longitude":56.77,
				"key":"In/3290",
				"place_name":"Haridwar",
				"city_name":"Himachal Pradesh"
				}

			response=self.client.post(url1, data, format='json')
			self.assertEqual(response.status_code, 400)
			selfdb=spatialData.objects.all()
			self.assertEqual(selfdb.count(), 0)


			data={
				"latitude":9.66,
				"longitude":-186.77,
				"key":"In/3290",
				"place_name":"Haridwar",
				"city_name":"Himachal Pradesh"
				}

			response=self.client.post(url1, data, format='json')
			self.assertEqual(response.status_code, 400)
			selfdb=spatialData.objects.all()
			self.assertEqual(selfdb.count(), 0)


			data={
				"key":"In/3290",
				"latitude":9.66,
				"longitude":-156.77,
				"place_name":"Haridwar",
				"city_name":"Himachal Pradesh"
				}

			response=self.client.post(url1, data, format='json')
			self.assertEqual(response.status_code, 400)
			selfdb=spatialData.objects.all()
			self.assertEqual(selfdb.count(), 0)



#For the Two Get Api's Of Interview Question 2
class Interview2APITestCase(APITestCase):
	# def setUp(self):
	# 	geojson.objects.create(location_name="dffd",latitude=23.44,longitude=45.45)

	def test_get_method_Self_Success(self):
		url1=""
		url="http://127.0.0.1:8000/get_using_self"
		testArray=SecondApiTestDataSuccess()

		for i in testArray:
			url1=url+i
			response=self.client.get(url1)
			self.assertEqual(response.status_code, 200)


	def test_get_method_Postgres_Success(self):
		url1=""
		url="http://127.0.0.1:8000/get_using_Postgres"
		testArray=SecondApiTestDataSuccess()

		for i in testArray:
			url1=url+i
			response=self.client.get(url1)
			self.assertEqual(response.status_code, 200)

	def test_get_method_Self_Fail(self):
		url1=""
		url="http://127.0.0.1:8000/get_using_self"
		testArray=SecondApiTestDataFail()

		for i in testArray:
			url1=url+i
			response=self.client.get(url1)
			# print(response, url1, response.status_code)
			self.assertEqual(response.status_code, 203)


	def test_get_method_Postgres_Fail(self):
		url1=""
		url="http://127.0.0.1:8000/get_using_Postgres"
		testArray=SecondApiTestDataFail()

		for i in testArray:
			url1=url+i
			response=self.client.get(url1)
			self.assertEqual(response.status_code, 203)




#For The Get Api Of Interview Question 3
class Interview3APITestCase(APITestCase):

	def test_get_method_Success(self):
		url1=""
		url="http://127.0.0.1:8000/latitude_longitude"
		testArray=ThirdApiTestDataSuccess()

		for i in testArray:
			url1=url+i
			response=self.client.get(url1)
			self.assertEqual(response.status_code, 200)
			print("Url is:- ",url1)


	def test_get_method_Fail(self):
		url1=""
		url="http://127.0.0.1:8000/latitude_longitude"
		testArray=ThirdApiTestDataFail()

		for i in testArray:
			url1=url+i
			response=self.client.get(url1)
			self.assertEqual(response.status_code, 203)