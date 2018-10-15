from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.conf import settings

import tempfile
from num2words import num2words

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
from datetime import datetime

from PyPDF2 import PdfFileWriter, PdfFileReader


dirreq = dirname(dirname(abspath(__file__)))
sys.path.append('{}/Project_SMO_Inventory/static/src'.format(dirreq))

from functions import Functions
from user import User
from log import Log
from employees import Employees
from notifications import Notification
from purchase_request import PurchaseRequest
from inspect_accept_report import InsepectionAndAcceptanceReceipt
from office import Offices
from key_positions import KeyPositions
from suppliers import Suppliers
from request_for_quotation import RequestForQuotation
from purchase_order import PurchaseOrder
from abstract_of_canvass import AbstractOfCanvass

f = Functions()
u = User()
l = Log()
e = Employees()
n = Notification()
ins = InsepectionAndAcceptanceReceipt()
pOrd = PurchaseOrder()
preq = PurchaseRequest()
reqQ = RequestForQuotation()
pord = PurchaseOrder()
off = Offices()
kp = KeyPositions()
sup = Suppliers()
abc = AbstractOfCanvass()



def index(request):
	return setReponse(request, 'procurement/index.html',[],[],[],[],[])

def profile(request):

	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)

	unameData = u.getUnameFromID(logDetails[0][1])
	
	userdata = u.getUserDetails(unameData[0][0])

	return setReponse(request, 'procurement/profile.html', userdata,[],[],[],[])

def addBid(request):
	return setReponse(request, 'procurement/add-bidding.html', [],[],[],[],[])

def bid(request):
	return setReponse(request, 'procurement/biddings.html', [],[],[],[],[])

def addQuotation(request):
	reqNum = reqQ.generateReqNum()
	thePRNumRef = ''
	
	if isSessionValueEmpty(request, 'toRQCookie') == False:
		thePRNumRef = getSessionData(request, 'toRQCookie')
		del request.session['toRQCookie']

	return setReponse(request, 'procurement/add-quotation-new.html',[],[(reqNum,),],[(thePRNumRef,),],[],[])

def addQuotationNew(request):
	reqNum = reqQ.generateReqNum()
	thePRNumRef = ''
	
	if isSessionValueEmpty(request, 'toRQCookie') == False:
		thePRNumRef = getSessionData(request, 'toRQCookie')
		del request.session['toRQCookie']

	return setReponse(request, 'procurement/add-quotation-new.html',[],[(reqNum,),],[(thePRNumRef,),],[],[])


def quotation(request):

	toPageData = []
	quoList = reqQ.getAllReqQuo()

	for x in quoList:
		compNums = len(reqQ.getReqComp(x[0]))
		refString = x[0]
		toPageData = toPageData + [x+(compNums, refString.replace('-','_'))]
	
	return setReponse(request, 'procurement/quotations.html',toPageData,[],[],[],[])

def addAbstract(request):
	return setReponse(request, 'procurement/add-abstract-new.html',[],[],[],[],[])

def addAbstractNew(request):
	return setReponse(request, 'procurement/add-abstract-new.html',[],[],[],[],[])


def abstract(request):

	toPageData = []
	abstractList = abc.getAllAbstract()

	for x in abstractList:
		rqDetails = reqQ.getRequestDetails(x[0])
		refString = x[0]

		toPageData = toPageData + [x + (rqDetails[0][0], rqDetails[0][1], refString.replace('-','_'))]

	return setReponse(request, 'procurement/abstract.html', toPageData,[],[],[],[])	

def createPO(request):

	poNum = f.generatePONum()
	return setReponse(request, 'procurement/create-po.html', [(poNum,),],[],[],[],[])

