from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import HttpResponse
from os.path import dirname, abspath
import json
import json
from os.path import dirname, abspath
import sys
import datetime


from weasyprint import HTML, CSS

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string

dirreq = dirname(dirname(abspath(__file__)))
sys.path.append('{}\Project_SMO_Inventory\static\src'.format(dirreq))

from functions import Functions
from user import User
from log import Log
from employees import Employees
from notifications import Notification
from inspect_accept_report import InsepectionAndAcceptanceReceipt
from purchase_order import PurchaseOrder
from purchase_request import PurchaseRequest
from property_acc_receipt import PropertyAcceptanceReceipt
from office import Offices
from key_positions import KeyPositions
from suppliers import Suppliers
from items import Items
from equipment import Equipment


f = Functions()
u = User()
l = Log()
e = Employees()
n = Notification()
ins = InsepectionAndAcceptanceReceipt()
pOrd = PurchaseOrder()
preq = PurchaseRequest()
propAR = PropertyAcceptanceReceipt()
off = Offices()
kp = KeyPositions()
suppl = Suppliers()
itemC = Items()
equip = Equipment()

theLocHead = 'approving_office'
urlHead = '/approving_officer'

dynamicStringData = ''
dynamicObjectData = None
dynamicIntData = 0
offListData = None

def index(request):

	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)

	chancellor = kp.getChancellor()
	vcaf = kp.getVCAF()

	pendingInitPRs = preq.getAllInitPendingPR()
	pendingPRs = preq.getAllPendingPR()
	
	toPageData = None
	usertype = ''
	
	if logDetails[0][1] == vcaf:
		toPageData = len(pendingInitPRs)
		usertype = 'vcaf'
	
	if logDetails[0][1] == chancellor:
		toPageData = len(pendingPRs)
		usertype = 'chancellor'
	
	
	pageData = []

	offices = off.getAllOfficesSorted()

	for offid in offices:

		offDetails = off.getOfficeDetails(offid[0])
		pageData = pageData + [offDetails]

	return setReponse(request, 'approving_office/index_v2.html', [(toPageData,usertype),], pageData, [], [])

def getPendingPR(request):


	pendingInitPRDetails = {}

	if request.method == 'POST':

		pendingInitPRs = preq.getAllPendingPR()
		
		for x in pendingInitPRs:
			prDetails = preq.getPRDetails(x[0])
			empDetails = e.getEmployeeDetails(prDetails[0][4])
			deptDetails = off.getOfficeDetails(empDetails[0][4])
			prItemList = preq.getItemByPR(x[0])
			totalCost = preq.getTotalCostofPR(prItemList)

			pendingInitPRDetails[x[0]] = {  
											'empName': empDetails[0][6]+" "+empDetails[0][1]+" "+empDetails[0][7]+" "+empDetails[0][2]+", "+empDetails[0][8],				
											'office': deptDetails[1],
											'date': str(prDetails[0][5]),
											'cost': totalCost,
											'purpose': prDetails[0][2],
											'reqnum' : prDetails[0][0],


			}

		pendingInitPRDetails['numOfPending'] = len(pendingInitPRs)
		

	return HttpResponse(json.dumps(pendingInitPRDetails), content_type="application/json")



def getPendingInitPR(request):


	pendingInitPRDetails = {}

	if request.method == 'POST':

		pendingInitPRs = preq.getAllInitPendingPR()
		
		for x in pendingInitPRs:
			prDetails = preq.getPRDetails(x[0])
			empDetails = e.getEmployeeDetails(prDetails[0][4])
			deptDetails = off.getOfficeDetails(empDetails[0][4])
			prItemList = preq.getItemByPR(x[0])
			totalCost = preq.getTotalCostofPR(prItemList)

			pendingInitPRDetails[x[0]] = {  'empName': empDetails[0][6]+" "+empDetails[0][1]+" "+empDetails[0][7]+" "+empDetails[0][2]+", "+empDetails[0][8],
											'office': deptDetails[1],
											'date': str(prDetails[0][5]),
											'cost': totalCost,
											'purpose': prDetails[0][2],
											'reqnum' : prDetails[0][0],


			}

		pendingInitPRDetails['numOfPending'] = len(pendingInitPRs)




	return HttpResponse(json.dumps(pendingInitPRDetails), content_type="application/json")

