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
from datetime import datetime

from django.http import JsonResponse



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
from inspect_accept_report_2 import InsepectionAndAcceptanceReceipt_2
from items import Items
from supply import Supply
from office import Offices
from requisition_issuance_slip import RequisitionAndIssuanceSlip
from office import Offices
from tasks import Tasks

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
taskClass = Tasks()


#dirreq = dirname(dirname(abspath(__file__)))
#sys.path.append('{}\SuperUser\static\src'.format(dirreq))

from SuperUser.forms import PhotoForm
from SuperUser.models import Photo



def index(request):
	
	loopRef = genLoopRangeString(5, [('rr','tt','yy','uu'),('ii','qq','ww'),('ss','dd')] )
	return setReponse(request, 'requisitioner/index_new.html', [('rr','tt','yy','uu'),('ii','qq','ww'),('ss','dd')],[(loopRef,),],[],[],[],{})

def search(request):
	

	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)

	reference = request.POST.get('search_input','')

	result = f.requiSearch(reference, logDetails[0][1])


	return setReponse(request, 'requisitioner/search.html', result,[],[],[],[],{})


def profile(request):	
	
	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)

	unameData = u.getUnameFromID(logDetails[0][1])
	userdata = u.getUserDetails(unameData[0][0])
	empdata = e.getEmployeeDetails(logDetails[0][1])
	offDetails = offClass.getOfficeDetails(empdata[0][4])
	allPRNum = len(preq.getAllPRbyID(logDetails[0][1]))
	parStat = f.getPARStat(logDetails[0][1])

	transList = taskClass.getTransOfPersonnel(logDetails[0][1])

	return setReponse(request, 'requisitioner/profile.html',userdata,[(allPRNum,offDetails[1]),parStat],empdata, [transList,],[],{})


def updateProfilePic(request):
	
	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)

	form = PhotoForm(request.POST, request.FILES)
		
	if form.is_valid():
		photo = form.save()
		data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
		e.updateEmpPic(photo.file.name, logDetails[0][1])

	else:
		data = {'is_valid': False}

	return JsonResponse(data)


def inquire(request):
	
	return setReponse(request, 'requisitioner/inq_items.html',[],[],[],[],[],{})

def ris(request):

	
	toPageData = []

	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)


	risList = risClass.getAllRISbyID(logDetails[0][1])

	for x in risList:
		risDetails = risClass.getRISDetails(x[0])
		print(risDetails)
		toPageData = toPageData + [ risDetails[0]+(str(x[0]).replace('-','_'),),]



	return setReponse(request, 'requisitioner/ris.html', toPageData,[],[],[],[],{})	

def risDetails(request):

	slipnum = getSessionData(request, 'theSlipNum')

	risDetails2 = risClass.getRISDetails(slipnum)
	
	print(risDetails2)
	
	reqOfficerDetails = e.getEmployeeDetails(risDetails2[0][4])
	reqOfficerName = reqOfficerDetails[0][6]+' '+reqOfficerDetails[0][1] +' ' + reqOfficerDetails[0][7]+' '+ reqOfficerDetails[0][2]+' ,'+reqOfficerDetails[0][8]
	reqOff = offClass.getOfficeDetails(reqOfficerDetails[0][4])
	risItems = risClass.getItemByRIS(slipnum)

	return setReponse(request, 'requisitioner/ris_details.html',risDetails2, [(reqOfficerName, reqOff[1])], risItems, [],[],{})

def risDetailsFromRef(request, refData):

	#slipnum = getSessionData(request, 'theSlipNum')
	slipnum = refData.replace('_','-')
	
	risDetails2 = risClass.getRISDetails(slipnum)
	
	print(risDetails2)
	
	reqOfficerDetails = e.getEmployeeDetails(risDetails2[0][4])
	reqOfficerName = reqOfficerDetails[0][6]+' '+reqOfficerDetails[0][1] +' ' + reqOfficerDetails[0][7]+' '+ reqOfficerDetails[0][2]+' ,'+reqOfficerDetails[0][8]
	reqOff = offClass.getOfficeDetails(reqOfficerDetails[0][4])
	risItems = risClass.getItemByRIS(slipnum)

	return setReponse(request, 'requisitioner/ris_details.html',risDetails2, [(reqOfficerName, reqOff[1])], risItems, [],[],{})