def newPOFromABS(request):

	
	absNum = request.POST.get('absnum','')
	rqDetails = reqQ.getRequestDetails(absNum)

	suppSudData = {'test':'Data Test'}

	prnum = rqDetails[0][1]
	
	suppIDs = []
	items = []

	supps = abc.getWinningSuppliers(absNum)
	
	poCounterx = pord.getMaxCounter()

	for x in supps:
		
		poCounterx = poCounterx + 1
		
		rqSuppDetails = reqQ.getComTerms(absNum, x[0])

		suppDetails = sup.getSupllierDetails(x[0])
		##toSuppIDsData = 

		suppIDs = suppIDs + [suppDetails[0] + rqSuppDetails[0]]

		genPO = generatePONum(poCounterx)

		suppSudData[str(x[0])+'_ponum'] = genPO
		poCounterx = poCounterx + 1

	
	poCounter = pord.getMaxCounter()
	suppCount = len(suppIDs)
	genPONum = ()

	for xx in range(0,suppCount):
		
		curentCount = poCounter + 1
		genPO = generatePONum(curentCount)
		
		genPONum = genPONum + (genPO,)
		curentCount = curentCount + 1

	
	for y in supps:
		
		suppWinnigItems = abc.getSupplierWinningItems(absNum, y[0])
		
		itemAllTotal = 0
		for cc in suppWinnigItems:
			
			itemDescrip = abc.getDescriptionFromItemNum(absNum, cc[2])
			itemAddDetails = abc.getItemTotalCost(absNum, cc[2], y[0])
			

			itemAllTotal = itemAllTotal + itemAddDetails[3]
			toItemsData = cc + itemAddDetails + (itemDescrip,) 	
		
			items = items + [toItemsData,]


	return setReponse(request, 'procurement/create-po-from-abs.html', [(prnum, absNum, suppCount, poCounter),genPONum], suppIDs, items,[(suppSudData),],[])	

def po(request):

	toPageData = []	

	poList = pord.getAllPO()

	for x in poList:
		
		suppDetails = sup.getSupllierDetails(x[1])
		refString = x[0]
		
		toPageData = toPageData + [x + suppDetails[0] + (refString.replace('-','_'),),]
		print(len(x + suppDetails[0] + (refString.replace('-','_'),)))

	print(toPageData)
	return setReponse(request, 'procurement/po.html', toPageData,[],[],[],[])	

def poCompleteDetails(request):
	return setReponse(request, 'procurement/po_details_new.html', [],[],[],[],[])	

def rqCompleteDetails(request):
	return setReponse(request, 'procurement/rq_details.html', [],[],[],[],[])	

def abcCompleteDetails(request):
	return setReponse(request, 'procurement/abc_details.html', [],[],[],[],[])	



def pendingPO(request):
	
	theCookieValue = ''

	if isSessionValueEmpty(request,'poCookie'):
		theCookieValue = request.POST.get('approveButton','')
	
	else:
		theCookieValue = getSessionData(request, 'poCookie')

	print("the PO num "+theCookieValue)
	
	poDetails = pord.getPODetails(theCookieValue)
	print(poDetails[0][1])
	suppDetails = sup.getSupllierDetails(poDetails[0][1])
	print(suppDetails)
	poItems = pord.getItemByPO(theCookieValue)

	return setReponse(request, 'procurement/pending_po_details.html', poDetails,poItems,[(suppDetails[0][1],),],[],[])

def addContract(request):
	return setReponse(request, 'procurement/add-contract.html',[],[],[],[],[])

def contract(request):
	return setReponse(request, 'procurement/contracts.html', [],[],[],[],[])		

def suppliers(request):
	return setReponse(request, 'procurement/suppliers.html', [],[],[],[],[])		

def suppCompleteDetails(request):
	return setReponse(request, 'procurement/supp_details.html', [],[],[],[],[])		


def prList(request):
	
	offID = ''
	if 'theOffID' in request.session:
		offID = request.session['theOffID']

	offDetails = off.getOfficeDetails(offID)	
	return setReponse(request, 'procurement/all_pr_list.html',[offDetails], [], [], [], [])


def allPR(request):
	
	toPageData = []

	allPRnum = preq.getAllApprovedPR()

	for x in allPRnum:
		prDetails = preq.getPRDetails(x[0])
		empDetails = e.getEmployeeDetails(prDetails[0][4])
		offDetails = off.getOfficeDetails(empDetails[0][4])

		toPageData = toPageData + [(prDetails[0]+empDetails[0]+(offDetails[1],)),]

	return setReponse(request, 'procurement/all_pr.html', toPageData, [], [], [], [])	


