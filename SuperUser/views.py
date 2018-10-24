from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.conf import settings
from django.views import View

import tempfile

from weasyprint import HTML, CSS

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import HttpResponse
import json
from os.path import dirname, abspath
import sys
import datetime
from datetime import datetime

from django.http import JsonResponse

from .forms import PhotoForm

from functions import Functions
from user import User
from log import Log
from employees import Employees
from notifications import Notification
from purchase_request import PurchaseRequest
from abstract_of_canvass import AbstractOfCanvass
from suppliers import Suppliers
from property_acc_receipt import PropertyAcceptanceReceipt
from key_positions import KeyPositions
from request_for_quotation import RequestForQuotation
from purchase_order import PurchaseOrder
from inspect_accept_report_2 import InsepectionAndAcceptanceReceipt_2
from items import Items
from supply import Supply
from office import Offices
from requisition_issuance_slip import RequisitionAndIssuanceSlip
from office import Offices

f = Functions()
u = User()
l = Log()
e = Employees()
n = Notification()
preq = PurchaseRequest()
pord = PurchaseOrder()
reqQ = RequestForQuotation()
abc = AbstractOfCanvass()
supp = Suppliers()
prop = PropertyAcceptanceReceipt()
kp = KeyPositions()
insp = InsepectionAndAcceptanceReceipt_2()
itemClass = Items()
supplyClass = Supply()
offClass = Offices()
risClass = RequisitionAndIssuanceSlip()
off = Offices()


def index(request):
	
	loopRef = genLoopRangeString(5, [('rr','tt','yy','uu'),('ii','qq','ww'),('ss','dd')] )
	return setReponse(request, 'super_user/home.html', [('rr','tt','yy','uu'),('ii','qq','ww'),('ss','dd')],[(loopRef,),],[],[],[],{})

def uploadTest(request):
	  
	if request.method == 'POST':
		#orm = FileUploadForm(data=request.POST, files=request.FILES)
		#json.loads(request.POST.get('theMatrix'))

		data = request.FILES.get('file')
		print("File")

		print(data)

	return HttpResponse('')

def search(request):
	

	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)

	reference = request.POST.get('search_input','')

	result = f.requiSearch(reference, logDetails[0][1])


	return setReponse(request, 'requisitioner/search.html', result,[],[],[],[],{})


def users(request):	
	
	userListToPage = []

	userList = u.getAllUsers()

	for x in userList:
		print(x)
		empDetails = e.getEmployeeDetails(x[2])
		print(empDetails)
		userListToPage = userListToPage + [x + (empDetails[0][6]+" "+empDetails[0][1]+" "+empDetails[0][7]+" "+empDetails[0][2]+" "+empDetails[0][8],)]

	return setReponse(request, 'super_user/users.html',userListToPage,[],[],[],[],{})

def keyUsers(request):	
	
	return setReponse(request, 'super_user/users.html',[],[],[],[],[],{})

def offices(request):	
    
    pageData = []

    offices = off.getAllOfficesSorted()

    for offid in offices:
       
        offDetails = off.getOfficeDetails(offid[0])
        empDetails = e.getEmployeeDetails(offDetails[3])
        urlString = (offid[0]).replace('-','_')
       
        pageData = pageData + [ offDetails + (empDetails, urlString) ]

    return setReponse(request, 'super_user/offices.html',pageData,[],[],[],[],{})

def officeDetails(request, refData):	
    
    refString = refData.replace('_','-')
    offDetails = offClass.getOfficeDetails(refString)
    empDetails = []

    if offDetails[3] != None:
   		empDetails = e.getEmployeeDetails(offDetails[3])

    empList = e.getEmployeeByOff(refString)
    empListToPage = []

    print(empDetails)

    for xy in empList:

        empD = e.getEmployeeDetails(xy[0])
        print(u.getUnameFromID(xy[0]))
        userDetails = u.getUserDetails(u.getUnameFromID(xy[0])[0][0])

        empListToPage = empListToPage + [(empD[0], userDetails[0]),]    


    return setReponse(request, 'super_user/office_details.html',[offDetails, empDetails], empListToPage,[],[],[],{})

