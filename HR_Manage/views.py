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
from request_for_quotation import RequestForQuotation
from purchase_order import PurchaseOrder
from inspect_accept_report import InsepectionAndAcceptanceReceipt

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
insp = InsepectionAndAcceptanceReceipt()


def index(request):
	
	
	return setReponse(request, 'requisitioner/login.html',[],[],[],[],[],{})

def search(request):
	
	print("Accessed")

	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)

	reference = request.POST.get('search_input','')

	result = f.requiSearch(reference, logDetails[0][1])


	return setReponse(request, 'requisitioner/search.html', result,[],[],[],[],{})


#========================================================================================================================================


def setReponse(request, outputPage, pageData1, pageData2, pageData3, pageData4, pageData5, dictData1):
	
		c = {

        	'pageData1': pageData1,
        	'pageData2': pageData2,
        	'pageData3': pageData3,
        	'pageData4': pageData4,
        	'pageData5': pageData5,
        	'dictData1': dictData1,
        
		}
		
		

		response = render(request, outputPage, c)

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

		print("list "+ str(outputList))	

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

		print("list "+ str(outputList))
		return outputList


def genLoopRangeString(maxRange, refList):
	
	output = ''
	maxInRange = maxRange - len(refList)
	
	for x in range(2, maxInRange):
		output = output + 'x'

	return output	