def departmentPR(request):
	
	completeDeptList = []
	if 'theDeptID' in request.session:
		offID = request.session['theDeptID']

	offDetails = off.getOfficeDetails(offID)
	deptList = off.getDepartmentByCollege(offID)

	for deptid in deptList:
			deptDetails = off.getOfficeDetails(deptid[0])
			completeDeptList = completeDeptList + [deptDetails]

	return setReponse(request, 'procurement/departments_pr.html', [offDetails], completeDeptList, [], [], [])

def pr(request):
	return setReponse(request, 'procurement/pr.html',[],[],[],[],[])		

def numPR(request):
	return setReponse(request, 'procurement/num_pr.html',[],[],[],[],[])		

def prDetails(request, refData):

	return setReponse(request, 'procurement/pr_details.html', [], [], [], [],[])
	
def prForNumDetails(request):
	
	theCookieValue = ''
	prDetails = []
	prItems = []

	if isSessionValueEmpty(request,'prCookie'):
		theCookieValue = request.POST.get('reqNum','')
		
	
	else:
		theCookieValue = getSessionData(request, 'prCookie')
		prDetails = preq.getPRDetails(theCookieValue)
		reqPersonnelDetails = e.getEmployeeDetails(prDetails[0][4])
		prItems = preq.getItemByPR(theCookieValue)
		totalCostOfPR = preq.getTotalCostofPR(prItems)

	response = setReponse(request, 'procurement/pending_pr_details.html', prDetails, prItems, reqPersonnelDetails, [(totalCostOfPR,),],[])
	
	return response

def displayPODetails(request, refData):

    refPO = refData.replace('_', '-')

    poDetails = pord.getPODetails(refPO)
    prDetails = preq.getPRDetails(preq.getReqNumFromPR(poDetails[0][13])[0][0])
    poItems = pord.getItemByPO(refPO)
    poTotal = pord.getTotalCostofPO(poItems)
    empDetails = e.getEmployeeDetails(prDetails[0][4])
    offDetails = off.getOfficeDetails(empDetails[0][4])
    suppDetails = sup.getSupllierDetails(poDetails[0][1])
    iarNum = ins.getIARNumFromRef(refPO)
    iarDetails = None
    
    quoNum = reqQ.getReqNumFromRefNum(poDetails[0][13])
    
    quoNumRef = ''
    if quoNum != None:
        quoNumRef =  quoNum.replace('-','_')

    theString = poDetails[0][6]


    if iarNum != None:
        iarDetails = ins.getIARDetails(iarNum)[0]+(iarNum.replace('-','_'),)

       
    return setReponse(request, 'procurement/po_details_new.html', [poDetails[0]+(poTotal,),prDetails[0]+(str(poDetails[0][13]).replace('-','_'),), empDetails[0], (offDetails[1],), suppDetails[0], iarDetails, (quoNum, quoNumRef)], poItems, [], [], [])

def rqCompleteDetailsFromRef(request, refData):

	rqNum = refData.replace('_','-')

	quoDetails = reqQ.getRequestDetails(rqNum)
	prRefDetails = None
	suppliers = None
	prItems = None
	reqQItems = None
	absDetails = None


	return setReponse(request, 'procurement/rq_details.html', [],[],[],[],[])	

def abcCompleteDetailsFromRef(request, refData):

	abcNum = refData.replace('_','-')
	
	abcDetails = abc.getAbstractDetails(abcNum)
	reqQDeatils = reqQ.getRequestDetails(abcNum)
	prDetails = preq.getPRDetails(preq.getReqNumFromPR(reqQDeatils[0][1])[0][0])
	empDetails = e.getEmployeeDetails(prDetails[0][4])
	offDetails = off.getOfficeDetails(empDetails[0][4])
	
	suppliers = []
	abcItems = []

	abcSupp = reqQ.getReqComp(abcNum)
	abcSuppBids = []
	absItems = abc.getAbstractItems(abcNum)
	
	for x in abcSupp:
		suppDetails = sup.getSupllierDetails(x[1])
		suppliers = suppliers + [suppDetails[0] + (x[2], x[3])]

	for x in absItems:
		pass
	
	return setReponse(request, 'procurement/abc_details.html', [abcDetails[0], reqQDeatils[0], prDetails[0],empDetails[0], offDetails],[],[],[],[])	


