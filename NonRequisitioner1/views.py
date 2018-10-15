from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.conf import settings

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

dirreq = dirname(dirname(abspath(__file__)))
sys.path.append('{}\Project_SMO_Inventory\static\src'.format(dirreq))

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

f = Functions()
u = User()
l = Log()
e = Employees()
n = Notification()
preq = PurchaseRequest()
abc = AbstractOfCanvass()
supp = Suppliers()
prop = PropertyAcceptanceReceipt()
kp = KeyPositions()


def index(request):
	
	loopRef = genLoopRangeString(5, [('rr','tt','yy','uu'),('ii','qq','ww'),('ss','dd')] )
	return setReponse(request, 'non_requisitioner/index.html', [('rr','tt','yy','uu'),('ii','qq','ww'),('ss','dd')],[(loopRef,),],[],[],[],{})

def profile(request):	
	
	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)

	unameData = u.getUnameFromID(logDetails[0][1])
	
	userdata = u.getUserDetails(unameData[0][0])	

	return setReponse(request, 'non_requisitioner/profile.html',userdata,[],[],[],[],{})


def pr(request):
	
	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)
	
	prList = f.getPRbyID(logDetails[0][1])
	

	return setReponse(request, 'non_requisitioner/pr.html', prList,[],[],[],[],{})

def accounts(request):

	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)

	parList = prop.getPAROFID(logDetails[0][1])
	outputItemList = []

	if parList != []:
		
		for x in parList:
			
			parDetails = prop.getPARDetails(x[0])
			parItems = prop.getPARItems(x[0])
			parTotal = prop.getPARTotal(parItems)
			parTotalQuantity = prop.getTotalQuantityOfPAR(parItems)
			intoData = parDetails[0]+(parTotal,parTotalQuantity,)
			outputItemList = outputItemList + [(intoData),]

	return setReponse(request, 'non_requisitioner/accounts.html', outputItemList,[],[],[],[],{})


def prDetails(request):
	
	theCookieValue = ''
	theCookieValue = ''
	prDetails = []
	prItems = []
	totalCostOfPR = 0

	if isSessionValueEmpty(request,'prCookie'):
		theCookieValue = request.POST.get('reqNum','')
	
	else:
		
		theCookieValue = getSessionData(request, 'prCookie')
		theUserCookieValue = getSessionData(request, 'theCookie')
		
		logDetails = l.getLogDetails(theUserCookieValue)
		unameData = u.getUnameFromID(logDetails[0][1]) 
		userdata = u.getUserDetails(unameData[0][0])
		employeeData = e.getEmployeeDetails(userdata[0][2])

		chanID = kp.getChancellor()
		chanData = e.getEmployeeDetails(chanID)

		prDetails = preq.getPRDetails(theCookieValue)
		prItems = preq.getItemByPR(theCookieValue)
		totalCostOfPR = preq.getTotalCostofPR(prItems)
		prStat = f.getPRStatus(theCookieValue)

		loopRef = genLoopRangeString(18, prItems)
		print("ghghg" + loopRef + str(len(prItems)))

	response = setReponse(request, 'non_requisitioner/pr_details.html', prDetails, prItems,[(totalCostOfPR,'', loopRef),],[chanData[0],employeeData[0]],[],prStat)
	
	return response

def parDetails(request):
	
	theCookieValue = ''
	parDetails = []
	parItems = []
	totalCostOfPR = 0

	if isSessionValueEmpty(request,'parCookie'):
		theCookieValue = request.POST.get('reqNum','')
	
	else:
		theCookieValue = getSessionData(request, 'parCookie')
		parDetails = prop.getPARDetails(theCookieValue)
		parItems = prop.getPARItems(theCookieValue)
		parTotal = prop.getPARTotal(parItems)

	response = setReponse(request, 'non_requisitioner/par_details.html', parDetails, parItems,[(parTotal,),],[],[],{})
	return response


def displayReqDetails(request):
	 
	reqnum = request.POST.get('detailsButton','')
	response = HttpResponseRedirect('/non_requisitioner/pr/pr_details')

	setSessionData(request, 'prCookie', reqnum)
	return response

def displayPARDetails(request):
	
	parnum = request.POST.get('details','')
	response = HttpResponseRedirect('/non_requisitioner/accounts/par_details/')

	setSessionData(request, 'parCookie', parnum)
	return response

def notifications(request):
	 
	 notifNum = request.POST.get('d', '')
	 notifDetails = n.getNotifDetails(notifNum)

	 notifRefType = notifDetails[0][10]
	 notifRef = notifDetails[0][5]
	 
	 setSessionData(request, 'prCookie', notifRef)
	 
	 response = None

	 if notifRefType == 'pr':
	 	response = HttpResponseRedirect('/non_requisitioner/pr/pr_details')
	 	n.updateNotif(notifNum)

	 if notifRefType == 'abstract':
	 	response = HttpResponseRedirect('/non_requisitioner/abstract_details')	

	 
	 
	 return response

def updateAbstract(request):
	
	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)
	
	if request.method == 'POST':
		
		canvnum = request.POST['canvnum']
		
		chosenBids = json.loads(request.POST.get('chosenBid'))
		
		f.updateAbstractBids(canvnum, chosenBids)

		notifNum = n.getNotifFromData(canvnum, logDetails[0][1])
		n.updateNotif(notifNum[0][0])
		
	return HttpResponseRedirect('/non_requisitioner/pr/')
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
	print("Cookie "+value+" on key "+key+" was set")

def isCookieEmpty(request, key):
  
	if key in request.COOKIES:
		print("Cookie is not Empty")
		return False
	else:
		print("Cookie is Empty")
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
		designation = employeeData[0][3]
		dept = employeeData[0][4]
		
		cookieValue = logDetails[0][0]

		c = {

			'fname': eFname,
        	'lname': eSname,
        	'designation': designation,
        	'dept': dept,
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
		
		if any( 5 == code for code in acctType):

			response = render(request, outputPage, c)
			setSessionData(request, 'theCookie', cookieValue)

		else:
			response = HttpResponse('Not Allowed to Access this Page')
	

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
	      
			ll = ll + (kk[0][2],kk[0][3],kk[0][4],) 
	      
			outputList = outputList + [ll]

		return outputList

def setTaskDetails(idnum):
	    
		outputList = []

		taskList = n.getTaskOfPersonel(idnum)

		for x in taskList:
	     
			kk = n.getNotifDisplayDetails(x[0])
	    
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
	      
			ll = ll + (kk[0][2],kk[0][3],kk[0][4],) 
	      
			outputList = outputList + [ll]

		return outputList


def genLoopRangeString(maxRange, refList):
	
	output = ''
	print("in Data "+ str(maxRange) + str(refList))
	maxInRange = maxRange - len(refList)
	print("rr "+str(maxInRange))
	
	for x in range(0, maxInRange):
		output = output + 'x'

	return output	