def employees(request):	
    
    pageData = []

    empIDList = e.getAllEmployeeID()


    for empID in empIDList:
       
        empDetails = e.getEmployeeDetails(empID[0])

        if empDetails[0][4] != '':
        	offDetails = offClass.getOfficeDetails(empDetails[0][4])
        	print(offDetails)
        	pageData = pageData + [empDetails[0]+(str(empID[0]).replace('-','_'),)+offDetails, ]

        else:
        	pageData = pageData + [empDetails[0]+(str(empID[0]).replace('-','_'),), ]

    return setReponse(request, 'super_user/employees.html',pageData,[],[],[],[],{})


def empDetails(request, refData):


	return 	setReponse(request, 'super_user/emp_details.html',[],[],[],[],[],{})

def addEmployee(request):
	 return setReponse(request, 'super_user/add-emp.html',[],[],[],[],[],{})

def addNewEmployee(request):
	
	reqnum = ''
	outputData = {}

	if request.method == 'POST':
		offid = request.POST['offid']
		offname = request.POST['offname']
		offtype = request.POST['offtype']
		
		print('offid: '+offid)

		f.addNewOffice(offid, offname, offtype)

	return HttpResponse('Done')

def addOffice(request):
	
	reqnum = ''
	outputData = {}

	if request.method == 'POST':
		offid = request.POST['offid']
		offname = request.POST['offname']
		offtype = request.POST['offtype']
		
		print('offid: '+offid)

		f.addNewOffice(offid, offname, offtype)

	return HttpResponse('Done')

def updateOfficeHead(request):
	
	reqnum = ''
	outputData = {}

	if request.method == 'POST':
		offid = request.POST['offid']
		idnum = request.POST['idnum']

		print('offid: '+offid)

		f.updateOfficeHead(idnum, offid)

	return HttpResponse('Done')

def updateUserStatus(request):
	

	if request.method == 'POST':
		idnum = request.POST['idnum']

		userDetails = u.getUserDetails(u.getUnameFromID(idnum)[0][0])

		if userDetails[0][5] == False:
			u.updateUserStatus(u.getUnameFromID(idnum)[0][0], 'TRUE')
		
		else:
			u.updateUserStatus(u.getUnameFromID(idnum)[0][0], 'FALSE')

	return HttpResponse('Done')


def updateUserType(request):
	


	if request.method == 'POST':
		idnum = request.POST['idnum']
		accessType = request.POST['accType']

		f.user.updateUserAccessType(idnum, 5, accessType)

	return HttpResponse('Done')

def tranferuser(request):

	if request.method == 'POST':
		idnum = request.POST['idnum']
		offid = request.POST['offid']

		print(idnum)
		print(offid)

		f.emp.transferEmployeeToOffice(idnum, offid)

	return HttpResponse('Done')

def getAllOffices(request):
	offList = off.getAllOfficesSorted()
	outputData = {}
	
	for x in offList:
		offDetails = off.getOfficeDetails(x[0])
		outputData[x[0]] = offDetails[1]

	return HttpResponse(json.dumps(outputData), content_type="application/json")    



def logs(request):	
	return setReponse(request, 'super_user/logs.html',[],[],[],[],[],{})


def cancelPR(request):
	
	reqnum = request.POST.get('detailsButton','')
	f.cancelPR(reqnum)
	
	return HttpResponse('')


#def return_data(request):
	
	#if request.method == 'POST':
    	#return HttpResponse('entered text:' + request.POST['text'])


def checkPass(request):

	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)

	unameData = u.getUnameFromID(logDetails[0][1])
	password = ''
	
	if request.method == 'POST':
		password = request.POST['password']

	chckResult = u.checkUserPass(unameData[0][0], password)

	outMsg = ''

	if chckResult == True:
		outMsg = 'True'

	else:
		outMsg = 'False'

	return HttpResponse(outMsg)	