def displayNotif(request):
	
	notifNum = request.POST.get('d', '')
	notifDetails = n.getNotifDetails(notifNum)

	notifRefType = notifDetails[0][10]
	notifRef = notifDetails[0][5]
	
	response = None

	if notifRefType == 'pr':
		response = HttpResponseRedirect('/procurement_office/number_a_pr/pr_details')
		setSessionData(request, 'prCookie', notifRef)

	if notifRefType == 'po':
		response = HttpResponseRedirect('/procurement_office/po/pendingPO')
		setSessionData(request, 'poCookie', notifRef)

	return response


def notifications(request, refData):
	 
	notifNum = refData.replace('_', '-')
	notifDetails = n.getNotifDetails(notifNum)

	notifRefType = notifDetails[0][10]
	notifRef = notifDetails[0][5]


	print("notifType: "+str(notifRefType)+", Notifef"+str(notifRef))
	
	response = None

	if notifRefType == 'pr':
		response = HttpResponseRedirect('/procurement_office/number_a_pr/pr_details')
		setSessionData(request, 'prCookie', notifRef)

	if notifRefType == 'po':
		response = HttpResponseRedirect('/procurement_office/po/pendingPO')
		setSessionData(request, 'poCookie', notifRef)

	if notifRefType == 'abstract':
		response = HttpResponseRedirect('/procurement_office/abstract/'+notifRef.replace('-','_')+'/details')
		#setSessionData(request, 'acCookie', notifRef)
	
	if notifRefType == 'po':
		response = HttpResponseRedirect('/procurement_office/po/pendingPO')
		setSessionData(request, 'poCookie', notifRef)
		
	return response

def numtheReq(request):
	
	prnum =  request.POST.get('approveButton', '')
	
	setSessionData(request, 'toRQCookie', prnum)

	return HttpResponseRedirect('/procurement_office/add_quotation/')

def prListDetails(request):
	
	reponse = None
	offID = request.POST.get('offDetails', '')

	offDetails = off.getOfficeDetails(offID)
	if offDetails[2] == 'college':
		
		reponse = HttpResponseRedirect('/procurement_office/pr/departments/')
		setSessionData(request, 'theDeptID', offID)
	
	else:
		reponse = HttpResponseRedirect('/procurement_office/pr/list/')
		setSessionData(request, 'theOffID', offID)	

	return reponse

def addReqQuotation(request):
	
	response = None
	
	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)
	
	quotNum = ''
	projName = ''
	projLoc = ''
	prNum = ''
	canv = ''
	quotNumCode = ''
	
	reqnum = l.generateLogID()
	supplier = {}
	itemsMatrix = {}

	if request.method == 'POST':
		
		supplier = json.loads(request.POST.get('theMatrix'))
		itemsMatrix = json.loads(request.POST.get('theItemMatrix'))
		prNum = request.POST['prnum']
		projName = request.POST['projName']
		projLoc = request.POST['projLoc']
		canv = request.POST['canv']
		quotNumCode = request.POST['quotNumCode']
	
	print(quotNumCode)

	f.addReqQuo(prNum, projName, projLoc, canv, supplier, itemsMatrix)
	
	#response = generateRQDocument(request, quotNumCode)	
	
	reqNum = preq.getReqNumFromPR(prNum)
	
	notifNum = n.getNotifFromDataWithRef(reqNum[0][0], logDetails[0][1], 'pr')
	notifDetails = n.getNotifDetails(notifNum[0][0])


	if notifDetails[0][3] == False:
		n.updateNotif(notifNum[0][0])

	
	return HttpResponse('')


def addAbstractOfCanvass(request):
	
	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)
	
	quotNum = ''
	openingDate = ''
	openingTime = ''
	
	reqnum = l.generateLogID()
	theArray = {}

	if request.method == 'POST':
		
		theArray = json.loads(request.POST.get('theDjangoArray'))
		quotNum = request.POST['quotNum']
		openingDate = request.POST['openingDate']
		openingTime = request.POST['openingTime']
	
	
	f.addAbsCanv(quotNum, openingDate, openingTime, theArray)

	return HttpResponse('')	