def displayRISDetails(request):
    
    slipnum = request.POST.get('slipNumButton', '')
    setSessionData(request, 'theSlipNum', slipnum)
    
    return HttpResponseRedirect('/requisitioner/ris/details/') 



def create_pr(request):

	createPRCookie = ''
	response = None

	if isSessionValueEmpty(request,'createPRCookie'):
		response = setReponse(request, 'requisitioner/create_pr_new.html',[],[],[],[('#','$String1|!String2;!String3;!String4;','Unit','Qty', 'Price', 'Total'),('#','$String1|!String2;!String3;!String4;','Unit','Qty','Price', 'Total'),('#','$String1|!String2;!String3;!String4;','Unit','Qty', 'Price', 'Total'),('#','String1','Unit','Qty', 'Price', 'Total')],[],{})
	
	else:
		
		createPRCookie = getSessionData(request, 'createPRCookie')
		prDetails = preq.getPRDetails(createPRCookie)
		prItems = preq.getItemByPR(createPRCookie)
		prTotalCost = preq.getTotalCostofPR(prItems)

		del request.session['createPRCookie']
		
		response = setReponse(request, 'requisitioner/create_pr_new.html', prDetails, prItems,[(len(prItems), prTotalCost),],[('$String1;String2;String3;String4;',),],[],{})

	return response

def create_pr_from_ex_pr(request, refData):

	refString = refData.replace('_','-')
	
	prDetails = preq.getPRDetails(refString)
	prItems = preq.getItemByPR(refString)
	prTotalCost = preq.getTotalCostofPR(prItems)

	response = setReponse(request, 'requisitioner/create_pr_new_from_ex_pr.html', prDetails, prItems,[(len(prItems), prTotalCost),],[('$String1;String2;String3;String4;',),],[],{})

	return response

def pr(request):
	
	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)
	
	prList = f.getPRListByPersonnel(logDetails[0][1])
	prStat = f.getReqStat(logDetails[0][1])

	return setReponse(request, 'requisitioner/pr.html', prList, prStat,[],[],[],{})

def offpr(request):
	
	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)
	empDetails = e.getEmployeeDetails(logDetails[0][1])
	
	prList = f.getPRlistByOffice(empDetails[0][4], 'staff')
	prStat = f.getReqStat(logDetails[0][1])

	return setReponse(request, 'requisitioner/off_pr.html', prList, prStat,[],[],[],{})	

def off_pr_details(request, refData):

	refString = refData.replace('_','-')
	
	prDetails = f.getPRCompleteDetails(refString, 'staff')
	prItems = preq.getItemByPR(refString)
	prTotalCost = preq.getTotalCostofPR(prItems)

	response = setReponse(request, 'requisitioner/off_pr_details.html', prDetails, prItems,[(len(prItems), prTotalCost),],[('$String1;String2;String3;String4;',),],[],{})

	return response

def theOffDetails(request):
	
	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)
	empDetails = e.getEmployeeDetails(logDetails[0][1])
	
	offid = empDetails[0][4]
	
	offDetails = off.getOfficeDetails(offid)
	subOffName = off.getOfficeDetails(offDetails[5])

	offTotalValue = 0
	offTotalValueQTY = 0
	offTotalPAR = 0

	empList = e.getEmployeeByOff(offid)
	empListToPage = []

	for xy in empList:

		allPARTotal = 0
		allPARQuantity = 0
		parList = prop.getPAROFID(xy[0])
		empD = e.getEmployeeDetails(xy[0])

		for x in parList:
			parTotal = prop.getPARTotal(prop.getPARItems(x[0]))
			parItemTotal = prop.getTotalQuantityOfPAR(prop.getPARItems(x[0]))

			allPARTotal = allPARTotal + parTotal
			allPARQuantity = allPARQuantity + parItemTotal

		empListToPage = empListToPage + [empD[0]+(allPARTotal, allPARQuantity),]

		offTotalPAR = offTotalPAR + len(parList)
		offTotalValueQTY = offTotalValueQTY + allPARQuantity
		offTotalValue = offTotalValue + allPARTotal

	empDetails = e.getEmployeeDetails(offDetails[3])

	supplyList = f.getAllSuppliesWithOfficeInfo(offid)
	offitems = f.getItemsByOffice( offid)

	return setReponse(request, 'requisitioner/off_details.html', [offDetails, empDetails[0], (offTotalPAR, offTotalValueQTY,offTotalValue,''), subOffName, empListToPage], [supplyList, offitems], [], [], [],{})


