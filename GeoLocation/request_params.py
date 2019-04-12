import re
def request_param(request):
	radius=""
	latitude=""
	longitude=""
	c=0

	if(len(request)<3):
			return ('Insufficient Details')

	elif(len(request)>3):
		return ('Wrong Data')

	else:

			for i,j in request.items():
				if(c==0):
					
					try:
						if(request[i]=="" or (not re.search(('[0-9]+'), request[i])) or (float)(request[i])>6378.1):
							return ('Radius Not Found')
						else:
							radius=request[i]
						#print("yes")
						
					except:
						#print("no")
						return ('Radius Not Found')
						#break
				elif(c==1):
					#latitude=request.query_params[i]
					try:
						#print("yes1")
						if(request[i]=="" or (not re.search(('[0-9]+'), request[i])) or (not ((float)(request[i])>=-90 and (float)(request[i])<=90))):
							return ('Latitude Not Found')
						else:
							latitude=request[i]
					except:
						return ('Latitude Not Found')
						#break
				elif(c==2):
					# longitude=request.query_params[i]
					try:
						if(request[i]=="" or (not re.search(('[0-9]+'), request[i])) or (not ((float)(request[i])>=-180 and (float)(request[i])<=180))):
							return ('Longitude Not Found')
						else:
							#print("yes2")
							longitude=request[i]
					except:
						#print("no2")
						return ('Longitude Not Found')
						#break
				c+=1
	return (str(radius)+','+str(latitude)+','+str(longitude))