def getSupplierDetails(request):

	compName = None
	compDetails = []

	if request.method == 'POST':
		
		compName = request.POST['compName']
		print(compName)
		compID = sup.getCompIDfromName(compName)
		compDetails = sup.getSupllierDetails(compID)
	
	outputData = {
		
		'name': compDetails[0][1],
		'address': compDetails[0][2],
		'rep': compDetails[0][3],
		'repnum': compDetails[0][4],
		'repemail':	compDetails[0][5],
	}

	return HttpResponse(json.dumps(outputData), content_type="application/json")

def findComp(request):
	
	compName = None
	outputData = {}
	
	if request.method == 'POST':
		compName = request.POST['compName']
		print(compName)
		compList = sup.findCompName(compName)
	
	refIndex = 1
	for x in compList:
		outputData[str(refIndex)] = x[0]
		refIndex = refIndex + 1
	print(outputData)
	return HttpResponse(json.dumps(outputData), content_type="application/json")

def findRepComp(request):
	
	repName = None
	outputData = {}
	
	if request.method == 'POST':
		repName = request.POST['repName']
		repList = sup.findCompRepName(repName)
	
	refIndex = 1
	
	for x in repList:
		outputData[str(refIndex)] = {'name':x[0],
									 'compid':x[1],
									 'compname':x[2],
		}
		refIndex = refIndex + 1

	return HttpResponse(json.dumps(outputData), content_type="application/json")


def getPRItems(request):
	
	items = []
	outputData = {}

	if request.method == 'POST':
		prNum = request.POST['prNum']
		
		print("PrNum in " + prNum)
		
		reqNum = preq.getReqNumFromPR(prNum)
		items = preq.getItemByPR(reqNum[0][0])
		counter = 1
		
		for x in items:
			outputData[str(counter)] = {'stocknum':x[1], 
										'description':x[2],
										'unit':x[3], 
										'unitprice':x[4], 
										'quantity':x[5],
										}
			counter = counter + 1							
	
	return HttpResponse(json.dumps(outputData), content_type="application/json")		

def getReqComp(request):
	
	outputData = {}
	response = None

	if request.method == 'POST':
		quotNum = request.POST['quotNum']
		
		compList = reqQ.getReqComp(quotNum)
		
		if compList == []:
			response = HttpResponse('nonExisting')
		
		else:

			abcDetails = abc.getAbstractDetails(quotNum)
			
			if abcDetails != []:
				response = HttpResponse('existing')
			
			else:

				counter = 1
				
				for x in compList:
					
					compDetails = sup.getSupllierDetails(x[1])
					
					outputData[str(counter)] = {'compid':compDetails[0][0],
												'name':compDetails[0][1], 
												'address':compDetails[0][2],
												'rep':compDetails[0][3],
												}
					counter = counter + 1

				response = HttpResponse(json.dumps(outputData), content_type="application/json")								
	
	return response

def getReqQItems(request):
	
	outputData = {}

	if request.method == 'POST':
		quotNum = request.POST['quotNum']
		itemList = reqQ.getReqItems(quotNum)
		counter = 1
		for x in itemList:
			
			outputData[str(counter)] = {'description':x[2],
										'quantity':x[3], 
										'unit':x[4],
										'price':x[5],
										}
			counter = counter + 1							
	
	return HttpResponse(json.dumps(outputData), content_type="application/json")

def addPO(request):
	
	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)
	
	ordNum = ''
	prRef = ''
	suppID = ''
	deldate = ''
	procmode = ''
	delplace = ''
	delterm = ''
	payterm = ''
	conf = ''
	
	reqnum = l.generateLogID()
	
	itemList = {}

	if request.method == 'POST':
		
		itemList = json.loads(request.POST.get('theMatrix'))
		
		ordNum = request.POST['ordNum']
		prRef = request.POST['prRef']
		suppID = request.POST['suppID']
		deldate = request.POST['deldate']
		procmode = request.POST['procmode']
		delplace = request.POST['delplace']
		delterm = request.POST['delterm']
		payterm = request.POST['payterm']
		conf = request.POST['conf']

	
	f.createPO(ordNum, suppID, procmode, deldate, delplace, delterm, payterm, 0, conf, prRef, itemList)
	
	return HttpResponse('')