def profile(request):	

	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)

	unameData = u.getUnameFromID(logDetails[0][1])
	
	userdata = u.getUserDetails(unameData[0][0])

	return setReponse(request, 'approving_office/profile.html', userdata, [], [], [])

def create_pr(request):
	
	return setReponse(request, 'approving_office/create_pr.html',[], [], [], [])


'''
def pr_Details(request, refData):
	
	prRef = refData.replace('_','-')
	prNumArr = preq.getReqNumFromPR(prRef)
	prNum = prNumArr[0][0]

	prDetails = preq.getPRDetails(prNum)
	prItems = preq.getItemByPR(prNum)
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
	prStat = f.getPRStatus(prNum)
	

	return setReponse(request, 'approving_office/pr_details.html', prDetails, prItemstoPage,[(totalCostOfPR,'', loopRef),],prStat)
'''


def pr_Details(request, refData):
	
	print("sdsdsd")
	prRef = refData.replace('_','-')

	setSessionData(request, 'prCookie', prRef)

	prDetails = preq.getPRDetails(prRef)
	prLocDetails = preq.getPRLocDetails(prRef)
	empDetails = e.getEmployeeDetails(prDetails[0][4])
	offDetails = off.getOfficeDetails(empDetails[0][4])

	prItems = preq.getItemByPR(prRef)
	prItemstoPage = []
	for x in prItems:
			
		descripString = str(x[2])
	
		if "$" in descripString :

			arr = descripString.split('$')
			print(arr)

			prItemstoPage = prItemstoPage + [(x[0],x[1],arr[0],x[3],x[4],x[5],x[6]),]


			for y in range(1,len(arr)):
				prItemstoPage = prItemstoPage + [('','',' • '+arr[y],'','','',''),]

		else:
			prItemstoPage = prItemstoPage + [x]	


	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)
	totalCostOfPR = preq.getTotalCostofPR(prItems)
	userDetails = e.getEmployeeDetails(logDetails[0][1])
	
	toPageUserRef = ''

	if userDetails[0][4] == 'VCAF':
		toPageUserRef = 'vcaf'
	
	else:
		toPageUserRef = 'chancellor'

	return setReponse(request, theLocHead+'/pr_details1.html', [prDetails[0], prLocDetails[0], empDetails[0], offDetails, (toPageUserRef, totalCostOfPR)], prItemstoPage, [(prItems,),],[])

def accounts(request):
	
	pageData = []

	colleges = off.getColleges()
	academics = off.getAcademics()
	administratives = off.getAdministratives()

	offices = colleges + academics + administratives

	for offid in offices:

		offDetails = off.getOfficeDetails(offid[0])
		pageData = pageData + [offDetails]

	return setReponse(request, 'approving_office/accounts.html',pageData, [], [], [])

def itemList(request):
	
	if 'theOffID' in request.session:
		offID = request.session['theOffID']	

	return setReponse(request, 'approving_office/item_list.html',[(offID,),], [], [], [])	

def pendingPRList(request):
	
	if 'theOffID' in request.session:
		offID = request.session['theOffID']

	return setReponse(request, 'approving_office/pending_pr_list.html',[(offID,),], [], [], [])	

def prList(request):
	
	if 'theOffID' in request.session:
		offID = request.session['theOffID']	

	return setReponse(request, 'approving_office/all_pr_list.html',[(offID,),], [], [], [])
		
def departments(request):
	
	#offID = ''
	completeDeptList = []
	if 'theDeptID' in request.session:
		offID = request.session['theDeptID']

	offDetails = off.getOfficeDetails(offID)
	deptList = off.getDepartmentByCollege(offID)

	for deptid in deptList:
			deptDetails = off.getOfficeDetails(deptid[0])
			completeDeptList = completeDeptList + [deptDetails]

	return setReponse(request, 'approving_office/departments.html', [offDetails], completeDeptList, [], [])