def accounts(request):

	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)

	parStat = f.getPARStat(logDetails[0][1])

	parList = prop.getPAROFID(logDetails[0][1])
	outputItemList = []

	if parList != []:
		
		for x in parList:
			
			parDetails = prop.getPARDetails(x[0])
			parItems = prop.getPARItems(x[0])
			parTotal = prop.getPARTotal(parItems)
			parTotalQuantity = prop.getTotalQuantityOfPAR(parItems)
			intoData = parDetails[0] + (parTotal, parTotalQuantity, str(x[0]).replace('-','_'))
			
			outputItemList = outputItemList + [(intoData),]

	print(outputItemList)

	return setReponse(request, 'requisitioner/accounts.html', outputItemList, [parStat,],[],[],[],{})

def items(request):

	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)

	parStat = f.getPARStat(logDetails[0][1])

	parList = prop.getPAROFID(logDetails[0][1])

	itemList = f.getItemsByPersonelID(logDetails[0][1])

	return setReponse(request, 'requisitioner/items.html', itemList, [parStat,],[],[],[],{})


def abstract(request):

	theCookieValue = ''

	if isSessionValueEmpty(request,'prCookie'):
		theCookieValue = request.POST.get('reqNum','')
	
	else:
		
		theCookieValue = getSessionData(request, 'prCookie')		
		absDetails = abc.getAbstractDetails(theCookieValue)
		rqDetails = reqQ.getRequestDetails(theCookieValue)
		suppliers = abc.getSuppliers(theCookieValue)
		prDetails = preq.getPRDetails(preq.getReqNumFromPR(rqDetails[0][1])[0][0])

		suppliersComplete = []

		for x in suppliers:
			supDetails = supp.getSupllierDetails(x[0])
			suppliersComplete = suppliersComplete + supDetails

		abstractItems = abc.getAbstractItems(theCookieValue)
		toPageItems = []	
			
		for x in abstractItems:
			
			pageItem = [(x[1], x[2]),]
			

			check = None
			theLowestIDX = None

			for idx, y in enumerate(suppliers):
				
				suppBid = abc.getSupplierBid(theCookieValue, x[1], y[0])
				if check is None:
					check = suppBid
					theLowestIDX = idx + 1

				else:
					if suppBid < check:
					   check = suppBid
					   theLowestIDX = idx + 1
										
			
				suppItemBid = abc.getSupplierItemBid(theCookieValue, x[1], y[0])
				pageItem = pageItem + [(y[0], suppBid, suppItemBid, False),]
			
			theTuple = pageItem[theLowestIDX]
			theListEqui = list(theTuple)
			theListEqui[3] = True

			theTupleEqui = tuple(theListEqui)
			pageItem[theLowestIDX] = theTupleEqui


			toPageItems = toPageItems + [pageItem,]	


	return setReponse(request, 'requisitioner/abstract.html', absDetails, suppliersComplete, toPageItems, prDetails,[],{})

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
		prItemstoPage = []
		for x in prItems:
			
			descripString = str(x[2])
	
			if "$" in descripString :

				arr = descripString.split('$')
				print(arr)

				prItemstoPage = prItemstoPage + [(x[0],x[1],arr[0],x[3],x[4],x[5],x[6]),]


				for y in range(1,len(arr)):
					prItemstoPage = prItemstoPage + [('','',arr[y],'','','',''),]

			else:
				prItemstoPage = prItemstoPage + [x]	

		totalCostOfPR = preq.getTotalCostofPR(prItems)
		prStat = f.getPRStatus(theCookieValue)
		prLocDetails = preq.getPRLocDetails(theCookieValue)


		print(prItemstoPage)

		loopRef = genLoopRangeString(18, prItems)

	response = setReponse(request, 'requisitioner/pr_details.html', prDetails, prItemstoPage,[(totalCostOfPR,'', loopRef),],[chanData[0],employeeData[0]],[(prLocDetails[0],)],prStat)
	
	return response