def addPObyAbs(request):
	
	
	absNum = ''
	

	if request.method == 'POST':
		
		absNum = request.POST['ordNum']


	f.createPOFromAbs(absNum)
	
	return HttpResponse('')	

def validatePO(request):

	theCookieValue = getSessionData(request, 'theCookie')
	logDetails = l.getLogDetails(theCookieValue)

	if request.method == 'POST':
		
		ponum = request.POST['ponum']
		appPO = request.POST['poNumber']
		valType = request.POST['validateType']
		
		print('ponum '+ponum+' valtype '+ valType)

		if valType == 'approve':
			
			fundRef = request.POST['fundRef']
			approvalDate = request.POST['approvalDate']
			servingDate = request.POST['servingDate']

			f.validateApprovePO(ponum, appPO, fundRef, approvalDate, servingDate)
		
		notifNum = n.getNotifFromDataWithRef(ponum, logDetails[0][1],'po')
		n.updateNotif(notifNum[0][0])

	return HttpResponse('')

def getEmployeeData(request):
	
	outputData = {}

	if request.method == 'POST':
		inputData = request.POST['inputName']
		dataToSearch = str(inputData)
		
		
		empFindResults = e.findEmployee(str(inputData))
		
		for x in empFindResults:
			
			outputData[x[0]] = {
				'name': str(x[1]) + ", "+ str(x[2]) 
			}
	
	return HttpResponse(json.dumps(outputData), content_type="application/json")


def generateRQDocument(request):
		
		quoNumber = ''

		if request.method == 'POST':
			quoNumber = request.POST.get('theRQNum')

		
		theCookieValue = getSessionData(request, 'theCookie')

		logDetails = l.getLogDetails(theCookieValue)

		unameData = u.getUnameFromID(logDetails[0][1]) 
		userdata = u.getUserDetails(unameData[0][0])

		procOff = off.getOfficeDetails('PROC')
		procOffHeadDetails = e.getEmployeeDetails(procOff[3])
		procOffHead = procOffHeadDetails[0][1] +" "+ procOffHeadDetails[0][2]
		
		rqItems = reqQ.getReqItems(quoNumber)

		quoDetails = reqQ.getRequestDetails(quoNumber)
		quoSuppliers = reqQ.getReqComp(quoNumber)
		cansvasserDetails = e.getEmployeeDetails(quoDetails[0][5])
		
		cansvasserName = cansvasserDetails[0][1]+" "+cansvasserDetails[0][2]

		loopRef = genLoopRangeString(19, rqItems)

		counter = 1
		
		output = PdfFileWriter()
		

		for x in quoSuppliers:
			
			suppID = x[1]
			suppDetails = sup.getSupllierDetails(suppID)	

			renderPDFwithoutResponse(request,'pdf_templates/doc-rqTest.html', [(suppDetails[0][1],suppDetails[0][2], procOffHead.upper()),(quoDetails[0][0], str(quoDetails[0][4]), cansvasserName.upper(), quoDetails[0][2], quoDetails[0][3],quoDetails[0][1],),], rqItems,[],[], str(quoNumber)+'_'+str(counter), loopRef, 'legal')

			append_pdf(PdfFileReader(open('{}/Project_SMO_Inventory/static/src/mypdf.pdf'.format(dirreq),"rb")),output)
			output.write(open( '{}/Project_SMO_Inventory/static/src/'.format(dirreq)+'mypdfRQ.pdf',"wb"))

		

		fs = FileSystemStorage('{}/Project_SMO_Inventory/static/src/'.format(dirreq))

		with fs.open('mypdfRQ.pdf') as pdf:

			response = HttpResponse(pdf, content_type='application/pdf')
			
			response['Content-Disposition'] = 'attachment; filename="ReqQuot_'+str(quoNumber)+'.pdf"'
			
			return response			

		
		return response