'''
def allPR(request):
	
	pageData = []
	
	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)

	chancellor = kp.getChancellor()
	vcaf = kp.getVCAF()

	if logDetails[0][1] == vcaf:
		pendingInitPRs = preq.getAllInitPendingPR()
		allPR_1 = preq.getAllNonInitPendingPR()

		for x in pendingInitPRs:
			
			prDetails_1 = preq.getPRDetails(x[0])
			prRef1 = ''
			
			if prDetails_1[0][1] != None:
				prRef1 = prDetails_1[0][1]

			empDataDetails = e.getEmployeeDetails(prDetails_1[0][4])
			offDetails = off.getOfficeDetails(empDataDetails[0][4])
			prItems_1 = preq.getItemByPR(x[0])
			totalCost_1 = preq.getTotalCostofPR(prItems_1)
			pageData = pageData + [prDetails_1[0]+(totalCost_1, prRef1.replace('-','_'), offDetails[1])]
		
		for y in allPR_1:
			
			prDetails_2 = preq.getPRDetails(y[0])
			prRef2 = ''
			
			if prDetails_2[0][1] != None:
				prRef2 = prDetails_2[0][1]

			empDataDetails = e.getEmployeeDetails(prDetails_2[0][4])
			offDetails = off.getOfficeDetails(empDataDetails[0][4])
			prItems_2 = preq.getItemByPR(y[0])
			totalCost_2 = preq.getTotalCostofPR(prItems_2)
			pageData = pageData + [prDetails_2[0]+(totalCost_2, prRef2.replace('-','_'), offDetails[1])]
	
	if logDetails[0][1] == chancellor:
		pendingPRs = preq.getAllPendingPR()
		allPR_2 = preq.getAllNonPendingPR()

		for a in pendingPRs:
			
			prDetails_3 = preq.getPRDetails(a[0])
			prRef3 = ''

			if prDetails_3[0][1] != None:
				prRef3 = prDetails_3[0][1]

			empDataDetails = e.getEmployeeDetails(prDetails_3[0][4])
			offDetails = off.getOfficeDetails(empDataDetails[0][4])
			prItems_3 = preq.getItemByPR(a[0])
			totalCost_3 = preq.getTotalCostofPR(prItems_3)
			pageData = pageData + [prDetails_3[0]+(totalCost_3, prRef3.replace('-','_'), offDetails[1])]
		
		for b in allPR_2:
			
			prDetails_4 = preq.getPRDetails(b[0])
			prRef4 = ''

			if prDetails_4[0][1] != None:
				prRef4 = prDetails_4[0][1]

			empDataDetails = e.getEmployeeDetails(prDetails_4[0][4])
			offDetails = off.getOfficeDetails(empDataDetails[0][4])
			prItems_4 = preq.getItemByPR(b[0])
			totalCost_4 = preq.getTotalCostofPR(prItems_4)
			pageData = pageData + [prDetails_4[0]+(totalCost_4, prRef4.replace('-','_'), offDetails[1])]	
	


	return setReponse(request, 'approving_office/pending_pr.html',pageData, [], [], [])	

'''

def allPR_Original(request):
	
	pageData = []
	
	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)

	chancellor = kp.getChancellor()
	vcaf = kp.getVCAF()

	if logDetails[0][1] == vcaf:
		pendingInitPRs = preq.getAllInitPendingPR()
		allPR_1 = preq.getAllNonInitPendingPR()

		for x in pendingInitPRs:
			
			prDetails_1 = preq.getPRDetails(x[0])
			prRef1 = prDetails_1[0][0]

			empDataDetails = e.getEmployeeDetails(prDetails_1[0][4])
			offDetails = off.getOfficeDetails(empDataDetails[0][4])
			prItems_1 = preq.getItemByPR(x[0])
			totalCost_1 = preq.getTotalCostofPR(prItems_1)
			pageData = pageData + [prDetails_1[0]+(totalCost_1, prRef1.replace('-','_'), offDetails[1])]
		
		for y in allPR_1:
			
			prDetails_2 = preq.getPRDetails(y[0])
			prRef2 = prDetails_2[0][0]

			empDataDetails = e.getEmployeeDetails(prDetails_2[0][4])
			offDetails = off.getOfficeDetails(empDataDetails[0][4])
			prItems_2 = preq.getItemByPR(y[0])
			totalCost_2 = preq.getTotalCostofPR(prItems_2)
			pageData = pageData + [prDetails_2[0]+(totalCost_2, prRef2.replace('-','_'), offDetails[1])]
	
	if logDetails[0][1] == chancellor:
		pendingPRs = preq.getAllPendingPR()
		allPR_2 = preq.getAllNonPendingPR()

		for a in pendingPRs:
			
			prDetails_3 = preq.getPRDetails(a[0])
			prRef3 = prDetails_3[0][0]

			empDataDetails = e.getEmployeeDetails(prDetails_3[0][4])
			offDetails = off.getOfficeDetails(empDataDetails[0][4])
			prItems_3 = preq.getItemByPR(a[0])
			totalCost_3 = preq.getTotalCostofPR(prItems_3)
			pageData = pageData + [prDetails_3[0]+(totalCost_3, prRef3.replace('-','_'), offDetails[1])]
		
		for b in allPR_2:
			
			prDetails_4 = preq.getPRDetails(b[0])
			prRef4 = prDetails_4[0][0]

			empDataDetails = e.getEmployeeDetails(prDetails_4[0][4])
			offDetails = off.getOfficeDetails(empDataDetails[0][4])
			prItems_4 = preq.getItemByPR(b[0])
			totalCost_4 = preq.getTotalCostofPR(prItems_4)
			pageData = pageData + [prDetails_4[0]+(totalCost_4, prRef4.replace('-','_'), offDetails[1])]	
	


	return setReponse(request, 'approving_office/pending_pr.html',pageData, [], [], [])	