def prDetails_WithRef(request, refData):
	
	theCookieValue = ''
	theCookieValue = ''
	prDetails = []
	prItems = []
	totalCostOfPR = 0

	
	theCookieValue = refData.replace('_','-')
	theUserCookieValue = getSessionData(request, 'theCookie')
		
	logDetails = l.getLogDetails(theUserCookieValue)
	unameData = u.getUnameFromID(logDetails[0][1]) 
	userdata = u.getUserDetails(unameData[0][0])
	employeeData = e.getEmployeeDetails(userdata[0][2])

	chanID = kp.getChancellor()
	chanData = e.getEmployeeDetails(chanID)



	prDetails = preq.getPRDetails(theCookieValue)
	prItems = preq.getItemByPR(theCookieValue)
	prItemstoPage = []
	for x in prItems:
			
		descripString = str(x[2])
	
		if "$" in descripString :

			arr = descripString.split('$')
			
			prItemstoPage = prItemstoPage + [(x[0],x[1],arr[0],x[3],x[4],x[5],x[6]),]


			for y in range(1,len(arr)):
				prItemstoPage = prItemstoPage + [('','',arr[y],'','','',''),]

		else:
			prItemstoPage = prItemstoPage + [x]	

	totalCostOfPR = preq.getTotalCostofPR(prItems)
	prStat = f.getPRStatus(theCookieValue)
	prLocDetails = preq.getPRLocDetails(theCookieValue)
	prPOTimeline = preq.getProCTimeLineDetails(theCookieValue)
	iarInfoToPage = ()
	acctInfoToPage = ()


	if prPOTimeline[0][12] != None:
		iarList = insp.getAllIARNumFromRef(prPOTimeline[0][12])
		
		if iarList != None:

			if len(iarList) == 1:
				iarDetails = insp.getIARDetails(iarList[0][0])
				receiveDate = iarDetails[0][10]
				delRemarks = iarDetails[0][12]

				totalIARItems = insp.getIARQtyOfItems(iarList[0][0])
				totalAvItems = insp.getQtyOfAvailableItems(iarList[0][0])

				tranferStatus = False

				if totalAvItems[0][0] == 0:
					tranferStatus = True

				if prDetails[0][3] == 'Equipment':
					proStatus = insp.getProStatusOfIARItems(prPOTimeline[0][12])

					iarInfoToPage = (True, receiveDate, delRemarks, proStatus)
					acctInfoToPage = (tranferStatus, totalIARItems[0][0], totalIARItems[0][0] - totalAvItems[0][0])

				else:
					iarInfoToPage = (True, receiveDate, delRemarks, True)

			else:	

				latRecDate = insp.getLatestDelDate(prPOTimeline[0][12])
				delRemarks = insp.getDelStatusForMultiIAROfAPO(prPOTimeline[0][12])
				proStatus = insp.getProStatusOfIARItems(prPOTimeline[0][12])
				
				totalIARItems = 0
				totalAvItems = 0

				for x in iarList:
					xTotalIARItems = insp.getIARQtyOfItems(x[0])[0][0]
					
					if xTotalIARItems != None:

						totalIARItems = totalIARItems + xTotalIARItems
						totalAvItems = totalAvItems + insp.getQtyOfAvailableItems(x[0])[0][0]
					
				tranferStatus = False
				startTransfer = False

				if totalAvItems == 0:
					tranferStatus = True

				if totalAvItems != totalIARItems:
					startTransfer =	True
					
				
				if prDetails[0][3] == 'Equipment':
					proStatus = insp.getProStatusOfIARItems(prPOTimeline[0][12])

					iarInfoToPage = (False, latRecDate, delRemarks, proStatus)	
					acctInfoToPage = (tranferStatus, totalIARItems, totalIARItems - totalAvItems, startTransfer)	

				else:
					iarInfoToPage = (True, receiveDate, delRemarks, True)

				
				

	loopRef = genLoopRangeString(18, prItems)

	response = setReponse(request, 'requisitioner/pr_details.html', [prDetails[0]], prItemstoPage,[(totalCostOfPR,'', loopRef),],[chanData[0],employeeData[0]],[prLocDetails[0],prPOTimeline[0], iarInfoToPage, acctInfoToPage],prStat)
	
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
		poDetails = pord.getPODetails(parDetails[0][6])
		#parItems = prop.getPARItems(theCookieValue)
		parTotal = prop.getPARTotal(parItems)
		empDetails = e.getEmployeeDetails(parDetails[0][4])
		offHeadId  = off.getOfficeHeadFromOffice('SMO')
		offHeadEmpDetails = e.getEmployeeDetails(offHeadId[0][0])

		receiveFrom = offHeadEmpDetails[0][6]+" "+offHeadEmpDetails[0][1]+" "+offHeadEmpDetails[0][7]+" "+offHeadEmpDetails[0][2]+", "+offHeadEmpDetails[0][8]
		dateRec = parDetails[0][5]
		dateInterval = datetime.now() - datetime(dateRec.year, dateRec.month, dateRec.day)
		dayInt = dateInterval.days

		intYears = int(dayInt / 365)
		intMonths = int((dayInt % 365) / 30)
		intDays = int((dayInt % 365) % 30)

		stringInt =  str(intYears)+" years, "+str(intMonths)+" months, "+str(intDays)+" days"
		
		if intYears == 0:
			stringInt = str(intMonths)+" months, "+str(intDays)+" days"
		
		if intMonths == 0:
			stringInt = str(intDays)+" days"
		
		parItems = f.getPARListItems(theCookieValue)
		

	response = setReponse(request, 'requisitioner/par_details.html', parDetails, parItems,[(parTotal,receiveFrom, stringInt),],poDetails,[],{})
	return response