def changePass(request):
	
	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)

	unameData = u.getUnameFromID(logDetails[0][1])
	password = ''
	
	if request.method == 'POST':
		password = request.POST['password']

	u.updateUserPass(unameData[0][0], password)

	return HttpResponse('')

class BasicUploadView(View):
    
    def get(self, request):
        print(Photo.objects)
        photos_list = Photo.objects.all()
        phh = ""
        try:
            p = Photo.objects.get(file='photos/667262.png')
        except Photo.DoesNotExist:
            print ("Apress isn't in the database yet.")
        else:
            phh = p
            print ("Apress is in the database.")
        
        return render(self.request, 'super_user/home-upload.html', {'photos': photos_list, 'uu':phh})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        
        print(form.is_valid())
        
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

def uploadTest2(request):
        form = PhotoForm(request.POST, request.FILES)
        
        print(form.is_valid())
        
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)



#============================ PR Status Details Functions ==============================================================================

def approvalInfo(request):
	
	reqnum = ''
	outputData = {}

	if request.method == 'POST':
		reqnum = request.POST['reqnum']

	reqDetails  = preq.getPRDetails(reqnum)
	
	outputData = {
			'initappStatus': reqDetails[0][7],
			'appStatus': reqDetails[0][8],
			'appDate': str(reqDetails[0][11]),
			'declineReason': reqDetails[0][9]



	}	
	return HttpResponse(json.dumps(outputData), content_type="application/json")

def canvassInfo(request):
	
	reqnum = ''
	outputData = {}

	if request.method == 'POST':
		reqnum = request.POST['reqnum']

	reqDetails  = preq.getPRDetails(reqnum)
	
	rqNum = reqQ.getReqNumFromRefNum(reqDetails[0][1])
	abcNum = ''
	abcSelStat = False

	if rqNum is None :
		pass
	else:

		abcNum = rqNum
		abcDetails = abc.getAbstractDetails(abcNum)
		abcSelStat = abcDetails[0][5]

	outputData = {
			
			'rqNum':rqNum,
			'abcNum': abcNum,
			'abcStat':abcSelStat,
	}	

	return HttpResponse(json.dumps(outputData), content_type="application/json")


def procInfo(request):
	
	reqnum = ''
	outputData = {}

	if request.method == 'POST':
		reqnum = request.POST['reqnum']

	reqDetails = preq.getPRDetails(reqnum)

	poNum = pord.getPONumFromPRRef(reqDetails[0][1])

	if poNum is None:
		pass

	else:
			
			poDetails = pord.getPODetails(poNum)
			totalCostOfPO = pord.getTotalCostofPO(pord.getItemByPO(poNum))

			outputData = {
								'poNum': poNum,
								'poStat':poDetails[0][9],
								'appDate': str(poDetails[0][16]),
								'total': totalCostOfPO,
			}	
	return HttpResponse(json.dumps(outputData), content_type="application/json")


def delInfo(request):
	
	reqnum = ''
	outputData = {}

	if request.method == 'POST':
		reqnum = request.POST['reqnum']

	reqDetails = preq.getPRDetails(reqnum)
	poNum = pord.getPONumFromPRRef(reqDetails[0][1])
	iarNum = '' 
	
	if poNum is None:
		pass

	else:
			iarNum = insp.getIARNumFromRef(poNum)
			iarDetails = insp.getIARDetails(iarNum) 
			poDetails = pord.getPODetails(poNum)

			outputData = {
								'iarNum': iarNum,
								'iarDelStat': iarDetails[0][9],
								'serveDate': str(poDetails[0][17]),
								'iarDelStat': iarDetails[0][9],
			}

	return HttpResponse(json.dumps(outputData), content_type="application/json")		


def receiveInfo(request):
	
	reqnum = ''
	outputData = {}

	if request.method == 'POST':
		reqnum = request.POST['reqnum']

	reqDetails = preq.getPRDetails(reqnum)
	poNum = pord.getPONumFromPRRef(reqDetails[0][1])
	iarNum = insp.getIARNumFromRef(poNum)

	disburstStatus = insp.checkIARItemsDisburstComplete(iarNum)

	return HttpResponse(disburstStatus)