def departmentPR(request):
	
	completeDeptList = []
	if 'theDeptID' in request.session:
		offID = request.session['theDeptID']

	offDetails = off.getOfficeDetails(offID)
	deptList = off.getDepartmentByCollege(offID)

	for deptid in deptList:
			deptDetails = off.getOfficeDetails(deptid[0])
			completeDeptList = completeDeptList + [deptDetails]

	return setReponse(request, 'approving_office/departments_pr.html', [offDetails], completeDeptList, [], [])

def departmentPendingPR(request):
	
	completeDeptList = []
	if 'theDeptID' in request.session:
		offID = request.session['theDeptID']

	offDetails = off.getOfficeDetails(offID)
	deptList = off.getDepartmentByCollege(offID)

	for deptid in deptList:
			deptDetails = off.getOfficeDetails(deptid[0])
			completeDeptList = completeDeptList + [deptDetails]

	return setReponse(request, 'approving_office/departments_pending.html', [offDetails], completeDeptList, [], [])

def pendingPR(request):

	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)	

	pageData = []

	chanId = kp.getChancellor()
	vcafId = kp.getVCAF()

	if chanId == logDetails[0][1]:
		pendings = preq.getAllPendingPR()
		
		for x in pendings:
			reqDetails = preq.getPRDetails(x[0])
			pageData = pageData +reqDetails
	
	if vcafId == logDetails[0][1]:
		
		pendings = preq.getAllInitPendingPR()

		for x in pendings:
			reqDetails = preq.getPRDetails(x[0])
			pageData = pageData +reqDetails
	

		
	return setReponse(request, 'approving_office/pending_pr.html',pageData, [], [], [])	


def allPR(request):
	
	toPageData = []
	

	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)
	
	userDetails = e.getEmployeeDetails(logDetails[0][1])
	
	allPRnum = []
	toPageUserRef = ''

	if userDetails[0][4] == 'VCAF':
		allPRnum = f.getAllPRList()
		toPageUserRef = 'vcaf'
	
	else:
		allPRnum = f.getAllPRListByStatus('pending', 'final') + f.getAllPRListByStatus('approved', 'final') + f.getAllPRListByStatus('declined', 'all')
		toPageUserRef = 'chancellor'	

	for x in allPRnum:
		prDetails = f. getPRCompleteDetails(x[0][0], '')
		toPageData = toPageData + [(prDetails)]

	return setReponse(request, theLocHead+'/all_pr.html', toPageData, [(toPageUserRef,),], [], [])	



def decidePR(request):
	
	thePRCookieValue = getSessionData(request, 'prCookie')
	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)

	notifNum = n.getNotifFromDataWithRef(thePRCookieValue, logDetails[0][1],'pr')

	vcaf = kp.getVCAF()
	chancellor = kp.getChancellor()

	ref = {chancellor:'chancellor', vcaf:'vcaf'}
	decision = ''

	if request.method == 'POST':
		decision = request.POST['decision']
		isEdit = request.POST['isEdit']
		theMatrix = json.loads(request.POST.get('theMatrix'))

		print("+++==============+++++===========")
		print(isEdit)
		print(theMatrix)

	print(ref[logDetails[0][1]])
	if ref[logDetails[0][1]] == 'vcaf':
		
		if decision == 'approve':
			f.initApprovePR(thePRCookieValue, isEdit, theMatrix)


	if ref[logDetails[0][1]] == 'chancellor':
		
		if decision == 'approve':
			f.approvePR(thePRCookieValue, isEdit, theMatrix)



	n.updateNotif(notifNum[0][0])
	return HttpResponse('')	