def parDetailsfromRef(request, refData):
	
	theCookieValue = ''
	parDetails = []
	parItems = []
	totalCostOfPR = 0

	
	theCookieValue = refData.replace('_','-')
	parDetails = prop.getPARDetails(theCookieValue)
	poDetails = pord.getPODetails(parDetails[0][6])
		#parItems = prop.getPARItems(theCookieValue)
	
	empDetails = e.getEmployeeDetails(parDetails[0][4])
	offHeadId  = off.getOfficeHeadFromOffice('SMO')
	offHeadEmpDetails = e.getEmployeeDetails(offHeadId[0][0])

	receiveFrom = offHeadEmpDetails[0][6]+" "+offHeadEmpDetails[0][1]+" "+offHeadEmpDetails[0][7]+" "+offHeadEmpDetails[0][2]+", "+offHeadEmpDetails[0][8]
	dateRec = parDetails[0][5]
	dateInterval = datetime.now() - datetime(dateRec.year, dateRec.month, dateRec.day)
	dayInt = dateInterval.days

	intYears = int(dayInt / 365)
	intMonths = int((dayInt % 365) / 30)
	intDays = int((dayInt % 365) % 30)
	
	stringInt =  str(intYears)+" years, "+str(intMonths)+" months, "+str(intDays)+" days"
		
	if intYears == 0:
		stringInt = str(intMonths)+" months, "+str(intDays)+" days"
		
	if intMonths == 0:
		stringInt = str(intDays)+" days"
		
	parItems = f.getPARListItems(theCookieValue)
	parTotal = prop.getPARItemAmountTotal(theCookieValue)
		

	response = setReponse(request, 'requisitioner/par_details.html', parDetails, parItems,[(parTotal,receiveFrom, stringInt),],poDetails,[],{})
	
	return response
	
	

def addPr(request):
	
	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)
	purpose = ''
	reqnum = f.generatePRNum()
	itemList = {}

	if request.method == 'POST':
		
		itemList = json.loads(request.POST.get('theMatrix'))
		purpose = request.POST['purpose']
		prType = request.POST['type']

	
	f.createPR(reqnum, purpose, prType, logDetails[0][1], itemList)

	


	return HttpResponse(json.dumps({'reqNum':reqnum.replace('-','_')}), content_type="application/json")