def generatePODocumentFromAbs(request, refData):

		absNum = refData.replace('_','-')
		
		rqDetails = reqQ.getRequestDetails(absNum)

		winningSuppList = abc.getWinningSuppliers(absNum)

		output = PdfFileWriter()
		counter = 1

		chacellor = kp.getChancellor()
		empDetails = e.getEmployeeDetails(chacellor)
		acct = off.getOfficeHeadFromOffice('AcctO')
		budget = off.getOfficeHeadFromOffice('Budget')

		empAcctDetails = e.getEmployeeDetails(acct[0][0])
		empBudgetDetails = e.getEmployeeDetails(budget[0][0])



		for  x in winningSuppList:
			
			print(x[0])

			suppDetails = sup.getSupllierDetails(x[0])


			toPageItems = []

			winningItems = abc.getSupplierWinningItems(absNum, x[0])

			theTotal = 0
			
			

			compTerms = reqQ.getComTerms(absNum, x[0])
			
			for y in winningItems:
				
				theItemDetails = abc.getAbstractItem(absNum, y[2])
				
				toPageTotal = theItemDetails[0][4]*y[3]
				
				toPageItems = toPageItems + [(y[2], theItemDetails[0][4], theItemDetails[0][3], y[6], theItemDetails[0][2], y[3], toPageTotal),]

				theTotal = theTotal + toPageTotal
			
			loopRef = genLoopRangeString(20, winningItems)

			theTotalInWords = num2words(theTotal)
			
			renderPDFwithoutResponse(request,'pdf_templates/doc-poTest.html', [(suppDetails[0][1], suppDetails[0][2],suppDetails[0][6], suppDetails[0][3], theTotal, theTotalInWords, compTerms[0][3], num2words(compTerms[0][3])),empDetails[0],empAcctDetails[0],empBudgetDetails[0]], toPageItems,[],[], 'PO_'+str(counter), loopRef, 'legal')	

			append_pdf(PdfFileReader(open('{}/Project_SMO_Inventory/static/src/mypdf.pdf'.format(dirreq),"rb")),output)
			output.write(open( '{}/Project_SMO_Inventory/static/src/'.format(dirreq)+'mypdfPO.pdf',"wb"))

		
		fs = FileSystemStorage('{}/Project_SMO_Inventory/static/src/'.format(dirreq))	
		
		with fs.open('mypdfPO.pdf') as pdf:

			response = HttpResponse(pdf, content_type='application/pdf')
			
			response['Content-Disposition'] = 'attachment; filename="POFrom_AbsNum_'+absNum+'.pdf"'
			
			return response	



def generatePODocument(request):
	
	return renderPDF(request, 'pdf_templates/doc-poTest.html', [], [], [], [], 'po', '', 'legal')

#----------------------------------------------------------------------------------

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

def setReponse(request, outputPage, pageData1, pageData2, pageData3, pageData4, pageData5):
	
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
			'dept':  deptDetails[1],
			'taskNum': taskNum,
			'notifNum': notifNum,
			'notifDetails': notifs,
			'taskDetails': tasks,
			'pageData1': pageData1,
			'pageData2': pageData2,
			'pageData3': pageData3,
			'pageData4': pageData4,
			'pageData5': pageData5,
		
		}

		if any( 2 == code for code in acctType):

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

def renderPDFwithoutResponse(request, template, pageData1, pageData2, pageData3, pageData4, pdfName, loopRefNum, csScript):
		
		

		c = {
			
			'pageData1': pageData1,
			'pageData2': pageData2,
			'pageData3': pageData3,
			'pageData4': pageData4,
			'loopRef' : loopRefNum,
		
		}

		html_string = render_to_string(template,c)
		
		html = HTML(string=html_string).write_pdf('{}/Project_SMO_Inventory/static/src/mypdf.pdf'.format(dirreq), stylesheets=[CSS(string='@page {size: '+csScript+'; margin:35px;}')]);
		


		print(c)
		print("Done")
		

def mergePDFs(request):
	pass

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

def generatePONum(counter):

	maxCounter = str(counter).zfill(3)
	year = datetime.now().year
	suffix = float(str(year)[-3:]) if '.' in str(year)[-2:] else int(str(year)[-2:])

	return maxCounter+"-"+str(suffix)


def genLoopRangeString(maxRange, refList):
	
	output = ''
	maxInRange = maxRange - len(refList)
	
	for x in range(2, maxInRange):
		output = output + 'x'

	return output	

def append_pdf(input,output):
	[output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

if __name__ == '__main__':
	print(dirreq)
	print('{}\Project_SMO_Inventory\static\src'.format(dirreq))