def pendingPRDetails(request):
	
	theCookieValue = ''
	prDetails = []
	prItems = []
	response = None

	if idSessionValueEmpty(request,'prCookie'):
		theCookieValue = request.POST.get('reqNum','')
		
	
	else:
		theCookieValue = getSessionData(request, 'prCookie')
		#theCookieValue = refData.replace('_','-')

		setSessionData(request, 'prCookie', theCookieValue)

		prDetails = preq.getPRDetails(theCookieValue)
		prLocDetails = preq.getPRLocDetails(theCookieValue)
		empDetails = e.getEmployeeDetails(prDetails[0][4])
		offDetails = off.getOfficeDetails(empDetails[0][4])

		prItems = preq.getItemByPR(theCookieValue)
		prItemstoPage = []
		for x in prItems:
				
			descripString = str(x[2])
		
			if "$" in descripString :

				arr = descripString.split('$')
				print(arr)

				prItemstoPage = prItemstoPage + [(x[0],x[1],arr[0],x[3],x[4],x[5],x[6]),]


				for y in range(1,len(arr)):
					prItemstoPage = prItemstoPage + [('','',' • '+arr[y],'','','',''),]

			else:
				prItemstoPage = prItemstoPage + [x]	


		theCookieValue = getSessionData(request, 'theCookie')
		logDetails = l.getLogDetails(theCookieValue)
		totalCostOfPR = preq.getTotalCostofPR(prItems)
		userDetails = e.getEmployeeDetails(logDetails[0][1])
		
		toPageUserRef = ''

		if userDetails[0][4] == 'VCAF':
			toPageUserRef = 'vcaf'
		
		else:
			toPageUserRef = 'chancellor'

		response = setReponse(request, theLocHead+'/pr_details1.html', [prDetails[0], prLocDetails[0], empDetails[0], offDetails, (toPageUserRef, totalCostOfPR)], prItemstoPage, [(prItems,),],[])

	return response

'''
def pendingPRDetails(request, refData):
	
	theCookieValue = ''
	prDetails = []
	prItems = []

	if idSessionValueEmpty(request,'prCookie'):
		theCookieValue = request.POST.get('reqNum','')
		
	
	else:
		theCookieValue = getSessionData(request, 'prCookie')
		prDetails = preq.getPRDetails(theCookieValue)
		reqPersonnelDetails = e.getEmployeeDetails(prDetails[0][4])
		prItems = preq.getItemByPR(theCookieValue)
		totalCostOfPR = preq.getTotalCostofPR(prItems)

	response = setReponse(request, 'approving_office/pending_pr_details.html', prDetails, prItems, reqPersonnelDetails, [(totalCostOfPR,),])
	
	return response	

'''

def displayPendingPRDetails(request):
	
	reqNum = request.POST.get('detailsButton','')
	response = HttpResponseRedirect('/approving_officer/pending_request/pr_details')
	setSessionData(request, 'prCookie', reqNum)
	return response

def displayPendingPRDetailsFromIndex(request):
	
	response = None
	
	if request.method == 'POST':

		reqNum = request.POST['reqNum']
		response = HttpResponseRedirect('/approving_officer/pending_request/pr_details')
		setSessionData(request, 'prCookie', reqNum)
		
	return response

def setPRCookie(request):
	
	
	if request.method == 'POST':

		reqNum = request.POST['reqNum']
		
		setSessionData(request, 'prCookie', reqNum)
		
	return HttpResponse('')



'''
def notifications(request):
	 
	 
	 notifNum = request.POST.get('d', '')
	 notifDetails = n.getNotifDetails(notifNum)

	 notifRefType = notifDetails[0][10]
	 notifRef = notifDetails[0][5]
	
	 response = None

	 if notifRefType == 'pr':
	 	response = HttpResponseRedirect('/approving_officer/pending_request/pr_details')

	 	setSessionData(request, 'prCookie', notifRef)
	 
	 return response
'''