def decideacceptpr(request):
	
	notifValue = getSessionData(request, 'notifnum')
	
	if request.method == 'POST':
		
		itemList = json.loads(request.POST.get('theMatrix'))
		purpose = request.POST['purpose']
		prType = request.POST['type']
		isEdit = request.POST['isEdit']
		reqnum = request.POST['reqnum']
		decicion = request.POST['decicion']

		print("+++++++++++++++++++++++++++++++++")
		print(decicion)
		print(type(decicion))

		f.acceptPR(reqnum, purpose, '', itemList, isEdit, decicion)
		n.updateNotif(notifValue)

	return HttpResponse('')

def holdCancelPR(request):
	
	
	if request.method == 'POST':
		
		reqnum = request.POST['reqnum']
		decision = request.POST['decicion']

		print("Desicion ============")
		print(decision)

		f.holdCancelPR(reqnum, decision)
		
	return HttpResponse('')


def addRIS(request):
	
	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)
	purpose = ''
	reqnum = l.generateLogID()
	itemList = {}

	if request.method == 'POST':
		
		itemList = json.loads(request.POST.get('theMatrix'))
		purpose = request.POST['purpose']

	
	f.createRIS(reqnum, purpose, '', logDetails[0][1], itemList)
	
	return HttpResponse('')

def displayReqDetails(request):
	 
	reqnum = request.POST.get('detailsButton','')
	response = HttpResponseRedirect('/requisitioner/pr/pr_details')

	setSessionData(request, 'prCookie', reqnum)
	return response

def createPRFromRef(request):
	 
	reqnum = request.POST.get('detailsButton','')
	response = HttpResponseRedirect('/requisitioner/create_pr')

	setSessionData(request, 'createPRCookie', reqnum)

	return response


def displayPARDetails(request):
	
	parnum = request.POST.get('details','')
	response = HttpResponseRedirect('/requisitioner/accounts/par_details/')

	setSessionData(request, 'parCookie', parnum)
	return response

def notifications(request):
	 
	 notifNum = request.POST.get('d', '')
	 notifDetails = n.getNotifDetails(notifNum)

	 notifRefType = notifDetails[0][10]
	 notifRef = notifDetails[0][5]
	 
	 print(notifRef)
	 
	 response = None

	 if notifRefType == 'pr':

	 	setSessionData(request, 'prCookie', notifRef)

	 	response = HttpResponseRedirect('/requisitioner/pr/pr_details')
	 	n.updateNotif(notifNum)

	 if notifRefType == 'abstract':

	 	setSessionData(request, 'prCookie', notifRef)

	 	response = HttpResponseRedirect('/requisitioner/abstract_details')	

	 if notifRefType == 'ris':

	 	setSessionData(request, 'theSlipNum', notifRef)

	 	response = HttpResponseRedirect('/requisitioner/ris/details/')	
	 
	 if notifRefType == 'par':

	 	setSessionData(request, 'parCookie', notifRef)

	 	response = HttpResponseRedirect('/requisitioner/accounts/par_details/')	
	 	n.updateNotif(notifNum)
  	
	 
	 return response

def updateAbstract(request):
	
	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)
	
	if request.method == 'POST':
		
		canvnum = request.POST['canvnum']
		recomend = request.POST['recomend']
		chosenBids = json.loads(request.POST.get('chosenBid'))
		

		f.updateAbstractBids(canvnum, chosenBids, recomend)

		notifNum = n.getNotifFromDataWithRef(canvnum, logDetails[0][1],'abstract')
		n.updateNotif(notifNum[0][0])
	
	setSessionData(request, 'acCookie', canvnum)	
	return HttpResponseRedirect('/requisitioner/pr/')

def generatePDF(request):

		theCookieValue = getSessionData(request, 'theCookie')

		logDetails = l.getLogDetails(theCookieValue)
		unameData = u.getUnameFromID(logDetails[0][1]) 
		userdata = u.getUserDetails(unameData[0][0])

		employeeData = e.getEmployeeDetails(userdata[0][2])

		loopRef = genLoopRangeString(35, [])
	
		return renderPDF(request, 'pdf_templates/doc-prTest.html', userdata, employeeData, [], [], 'purchase_request2', loopRef, 'legal')

