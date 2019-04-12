import re
def requestparamForGeojson(request):
	latitude=""
	longitude=""
	c=0

	if(len(request)<2):
			return ('Insufficient Details')

	elif(len(request)>2):
		return ('Wrong Data')

	else:

			for i,j in request.items():

				if(c==0):
					try:
						if(request[i]=="" or re.search(('[a-zA-Z]+'), request[i]) or (not ((float)(request[i])>=-90 and (float)(request[i])<=90))):
							return ('Latitude Not Found')
						else:
							latitude=request[i]
					except:
						return ('Latitude Not Found')
				
				else:
					try:
						if(request[i]=="" or re.search(('[a-zA-Z]+'), request[i]) or (not ((float)(request[i])>=-180 and (float)(request[i])<=180))):
							return ('Longitude Not Found')
						else:
							longitude=request[i]
					except:
						return ('Longitude Not Found')

				c+=1
	return (str(latitude)+','+str(longitude))