def notifications(request, refData):
	 
	 notifNum = refData.replace('_', '-')
	 notifDetails = n.getNotifDetails(notifNum)
	 userDetails = u.getUserDetailsFromID(notifDetails[0][2])

	
	 response = None
	 notifRefType = notifDetails[0][9]
	 notifRef = notifDetails[0][5]

	 if notifRefType == 2:
	 	n.updateNotif(notifNum)

	 linkEqui = {
	 				1:'/approving_officer/',
	 				12:'/approving_officer_representative',
	 				2:'/procurement_office/' ,
	 				21:'/procurement_office/' ,
	 				3:'/inventory_office_admin/',
	 				32:'/inventory_office_acct_mgr/',
	 				33:'/inventory_office_rec_off/',
	 				34:'/inventory_office_rec_off/',
	 				4:'/requisitioner/',
	 				5:'/non_requisitioner/',
	 				6:'/accounting/',


	 }	

	 acctType = (userDetails[0][3])[0]

	 print("+++++++++++ffffff+++++++++++++++++++")
	 print(linkEqui[acctType])

	 response = HttpResponseRedirect( linkEqui[acctType] + notifDetails[0][11])
	 setSessionData(request, 'notifnum', notifNum)
	 
	 return response


def officeInvenDetails(request):
	
	reponse = None
	buttonData = request.POST.get('','')

def displayDeptItems(request):
	
	deptID = request.POST.get('','')
	setSessionData(request,'theDeptID', deptID)

def acctdetails(request):
	
	reponse = None
	offID = request.POST.get('offDetails', '')

	offDetails = off.getOfficeDetails(offID)
	if offDetails[2] == 'college':
		
		reponse = HttpResponseRedirect('/approving_officer/account/departments')
		setSessionData(request, 'theDeptID', offID)
	
	else:
		reponse = HttpResponseRedirect('/approving_officer/account/item_list')
		setSessionData(request, 'theOffID', offID)	

	return reponse

def pendingListDetails(request):
	
	reponse = None
	offID = request.POST.get('offDetails', '')

	offDetails = off.getOfficeDetails(offID)
	if offDetails[2] == 'college':
		
		reponse = HttpResponseRedirect('/approving_officer/pending_request/departments')
		setSessionData(request, 'theDeptID', offID)
	
	else:
		reponse = HttpResponseRedirect('/approving_officer/pending_request/list')
		setSessionData(request, 'theOffID', offID)	

	return reponse

def prListDetails(request):
	
	reponse = None
	offID = request.POST.get('offDetails', '')

	offDetails = off.getOfficeDetails(offID)
	if offDetails[2] == 'college':
		
		reponse = HttpResponseRedirect('/approving_officer/all_request/departments')
		setSessionData(request, 'theDeptID', offID)
	
	else:
		reponse = HttpResponseRedirect('/approving_officer/all_request/list')
		setSessionData(request, 'theOffID', offID)	

	return reponse

def declinePR(request):
	
	thePRCookieValue = getSessionData(request, 'prCookie')
	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)

	notifNum = n.getNotifFromDataWithRef(thePRCookieValue, logDetails[0][1], 'pr')

	vcaf = kp.getVCAF()
	chancellor = kp.getChancellor()

	ref = {chancellor:'chancellor', vcaf:'vcaf'}
	reason = ''

	if request.method == 'POST':
		reason = request.POST['reason']


	print(ref[logDetails[0][1]])
	if ref[logDetails[0][1]] == 'vcaf':
		
		f.initDeclinePR(thePRCookieValue, reason)


	if ref[logDetails[0][1]] == 'chancellor':
		
		f.declinePR(thePRCookieValue, reason)

	n.updateNotif(notifNum[0][0])
	
	return HttpResponse('')	

def getNotifNum(request):

	outputData = {}

	theCookieValue = getSessionData(request, 'theCookie')

	logDetails = l.getLogDetails(theCookieValue)
	notifNum = n.getNotifNum(logDetails[0][1])

	return HttpResponse(notifNum[0][0])

def getTaskNum(request):

	outputData = {}

	theCookieValue = getSessionData(request, 'theCookie')

	logDetails = l.getLogDetails(theCookieValue)
	taskNum = n.getTaskNum(logDetails[0][1])

	print(taskNum)

	return HttpResponse(taskNum[0][0])


def getNotifs(request):
	

	outputData = {}

	theCookieValue = getSessionData(request, 'theCookie')

	logDetails = l.getLogDetails(theCookieValue)

	notifs = setNotifDetails(logDetails[0][1])
	
	counter = 1
	
	for x in notifs:

			outputData[str(counter)] = {'notifID': x[0],
										'iconTag': x[1],
										'colorTag': x[2],
										'subT1': x[3],
										'subT2' : x[4],
										'title': x[5],
										'date': (x[6]).strftime('%m/%d/%Y'),
										'time': (x[7]).strftime('%H:%M'),
										'linkref':x[8],
			}

			counter = counter + 1


	return HttpResponse(json.dumps(outputData), content_type="application/json")