def findItems(request):
    
	outputData = {}
	reponse = ''

	if request.method == 'POST':
		descripData = request.POST['descripData']
		findResult = itemClass.findItem(descripData)
		
		if findResult == []:
			response = HttpResponse('No Match')
		else:
				
			for x in findResult:

				outputData[x[1]] = {
					'name': str(x[0])
					}

			response = HttpResponse(json.dumps(outputData), content_type="application/json")   		

	return response

def findSupplyItems(request):
    
	outputData = {}
	reponse = ''

	if request.method == 'POST':
		descripData = request.POST['descripData']
		findResult = itemClass.findSupplyItem(descripData)
		
		if findResult == []:
			response = HttpResponse('No Match')
		else:
				
			for x in findResult:

				outputData[x[1]] = {
					'name': str(x[0])
					}

			response = HttpResponse(json.dumps(outputData), content_type="application/json")   		

	return response	

def getItemDetails(request):

	outputData = {}

	if request.method == 'POST':
		inputItemId = request.POST['inputItemId']
		itemDetails = itemClass.getItemDetails(inputItemId)
		
		outputData = {
					'unit':itemDetails[0][4],
					'unitprice':itemDetails[0][5],
					'class': itemDetails[0][3]
					}

	return HttpResponse(json.dumps(outputData), content_type="application/json")   		

def getSupplyAvailability(request):


	outputData = {}

	if request.method == 'POST':


		suppItemID = request.POST['suppItemID']
		itemDetails = itemClass.getItemDetails(suppItemID)

		totalAvailable = supplyClass.getSupplyQuantityFromItemID(suppItemID)

		outputData = {
					'unit':itemDetails[0][4].lower()+'/s',
					'quantity': str(int(totalAvailable)),
					}

	
	return HttpResponse(json.dumps(outputData), content_type="application/json")  	


#========================================================================================================================================

def setSessionData(request, key, value):
    request.session[key] = value
    SESSION_COOKIE_AGE = 60 * 60

def getSessionData(request, key):
    value = request.session[key]
    return value 

def isSessionValueEmpty(request, key):
    if key in request.session:
      return False
    else:
      return True 

def setCookie(reponse, key, value):
    
	reponse.set_cookie(key, value, max_age = 3600)

def isCookieEmpty(request, key):
  
	if key in request.COOKIES:
		return False
	else:
		return True 

def getCookieValue(request, key):
  
	value = request.COOKIES[key]
	return value	

def setReponse(request, outputPage, pageData1, pageData2, pageData3, pageData4, pageData5, dictData1):
	
	if isSessionValueEmpty(request,'theCookie'):
		response = HttpResponseRedirect('/')
	
	else:
		
		theCookieValue = getSessionData(request, 'theCookie')

		logDetails = l.getLogDetails(theCookieValue)
		unameData = u.getUnameFromID(logDetails[0][1]) 
		userdata = u.getUserDetails(unameData[0][0])

		acctType = userdata[0][3]
      
		taskNum = n.getTaskNum(userdata[0][2]) 
		notifNum = n.getNotifNum(userdata[0][2])
		notifs = setNotifDetails(userdata[0][2])
		tasks = setTaskDetails(userdata[0][2])
		
		employeeData = e.getEmployeeDetails(userdata[0][2])
		
		eFname = employeeData[0][1]
		eSname = employeeData[0][2]
		mName = employeeData[0][7]
		sufX = employeeData[0][8]
		prefX = employeeData[0][6]
		designation = employeeData[0][3]
		dept = employeeData[0][4]
		deptDetails = off.getOfficeDetails(dept)
		
		cookieValue = logDetails[0][0]

		c = {

			'name': prefX+' '+eFname+' '+mName+' '+eSname+' '+sufX,
        	'designation': designation,
        	'taskNum': taskNum,
        	'notifNum': notifNum,
        	'notifDetails': notifs,
        	'taskDetails': tasks,
        	'pageData1': pageData1,
        	'pageData2': pageData2,
        	'pageData3': pageData3,
        	'pageData4': pageData4,
        	'pageData5': pageData5,
        	'dictData1': dictData1,
        
		}
		
		
		
		if any( 0 == code for code in acctType):

			response = render(request, outputPage, c)
			setSessionData(request, 'theCookie', cookieValue)

		else:
			response = HttpResponse('Page not Found')
		

	return response	