def generatePRDocument(request):
		
		prnum = request.POST.get('reqNumB','')
		

		theCookieValue = getSessionData(request, 'theCookie')

		logDetails = l.getLogDetails(theCookieValue)

		unameData = u.getUnameFromID(logDetails[0][1]) 
		userdata = u.getUserDetails(unameData[0][0])

		chanID = kp.getChancellor()
		chanData = e.getEmployeeDetails(chanID)		

		prDetails = preq.getPRDetails(prnum)
		prItems = preq.getItemByPR(prnum)
		prItemstoPage = []
		for x in prItems:
			
			descripString = str(x[2])
	
			if "$" in descripString :

				arr = descripString.split('$')
				print(arr)

				prItemstoPage = prItemstoPage + [(x[0],x[1],arr[0],x[3],x[4],x[5],x[6]),]


				for y in range(1,len(arr)):
					prItemstoPage = prItemstoPage + [('','',arr[y],'','','',''),]

			else:
				prItemstoPage = prItemstoPage + [x]	
		prTotal = preq.getTotalCostofPR(prItems)

		employeeData = e.getEmployeeDetails(userdata[0][2])

		offName = offClass.getOfficeDetails(employeeData[0][4])
		loopRef = genLoopRangeString(26, prItemstoPage)

	
		return renderPDF(request, 'pdf_templates/doc-prTest.html', [(prTotal,),], 
																	[(chanData[0][1].upper(), chanData[0][2].upper(), chanData[0][3], chanData[0][6].upper(),chanData[0][7].upper(),),
																	 (employeeData[0][1].upper(),employeeData[0][2].upper(), employeeData[0][3], offName[0][1], employeeData[0][6].upper(),employeeData[0][7].upper(),employeeData[0][8].upper(),),
																	 prDetails[0]], 
																	 [(str(prDetails[0][11]),),], 
																	 prItemstoPage, 
																	 'pr_'+str(prDetails[0][1]), 
																	 loopRef, 
																	 'legal')

def generatePRDocumentFromRef(request, refData):
		
		prnum = refData.replace('_','-')
		
		theCookieValue = getSessionData(request, 'theCookie')

		logDetails = l.getLogDetails(theCookieValue)

		unameData = u.getUnameFromID(logDetails[0][1]) 
		userdata = u.getUserDetails(unameData[0][0])

		chanID = kp.getChancellor()
		chanData = e.getEmployeeDetails(chanID)		

		prDetails = preq.getPRDetails(prnum)
		prItems = preq.getItemByPR(prnum)
		prItemstoPage = []
		
		for x in prItems:
			
			descripString = str(x[2])
	
			if "$" in descripString :

				arr = descripString.split('$')
				print(arr)

				prItemstoPage = prItemstoPage + [(x[0],x[1],arr[0],x[3],x[4],x[5],x[6]),]


				for y in range(1,len(arr)):
					prItemstoPage = prItemstoPage + [('','',arr[y],'','','',''),]

			else:
				prItemstoPage = prItemstoPage + [x]	
		prTotal = preq.getTotalCostofPR(prItems)

		employeeData = e.getEmployeeDetails(userdata[0][2])

		offName = offClass.getOfficeDetails(employeeData[0][4])
		loopRef = genLoopRangeString(23, prItemstoPage)


	
		return renderPDF(request, 'pdf_templates/doc-prTest.html', [(prTotal,),], 
																	[(chanData[0][1].upper(), chanData[0][2].upper(), chanData[0][3], chanData[0][6].upper(),chanData[0][7].upper(),),
																	 (employeeData[0][1].upper(),employeeData[0][2].upper(), employeeData[0][3], offName[1], employeeData[0][6].upper(),employeeData[0][7].upper(),employeeData[0][8].upper(),),
																	 prDetails[0]], 
																	 [(str(prDetails[0][11]),),], 
																	 prItemstoPage, 
																	 'pr_'+str(prDetails[0][5]), 
																	 loopRef, 
																	 'legal')