def getTasks(request):
	

	outputData = {}

	theCookieValue = getSessionData(request, 'theCookie')

	logDetails = l.getLogDetails(theCookieValue)

	tasks = setTaskDetails(logDetails[0][1])
	
	counter = 1
	
	for x in tasks:
			print("=======    =================")
			print(x)
			outputData[str(counter)] = {'notifID': x[0],
										'iconTag': x[1],
										'colorTag': x[2],
										'subT1': x[3],
										'subT2' : x[4],
										'title': x[5],
										'date': (x[6]).strftime('%m/%d/%Y'),
										'time': (x[7]).strftime('%H:%M'),
										'linkref':x[8],
			}

			counter = counter + 1

			#
        


	return HttpResponse(json.dumps(outputData), content_type="application/json")




#/////=================================================================================================================================

def setSessionData(request, key, value):
    request.session[key] = value
    SESSION_COOKIE_AGE = 60 * 60
    

def getSessionData(request, key):
    value = request.session[key]
    return value 

def idSessionValueEmpty(request, key):
    if key in request.session:
      return False
    else:
      return True 

def setCookie(reponse, key, value):
    
	reponse.set_cookie(key, value, max_age = 3600)

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

def setReponse(request, outputPage, pageData1, pageData2, pageData3, pageData4):
	
	if idSessionValueEmpty(request,'theCookie'):
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
        	'dept': deptDetails[0][1],
        	'empData':employeeData,

        	'taskNum': taskNum,
        	'notifNum': notifNum,
        	'pageData1': pageData1,
        	'pageData2': pageData2,
        	'pageData3': pageData3,
        	'pageData4': pageData4,
			'baseSource': 'approving_office/base.html',
            'urlHead': urlHead,
        
		}


		if any( 1 == code for code in acctType):

			response = render(request, outputPage, c)
			setSessionData(request, 'theCookie', cookieValue)

		else:
			response = HttpResponse('Not Allowed to Access this Page')

	return response	

def renderPDF(request, template, pageData1, pageData2, pageData3, pageData4, pdfName, loopRefNum):

		c = {
        	
        	'pageData1': pageData1,
        	'pageData2': pageData2,
        	'pageData3': pageData3,
        	'pageData4': pageData4,
        	'loopRef' : loopRefNum,
		
		}

		html_string = render_to_string(template,c)
		
		html = HTML(string=html_string).write_pdf('{}/Project_SMO_Inventory/static/src/mypdf.pdf'.format(dirreq), stylesheets=[CSS(string='@page {size: Legal; margin:35px;}')]);
		
		fs = FileSystemStorage('{}/Project_SMO_Inventory/static/src/'.format(dirreq))

		with fs.open('mypdf.pdf') as pdf:

			response = HttpResponse(pdf, content_type='application/pdf')
			
			response['Content-Disposition'] = 'attachment; filename="'+pdfName+'.pdf"'
			
			return response	

		return response	


def setNotifDetails(idnum):
    
		outputList = []

		notifList = n.getNotifOfPersonnel(idnum)

		print('//=============')

		for x in notifList:
	      
			kk = n.getNotifDisplayDetails(x[0])
			print(kk)

			notifTimeDate = n.getHotifTimeAndDate(x[0])
			linkref = n.getNotifLinkRef(x[0])
			print('//========    =====')
			print(linkref)
	      
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
	      
			ll = ll + (kk[0][2],kk[0][3],kk[0][4],notifTimeDate[0][0], notifTimeDate[0][1],linkref[0]) 
	      
			outputList = outputList + [ll]


		return outputList

def setTaskDetails(idnum):
	    
		outputList = []

		taskList = n.getTaskOfPersonel(idnum)
		print('//=============')

		for x in taskList:
	     
			kk = n.getNotifDisplayDetails(x[0])
			print(kk)
	        
			notifTimeDate = n.getHotifTimeAndDate(x[0])
			linkref = n.getNotifLinkRef(x[0])
			print('//========    =====')
			print(linkref)


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
	      
			ll = ll + (kk[0][2],kk[0][3],kk[0][4],notifTimeDate[0][0], notifTimeDate[0][1],linkref[0]) 
	      
			outputList = outputList + [ll]

		return outputList

