def SecondApiTestDataFail():
	testArray=[]

	testArray.append("?n1=abc32&n2=34&n3=23")
	testArray.append("?")
	testArray.append("?n1=/?")
	testArray.append("?n1=34")
	testArray.append("?n1=32&n2=fg34?'&n3=23")
	testArray.append("?n1=32&n2=34'&n3=23^$")
	testArray.append("?n1=32&n2=34'&n3=2345")
	testArray.append("?n1=32&n2=3454'&n3=23")
	testArray.append("?n1=34554&n2=34'&n3=2345")
	
	return testArray


def SecondApiTestDataSuccess():
	testArray=[]

	testArray.append("?radius=34&latitude=34&longitude=23")
	testArray.append("?radius=32&latitude=24.9833&longitude=81.0583")
	testArray.append("?n2=32&n1=24.9833&dl=81.0583")
	
	return testArray



def ThirdApiTestDataSuccess():
	testArray=[]
	
	testArray.append("?latitude=76.97596549987793&longitude=28.822755894706358")
	testArray.append("?latitude=72.95393943786621&longitude=19.28108901344132")
	testArray.append("?latitude=77.33078956604004&longitude=28.68840413943363")
	testArray.append("?latitude=72.8252363204956&longitude=18.906814295772328")
	testArray.append("?latitude=72.95290946960449&longitude=19.26950325223538")
	testArray.append("?latitude=72.7913761138916&longitude=18.945826271255413")
	testArray.append("?latitude=77.29381799697876&longitude=28.579735680241054")
	testArray.append("?latitude=77.22633361816405&longitude=28.67530209433848")
	testArray.append("?latitude=76.9740343093872&longitude=28.65737825242822")
	
	return testArray


def ThirdApiTestDataFail():
	testArray=[]
	
	testArray.append("?n2=34&n3=23")
	testArray.append("?&n2=3fd4&n3=23")
	testArray.append("?")
	testArray.append("?n1=/?")
	testArray.append("?n1=34")
	testArray.append("?n2=fg34?'&n3=23")
	testArray.append("?n1=32&n2=34'&n3=23^$")
	testArray.append("?n2=24.9833&n3=81.0583")
	testArray.append("?n2=99.9833&n3=181.0583")
	testArray.append("?n2=93.933&n3=171.0583")
	testArray.append("?n2=-86.9833&n3=-171.0583")
	testArray.append("?n2=-47.833&n3=-100.0583")
	testArray.append("?n2=-23.9833&n3=-11.0583")

	return testArray