def generateACDocument(request):
		
	theEmpCookieValue = getSessionData(request, 'theCookie')

	logDetails = l.getLogDetails(theEmpCookieValue)

	employeeData = e.getEmployeeDetails(logDetails[0][1]) 

	theCookieValue = ''

	if isSessionValueEmpty(request,'acCookie'):
		theCookieValue = request.POST.get('reqNum','')
	
	else:
		
		theCookieValue = getSessionData(request, 'acCookie')		
		absDetails = abc.getAbstractDetails(theCookieValue)	
		suppliers = abc.getSuppliers(theCookieValue)

		suppliersComplete = []

		for x in suppliers:
			supDetails = supp.getSupllierDetails(x[0])
			suppliersComplete = suppliersComplete + supDetails

		abstractItems = abc.getAbstractItems(theCookieValue)
		toPageItems = []	
			
		for x in abstractItems:
			
			pageItem = ((x[1], x[2],x[3], x[4]),)
			
			for y in suppliers:
				
				suppBid = abc.getSupplierBid(theCookieValue, x[1], y[0])
				suppItemBid = abc.getSupplierItemBid(theCookieValue, x[1], y[0])
				suppBidSelStat  = abc.getSupplierSelectionStat(theCookieValue, x[1], y[0])


				pageItem = pageItem + ((y[0], suppBid, suppItemBid, suppBidSelStat),)


			toPageItems = toPageItems + [pageItem,]	

		
		loopRef = genLoopRangeString(9, toPageItems)
	
		return renderPDF(request, 'pdf_templates/doc-acTest.html', [employeeData[0], absDetails[0]], suppliersComplete, toPageItems,[], 'ac_'+theCookieValue, loopRef, 'legal landscape')


def generateRISDocument(request):
		
		theCookieValue = getSessionData(request, 'theCookie')
		logDetails = l.getLogDetails(theCookieValue)	
		
		slipnum = getSessionData(request, 'theSlipNum')

		risDetails2 = risClass.getRISDetails(slipnum)
		
		reqOfficerDetails = e.getEmployeeDetails(risDetails2[0][4])
		reqOfficerName = reqOfficerDetails[0][6]+' '+reqOfficerDetails[0][1] +' ' + reqOfficerDetails[0][7]+' '+ reqOfficerDetails[0][2]+' ,'+reqOfficerDetails[0][8]
		reqOff = offClass.getOfficeDetails(reqOfficerDetails[0][4])
		reqDesignation = reqOfficerDetails[0][3] 

		smoHead = offClass.getOfficeHeadFromOffice('SMO')
		appOfficerDetails = e.getEmployeeDetails(smoHead[0][0])
		appOfficerName = appOfficerDetails[0][6]+' '+appOfficerDetails[0][1] +' ' + appOfficerDetails[0][7]+' '+ appOfficerDetails[0][2]+' ,'+appOfficerDetails[0][8]
		appDesignation = appOfficerDetails[0][3] 

		risItems = risClass.getItemByRIS(slipnum)

		loopRef = genLoopRangeString(25, risItems)

		notifNum = n.getNotifFromDataWithRef(slipnum, logDetails[0][1],'ris')
		
		if notifNum != []:
			n.updateNotif(notifNum[0][0])
	
		return renderPDF(request, 'pdf_templates/doc-risTest.html', [(reqOfficerName, reqOff[0], reqDesignation),(appOfficerName, appDesignation), (risDetails2[0][1], str(risDetails2[0][7]), risDetails2[0][2])], risItems, [], [], 'ris_'+ risDetails2[0][1], loopRef, '')


def testingLang(request):
	
	return render_to_string('pdf_templates/doc-prTest.html')


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
        	'dept': deptDetails[1],
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
        	'acctype': acctType,
        	'propic': employeeData[0][9]
        
		}
		
		
		
		if any( 5 == code for code in acctType):
			response = HttpResponse('Page not Found')

		else:
			
			response = render(request, outputPage, c)
			setSessionData(request, 'theCookie', cookieValue)
		

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