def renderPDF(request, template, pageData1, pageData2, pageData3, pageData4, pdfName, loopRefNum, csScript):

		c = {
        	
        	'pageData1': pageData1,
        	'pageData2': pageData2,
        	'pageData3': pageData3,
        	'pageData4': pageData4,
        	'loopRef' : loopRefNum,
		
		}

		html_string = render_to_string(template,c)
		
		html = HTML(string=html_string).write_pdf('{}/Project_SMO_Inventory/static/src/mypdf.pdf'.format(dirreq), stylesheets=[CSS(string='@page {size: '+csScript+'; margin:35px;}')]);
		
		fs = FileSystemStorage('{}/Project_SMO_Inventory/static/src/'.format(dirreq))

		with fs.open('mypdf.pdf') as pdf:

			response = HttpResponse(pdf, content_type='application/pdf')
			
			response['Content-Disposition'] = 'attachment; filename="'+pdfName+'.pdf"'
			
			return response	

		return response	


def setNotifDetails(idnum):
    
		outputList = []

		notifList = n.getNotifOfPersonnel(idnum)


		for x in notifList:
	      
			kk = n.getNotifDisplayDetails(x[0])

			notifTimeDate = n.getHotifTimeAndDate(x[0])
	      
			ll = ()
	        
			ll = (x[0],)

			if kk[0][0] == '1':
				ll = ll + ('icon-ok',)
			if kk[0][0] == '2':
				ll = ll + ('icon-legal',)
			if kk[0][0] == '3':
				ll = ll + ('icon-info',)
			if kk[0][0] == '4':
				ll = ll + ('icon-truck',)
			if kk[0][0] == '5':
				ll = ll + ('icon-exclamation',)
	      
			if kk[0][1] == '1':
				ll = ll + ('success',)
			if kk[0][1] == '2':
				ll = ll + ('info',)
			if kk[0][1] == '3':
				ll = ll + ('danger',)
			if kk[0][1] == '4':
				ll = ll + ('warning',)
	      
			ll = ll + (kk[0][2],kk[0][3],kk[0][4],notifTimeDate[0][0], notifTimeDate[0][1],) 
	      
			outputList = outputList + [ll]


		return outputList

def setTaskDetails(idnum):
	    
		outputList = []

		taskList = n.getTaskOfPersonel(idnum)

		for x in taskList:
	     
			kk = n.getNotifDisplayDetails(x[0])
	        
			notifTimeDate = n.getHotifTimeAndDate(x[0])


			ll = ()
	        
			ll = (x[0],)

			if kk[0][0] == '1':
				ll = ll + ('icon-ok',)
			if kk[0][0] == '2':
				ll = ll + ('icon-legal',)
			if kk[0][0] == '3':
				ll = ll + ('icon-info',)
			if kk[0][0] == '4':
				ll = ll + ('icon-truck',)
			if kk[0][0] == '5':
				ll = ll + ('icon-exclamation',)
	      
			if kk[0][1] == '1':
				ll = ll + ('success',)
			if kk[0][1] == '2':
				ll = ll + ('info',)
			if kk[0][1] == '3':
				ll = ll + ('danger',)
			if kk[0][1] == '4':
				ll = ll + ('warning',)
	      
			ll = ll + (kk[0][2],kk[0][3],kk[0][4],notifTimeDate[0][0], notifTimeDate[0][1],) 
	      
			outputList = outputList + [ll]

		return outputList


def genLoopRangeString(maxRange, refList):
	
	output = ''
	maxInRange = maxRange - len(refList)
	
	for x in range(2, maxInRange):
		output = output + 'x'

	return output	

