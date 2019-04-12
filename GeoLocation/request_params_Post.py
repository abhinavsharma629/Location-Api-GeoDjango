import re
def requestParamPost(request):
	city=""
	latitude=""
	longitude=""
	pincode=""
	address=""
	c=0

	if(len(request)<5):
			return ('Insufficient Details')

	elif(len(request)>5):
		return ('Wrong Data')

	else:
			for i,j in request.items():
				if(c==0):
					
					try:
						if(request[i]=="" or (not ((float)(request[i])>=-90 and (float)(request[i])<=90))):
							return ('Latitude Not Found')
						else:
							latitude=request[i]
						#print("yes")
						
					except:
						#print("no")
						return ('Latitude Not Found')
						#break
				elif(c==1):
					#latitude=request.query_params[i]
					try:
						#print("yes1")
						if(request[i]=="" or (not ((float)(request[i])>=-180 and (float)(request[i])<=180))):
							return ('Longitude Not Found')
						else:
							longitude=request[i]
					except:
						#print("no1")
						return ('Longitude Not Found')
						#break
				elif(c==2):
					# longitude=request.query_params[i]
					try:
						if(request[i]==""):
							return ('Pincode Not Found')
						else:
							#print("yes2")
							pincode=request[i]
					except:
						#print("no2")
						return ('Pincode Not Found')
						#break
				elif(c==3):
					# longitude=request.query_params[i]
					try:
						if(request[i]==""):
							return ('Address Not Found')
						else:
							#print("yes2")
							address=request[i]
					except:
						#print("no2")
						return ('Address Not Found')
						#break
				else:
					# longitude=request.query_params[i]
					try:
						if(request[i]=="" or (not re.search(('[a-zA-Z]+'), request[i]))):
							return ('City Not Found')
						else:
							#print("yes2")
							city=request[i]
					except:
						#print("no2")
						return ('City Not Found')
						#break
				c+=1
	return (str(latitude)+','+str(longitude)+','+str(pincode)+','+str(address)+','+str(city))