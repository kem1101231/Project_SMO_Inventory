from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import HttpResponse
import json
import json
from os.path import dirname, abspath
import sys
from datetime import datetime



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
from inspect_accept_report_2 import InsepectionAndAcceptanceReceipt_2
from purchase_order import PurchaseOrder
from purchase_request import PurchaseRequest
from property_acc_receipt import PropertyAcceptanceReceipt
from request_for_quotation import RequestForQuotation
from purchase_order import PurchaseOrder
from office import Offices
from key_positions import KeyPositions
from suppliers import Suppliers
from items import Items
from equipment import Equipment
from requisition_issuance_slip import RequisitionAndIssuanceSlip
from supply import Supply
from waste import Waste
from abstract_of_canvass import AbstractOfCanvass
from liquidating_damages import LiquidatingDamages


f = Functions()
u = User()
l = Log()
e = Employees()
n = Notification()
ins = InsepectionAndAcceptanceReceipt_2()
pOrd = PurchaseOrder()
preq = PurchaseRequest()
propAR = PropertyAcceptanceReceipt()
reqQ = RequestForQuotation()
pord = PurchaseOrder()
off = Offices()
kp = KeyPositions()
suppl = Suppliers()
itemC = Items()
equip = Equipment()
ris_Class = RequisitionAndIssuanceSlip()
supplyC = Supply()
waste_Class = Waste()
abc = AbstractOfCanvass()
ldClass = LiquidatingDamages()

templateFolder = 'inventory_office'
urlHead = '/inventory_office'

def index(request):
    
    suppList = f.getAllSupplies()
   
    return setReponse(request, templateFolder+'/home.html', [suppList,], [], [], [], [])

def search(request):


    theCookieValue = getSessionData(request, 'theCookie')
    logDetails = l.getLogDetails(theCookieValue)

    reference = request.POST.get('search_input','')

    print("Input")
    print(reference)    

    result = f.findInfo(reference)

    return setReponse(request, templateFolder+'/search.html', result, [], [], [], [])
    
def searchTest(request):


    theCookieValue = getSessionData(request, 'theCookie')
    logDetails = l.getLogDetails(theCookieValue)

    reference = request.POST.get('search_input','')

    #result = f.findInfo(reference)

    return setReponse(request, templateFolder+'/searchTest.html', [], [], [], [], [])
    

def searchRedirectDetails(request, refData, refType):
    
    return HttpResponse(refData)

def addAcct(request):

    parNum = propAR.generateRecNum()

    return setReponse(request, templateFolder+'/add-acct-by-po.html', [(parNum,),], [], [], [], [])
'''
def acct(request):

    empIds = e.getAllEmployeeID()

    toPageData = []
    
    for x in empIds:


        toPageDataInput = []
        empDetails = e.getEmployeeDetails(x[0])
        parList = propAR.getPAROFID(x[0])

        
        if parList != []:
            
            toPageDataInput = toPageDataInput + [(empDetails[0][6]+" "+empDetails[0][1]+" "+empDetails[0][7]+" "+empDetails[0][2]+", "+empDetails[0][8],),] 
            
            parListData = []
           
            for y in parList:
                
                parDetails = propAR.getPARDetails(y[0])
                parItems = propAR.getPARItems(y[0])
                parItemsOnAcct = propAR.getPARItemsOnAcct(y[0])
                parItemsNotOnAcct = propAR.getPARItemsNotOnAcct(y[0])

                parCost = propAR.getPARTotal(parItems)

                totalparItemsOnAcct = propAR.getTotalQuantityOfPAR(parItemsOnAcct)
                totalparItemsNotOnAcct = propAR.getTotalQuantityOfPAR(parItemsNotOnAcct)
                parListData = parListData + [(parDetails[0][0], parDetails[0][1], parCost, totalparItemsOnAcct, totalparItemsNotOnAcct),]

            toPageDataInput = toPageDataInput + [parListData]       
        
            toPageData = toPageData + [toPageDataInput]

    return setReponse(request, templateFolder+'/all_par.html', toPageData, [], [], [], [])
'''


def acct(request):

    toPageData = []

    parList = propAR.getAllPAR()

    for x in parList:
        
        parItems = propAR.getPARItems(x[0])
        parTotalQty = propAR.getTotalQuantityOfPAR(parItems)
        parTotal = propAR.getPARTotal(parItems)
        
        empDetails = e.getEmployeeDetails(x[2])
        
        endUser = 'Information Not Available'
        if empDetails != []:
            endUser = empDetails[0][6]+" "+empDetails[0][1]+" "+empDetails[0][7]+" "+empDetails[0][2]+" "+empDetails[0][8]

        parURL = str(x[0]).replace('-','_')
           


        toPageData += [(x[0], x[3], parTotal, parTotalQty, endUser, parURL),]

       #[(len(toPageData[0]),),]
    return setReponse(request, templateFolder+'/all_par.html', toPageData, [], [], [], [])


def wMR(request):

    toPageData = []

    wmrList = waste_Class.getAllWMRwithDetails()
    print('//------------------------------------')
    print(wmrList)

    for x in wmrList:
        print(x[0])
        print(x)
        toPageData = toPageData + [x + (x[0].replace('-','_'),)]

    print(toPageData)
    return setReponse(request, templateFolder+'/all_wmr.html', toPageData, [], [], [], [])

def offices(request):

    pageData = []

    offices = off.getAllOfficesSorted()

    for offid in offices:

        empList = e.getEmployeeByOff(offid[0])
        offTotalValue = 0

        for xy in empList:

            allPARTotal = 0
            allPARQuantity = 0
            parList = propAR.getPAROFID(xy[0])

            for x in parList:
                parTotal = propAR.getPARTotal(propAR.getPARItems(x[0]))
                parItemTotal = propAR.getTotalQuantityOfPAR(propAR.getPARItems(x[0]))

                allPARTotal = allPARTotal + parTotal
                allPARQuantity = allPARQuantity +parItemTotal

            offTotalValue = offTotalValue + allPARTotal    

                   
        offDetails = off.getOfficeDetails(offid[0])
        
        headName = None
        
        empDetails = e.getEmployeeDetails(offDetails[3])
       
        pageData = pageData + [ offDetails + (offTotalValue, empDetails, str(offid[0]).replace('-','_')) ]
    
    return setReponse(request, templateFolder+'/acct-off.html', pageData, [], [], [], [])


def offList(request):
    return setReponse(request, templateFolder+'/off_list.html', [], [], [], [], [])

def risList(request):

    toPageData = []

    risS = ris_Class.getAllRIS()

    for x in risS:
        
        risDetails = ris_Class.getRISDetails(x[0])
        empDetails = e.getEmployeeDetails(risDetails[0][4])
        offDetails = off.getOfficeDetails(empDetails[0][4])
      
        toPageData = toPageData + [(risDetails[0][3],offDetails[1],risDetails[0][2],risDetails[0][5],risDetails[0][1],risDetails[0][9],risDetails[0][0].replace('-','_')),]

    return setReponse(request, templateFolder+'/all_ris.html', toPageData, [], [], [], [])    

def offDetails(request, refData):

    offid = refData.replace('_','-')

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
        parList = propAR.getPAROFID(xy[0])
        empD = e.getEmployeeDetails(xy[0])

        for x in parList:
            parTotal = propAR.getPARTotal(propAR.getPARItems(x[0]))
            parItemTotal = propAR.getTotalQuantityOfPAR(propAR.getPARItems(x[0]))

            allPARTotal = allPARTotal + parTotal
            allPARQuantity = allPARQuantity + parItemTotal

        empListToPage = empListToPage + [empD[0]+(allPARTotal, allPARQuantity),]    

        offTotalPAR = offTotalPAR + len(parList)
        offTotalValueQTY = offTotalValueQTY + allPARQuantity
        offTotalValue = offTotalValue + allPARTotal    

        
           
    empDetails = e.getEmployeeDetails(offDetails[3])

    supplyList = f.getAllSuppliesWithOfficeInfo(offid)
    offitems = f.getItemsByOffice( offid)    

    return setReponse(request, templateFolder+'/off_details.html', [offDetails, empDetails[0], (offTotalPAR, offTotalValueQTY,offTotalValue,''), subOffName, empListToPage], [supplyList, offitems], [], [], [])

def createWMR(request):

    return setReponse(request, templateFolder+'/create_wmr.html', [], [], [], [], [])

def wmrDetails(request, refData):

    return setReponse(request, templateFolder+'/wmr_details.html', [], [], [], [], [])

def prDetails(request, refData):

    prNum = refData.replace('_','-')
    reqNumber = preq.getReqNumFromPR(prNum)
    

    prDetails_1 = preq.getPRDetails(prNum)

    rqFromRef = reqQ.getReqNumFromRefNum(prNum)
    poRef = pOrd.getPONumFromPRRef(prDetails_1[0][1])

    
    empDetails_1 = e.getEmployeeDetails(prDetails_1[0][4])
    offDetails_1 = off.getOfficeDetails(empDetails_1[0][4])
    poDetails_1 = None
    
    if poRef != None:
        poDetails_1 = pord.getPODetails(poRef)[0]

    prItems_1 = preq.getItemByPR(prNum) 
   
    return setReponse(request, templateFolder+'/pr_details.html', [prDetails_1[0], poDetails_1, (rqFromRef,), empDetails_1[0], offDetails_1], prItems_1, [], [], [])

def rqDetails(request, refData):

    rqNum = refData.replace('_','-')

    quoDetails = reqQ.getRequestDetails(rqNum)
    abcDetails = abc.getAbstractDetails(rqNum)
    prRefDetails = preq.getPRDetails(preq.getReqNumFromPR(quoDetails[0][1])[0][0])
    prRefString = prRefDetails[0][1]
    empDetails = e.getEmployeeDetails(prRefDetails[0][4])
    offDetails = off.getOfficeDetails(empDetails[0][4])
    suppliers = None
    prItems = None
    reqQItems = None

    

    return setReponse(request, templateFolder+'/rq_details.html', [abcDetails[0], quoDetails[0], prRefDetails[0]+(prRefString.replace('-','_'),),empDetails[0], offDetails], [], [], [], [])

def parDetailsfromRef(request, refData):
    
    parNum = refData.replace('_', '-')

    parDetails = propAR.getPARDetails(parNum)
    parItems = []

    parItems = parItems + propAR.getPARItems(parNum)
    parItems = parItems + propAR.getPARItemsFromNoInvNum(parNum)

    empDetails = e.getEmployeeDetails(parDetails[0][2])
    offDetails = off.getOfficeDetails(empDetails[0][4])
    iarDetails = ins.getIARDetails(parDetails[0][8])

    prRef = preq.getPRNumforPONumForNew(parDetails[0][6])

    prPOTimelineDetails = [(None,),]
    
    if prRef != []:
        prPOTimelineDetails = preq.getProCTimeLineDetails(prRef[0][0])

    parTotal = propAR.getPARTotal(parItems)

    parItemsToPage = []
    parItemsToPage2 = []

    for x in parItems:
        
        if '$' in x[2]:
            descripArr = str(x[2]).split('$')
           
            parItemsToPage = parItemsToPage + [(x[0], x[1], descripArr, x[3], x[4], x[5], x[6], x[7], x[8], x[9], 'multi')]
        else:
            parItemsToPage = parItemsToPage + [x+('none',),]    

    parItemsList = equip.getAllEquiListbyPARNum(parNum)  
    counter = 1
    for x in parItemsList:
        
        toArrX = ['1',x]    
        
        itemDetails = equip.getEquiIndiDetailsbyPARNum(x[0], parNum)

        print(toArrX)
        
        if "$" in x[0]:
            
            descripArr = (x[0]).split('$')
            toArrXx = list(x)

            toArrXx[0] = descripArr
            toArrX[0] = '2'
            toArrX[1] = tuple(toArrXx)


           

        parItemsToPage2 = parItemsToPage2 + [(toArrX, len(itemDetails), itemDetails, counter)]      

        counter = counter + 1


    return setReponse(request, templateFolder+'/par_details.html', [parDetails[0], empDetails[0], offDetails, iarDetails[0], prPOTimelineDetails[0], (parTotal,)], parItemsToPage, parItemsToPage2, [], [])

def displayPODetails(request, refData):

    refPOCode = refData.replace('_', '-')

    refPO = pord.getPONumFromAppPONum(refPOCode)

    poDetails = pord.getPODetails(refPO)
    prDetails = preq.getPRDetails(preq.getReqNumFromPR(poDetails[0][13])[0][0])
    poItems = pord.getItemByPO(refPO)
    poTotal = pord.getTotalCostofPO(poItems)
    empDetails = e.getEmployeeDetails(prDetails[0][4])
    offDetails = off.getOfficeDetails(empDetails[0][4])
    suppDetails = suppl.getSupllierDetails(poDetails[0][1])
    iarNum = ins.getIARNumFromRef(refPO)
    iarDetails = None
    
    quoNum = reqQ.getReqNumFromRefNum(poDetails[0][13])


    refDate = datetime.datetime.strptime(str(poDetails[0][17]), "%Y-%m-%d")
    print(type(refDate))
    delDate = poDetails[0][17] + datetime.timedelta(days=30)

    quoNumRef = ''
    if quoNum != None:
        quoNumRef =  quoNum.replace('-','_')

    theString = poDetails[0][6]


    if iarNum != None:
        iarDetails = ins.getIARDetails(iarNum)[0]+(iarNum.replace('-','_'),)

    
    print([poDetails[0]+(poTotal,),prDetails[0]+(str(poDetails[0][13]).replace('-','_'), delDate), empDetails[0], (offDetails[1],), suppDetails[0], iarDetails, (quoNum, quoNumRef)])

    return setReponse(request, templateFolder+'/po_details_new.html',[poDetails[0]+(poTotal,),prDetails[0]+(str(poDetails[0][13]).replace('-','_'), delDate), empDetails[0], (offDetails[1],), suppDetails[0], iarDetails, (quoNum, quoNumRef, refData)], poItems, [], [], [])

def empDetails(request, refData):

    idNum = refData.replace('_','-')

    empDetails = e.getEmployeeDetails(idNum)
    offDetails = off.getOfficeDetails(empDetails[0][4])

    parStat = f.getPARStat(idNum)

    parList = propAR.getPAROFID(idNum)
    outputItemList = []

    if parList != []:
        
        for x in parList:
            
            parDetails = propAR.getPARDetails(x[0])
            parItems = propAR.getPARItems(x[0])
            parTotal = propAR.getPARTotal(parItems)
            parTotalQuantity = propAR.getTotalQuantityOfPAR(parItems)
            intoData = parDetails[0] + (parTotal, parTotalQuantity, str(x[0]).replace('-','_'))
            
            outputItemList = outputItemList + [(intoData),]   

    itemList = f.getItemsByPersonelID(idNum)

    return setReponse(request, templateFolder+'/emp_details.html', itemList, parStat, outputItemList, [empDetails,offDetails], [])
'''
def supplyDetails(request, refData):

    refPO = refData.replace('_', '-')
    print(refPO)
    supply_Details = f.getCompleteSupplyDetails(refPO)
    print(supply_Details)
       
    return setReponse(request, templateFolder+'/supply_details.html', supply_Details, [], [], [], [])
'''
def risDetails(request):
    slipnum = getSessionData(request, 'theSlipNum')

    risDetails = ris_Class.getRISDetails(slipnum)
    reqOfficerDetails = e.getEmployeeDetails(risDetails[0][4])
    reqOfficerName = reqOfficerDetails[0][6]+' '+reqOfficerDetails[0][1] +' ' + reqOfficerDetails[0][7]+' '+ reqOfficerDetails[0][2]+' ,'+reqOfficerDetails[0][8]
    reqOff = off.getOfficeDetails(reqOfficerDetails[0][4])

    risItems = ris_Class.getItemByRIS(slipnum)

    return setReponse(request, templateFolder+'/ris_details.html', risDetails, [(reqOfficerName, reqOff[1])], risItems, [], [])

def risWithRefDetails(request, refData):
    slipnum = refData.replace('_','-')

    risDetails = ris_Class.getRISDetails(slipnum)
    reqOfficerDetails = e.getEmployeeDetails(risDetails[0][4])
    reqOfficerName = reqOfficerDetails[0][6]+' '+reqOfficerDetails[0][1] +' ' + reqOfficerDetails[0][7]+' '+ reqOfficerDetails[0][2]+' ,'+reqOfficerDetails[0][8]
    reqOff = off.getOfficeDetails(reqOfficerDetails[0][4])

    risItems = ris_Class.getItemByRIS(slipnum)

    return setReponse(request, templateFolder+'/ris_details.html', risDetails, [(reqOfficerName, reqOff[1])], risItems, [], [])


def prList(request):

    toPageData = []

    initpenPR = f.getAllPRListByStatus('pending', 'init')
    penPR = f.getAllPRListByStatus('pending', 'final')
    appPRList = f.getAllPRListByStatus('approved', 'final')


    toPageData = initpenPR + penPR + appPRList

    return setReponse(request, templateFolder+'/all_pr.html', toPageData, [], [], [], [])   

def poList(request):

    toPageData = [] 

    poList = pord.getAllApprovedPO()

    for x in poList:
        #suppDetails = suppl.getSupllierDetails(x[1])
        toPageData = toPageData + [x + ('',)+ (x[18].replace('-','_'),),]
    
    return setReponse(request, templateFolder+'/po.html', toPageData,[],[],[],[])   


def quoList(request):

    toPageData = []
    quoList = reqQ.getAllReqQuo()

    for x in quoList:
        compNums = len(reqQ.getReqComp(x[0]))
        toPageData = toPageData + [x+(compNums,x[0].replace('-','_'))]
  

    return setReponse(request, templateFolder+'/quotations.html',toPageData,[],[],[],[])


def addInven(request):
    return setReponse(request, templateFolder+'/add_inventory.html', [], [], [], [], [])


def addEqui(request):
    return setReponse(request, templateFolder+'/add-equi.html', [], [], [], [], [])

def addReceive(request):

    iarnum = ins.generateReqNum()

    return setReponse(request, templateFolder+'/add-receive-new-v3-existing.html', [(iarnum, ),], [], [], [], [])

def addReceiveExisting(request):

    iarnum = ins.generateReqNum()

    return setReponse(request, templateFolder+'/add-receive-new-v3-existing.html', [], [], [], [], [])


def addReceiveNew(request):

    iarnum = ins.generateReqNum()

    return setReponse(request, templateFolder+'/add-receive-new.html', [(iarnum, ),], [], [], [], [])

def addReceiveNewer(request):

    iarnum = ins.generateReqNum()

    return setReponse(request, templateFolder+'/add-receive-new-v4.html', [(iarnum, ),], [], [], [], [])



def itemList(request):
    
    itemlist = f.getListFromItemList(itemC.getAllItemsWithDetails(), 1)
    
    '''
    for idx, x in enumerate(itemlist):
        
        if "$" in x[1]:
            xList = list(x)
            xList[1] = ('multi', str(x[1]).split('$'))
            xTuple = tuple(xList)

            itemlist[idx] = xTuple
    '''
    return setReponse(request, templateFolder+'/item_list.html', itemlist, [], [], [], [])

def iarDisplayDetails(request):
    return setReponse(request, templateFolder+'/iar_details.html', [], [], [], [], [])

def iarDisplayDetailsFromRef(request, refData):

    iarNumFromRef = refData.replace('_','-')
    iarDetails = ins.getIARDetails(iarNumFromRef)
    poDetails = pOrd.getPODetails(iarDetails[0][1])

    supplierDetails = suppl.getSupllierDetails(poDetails[0][1])

    iarItems = ins.getIARItems(iarNumFromRef)

    totalMiss = 0
    totalToRec = 0
    
    for xx in iarItems:
        totalMiss = totalMiss + xx[9]
        totalToRec = totalToRec + xx[4]

    recOffDetails = e.getEmployeeDetails(iarDetails[0][11])
    insOffDetails = e.getEmployeeDetails(iarDetails[0][8])

    recOffName = recOffDetails[0][6] + ' ' + recOffDetails[0][1] + ' ' + recOffDetails[0][7] + ' ' + recOffDetails[0][2] + ' ' + recOffDetails[0][8]
    InsOffName = insOffDetails[0][6] + ' ' + insOffDetails[0][1] + ' ' + insOffDetails[0][7] + ' ' + insOffDetails[0][2] + ' ' + insOffDetails[0][8]


    return setReponse(request, templateFolder+'/iar_details.html', [iarDetails[0], poDetails[0], (recOffName, InsOffName, totalToRec, totalMiss)], iarItems, supplierDetails, [], [])




'''
def iarDisplayDetailsFromPORef(request, refData):

    poRefData = pOrd.getPONumFromAppPONum(refData.replace('_','-'))
    poDetails = pOrd.getPODetails(poRefData)

    supplierDetails = suppl.getSupllierDetails(poDetails[0][1])
    
    iarNumList_2 = ins.getAllIARNumFromRef(poRefData)

    toPageIARData = []

    for x in iarNumList_2:
        
        intoPageData = []

        iarDetails = ins.getIARDetails(x[0])

        iarItems = ins.getIARItems(x[0])

        

        totalMiss = 0
        totalToRec = 0
        
        for xx in iarItems:
            totalMiss = totalMiss + xx[9]
            totalToRec = totalToRec + xx[4]

        recOffDetails = e.getEmployeeDetails(iarDetails[0][11])
        insOffDetails = e.getEmployeeDetails(iarDetails[0][8])

        recOffName = recOffDetails[0][6] + ' ' + recOffDetails[0][1] + ' ' + recOffDetails[0][7] + ' ' + recOffDetails[0][2] + ' ' + recOffDetails[0][8]
        InsOffName = insOffDetails[0][6] + ' ' + insOffDetails[0][1] + ' ' + insOffDetails[0][7] + ' ' + insOffDetails[0][2] + ' ' + insOffDetails[0][8]

        intoPageData = intoPageData + iarDetails + [(totalToRec, totalMiss, recOffName, InsOffName),] + [iarItems]

        toPageIARData = toPageIARData + [intoPageData]

    
    return setReponse(request, templateFolder+'/iar_details_by_po.html', [poDetails[0],supplierDetails[0]], toPageIARData, [], [], [])
'''

def iarDisplayDetailsFromPORef(request, refData):

    poRef = refData.replace('_','-')
    prRefFromPO = preq.getPRNumforPONum(poRef)


    prPOTimelineDetails = preq.getProCTimeLineDetails(prRefFromPO[0][0])
    iarList = ins.getAllIARNumFromRef(poRef)
    lqDamage = ldClass.getLiqDamageFromPO(poRef)
    latestDelDate = ins.getLatestDelDate(poRef)

    iarCompltChck = None
    iarDelRemarks = None

    if len(iarList) != 1:
        iarCompltChck = ins.getDelStatusForMultiIAROfAPO(poRef)
      
    else:
        iarDetails = ins.getIARDetails(iarList[0][0])
        iarCompltChck = iarDetails[0][12]

    if latestDelDate > prPOTimelineDetails[0][20]:
        iarDelRemarks = False
    else:
        iarDelRemarks = True       

    iarListToPage = []    
    
    for x in iarList:
        iarXDetails = ins.getIARDetails(x[0])
        totalIARCost = ins.getTotalIARCost(x[0])

        recOffDetails = e.getEmployeeDetails(iarXDetails[0][11])
        insOffDetails = e.getEmployeeDetails(iarXDetails[0][9])

        xDelRemarks = False

        if iarXDetails[0][10] <= prPOTimelineDetails[0][20]:
            xDelRemarks = True
        
        recOffName = recOffDetails[0][6] + ' ' + recOffDetails[0][1] + ' ' + recOffDetails[0][7] + ' ' + recOffDetails[0][2] + ' ' + recOffDetails[0][8]
        InsOffName = insOffDetails[0][6] + ' ' + insOffDetails[0][1] + ' ' + insOffDetails[0][7] + ' ' + insOffDetails[0][2] + ' ' + insOffDetails[0][8]
        

        iarXItems = ins.getIARItems(x[0])
        iarXItemsToPage = f.getListFromItemList(iarXItems, 3)
        
        '''
        for x in iarXItems:
            if "$" in x[3]:
                descripArr = str(x[3]).split('$')
                iarXItemsToPage = iarXItemsToPage + [(x[0],x[1],x[2],descripArr, x[4],x[5], x[6],x[9],x[11]),]
            else:
                iarXItemsToPage = iarXItemsToPage + [(x[0],x[1],x[2],x[3], x[4],x[5], x[6],x[9],x[11]),]  
        '''
        
        iarListToPage = iarListToPage + [(x[0], xDelRemarks, iarXDetails[0][10], iarXDetails[0][5],iarXDetails[0][6], iarXDetails[0][12], 0, recOffName, InsOffName, iarXItemsToPage, totalIARCost),]




    return setReponse(request, templateFolder+'/iar_details_by_po.html', [(poRef, prPOTimelineDetails[0][18], prPOTimelineDetails[0][19], prPOTimelineDetails[0][20]),(latestDelDate, iarDelRemarks, iarCompltChck, lqDamage[0][0])], iarListToPage, [(refData,),], [], [])


def iarDisplayDetailsFromPORefWithIAR(request, refData, refData2):

    poRef = refData.replace('_','-')
    iarNum = refData2.replace('_','-')
    
    prPOTimelineDetails = []
    iarCompltChck = None
    iarDelRemarks = True 
    
    prRefFromPO = preq.getPRNumforPONum(poRef)
    iarList = ins.getAllIARNumFromRef(poRef)
    lqDamage = ldClass.getLiqDamageFromPO(poRef)
    latestDelDate = ins.getLatestDelDate(poRef)

    procData1 = ''
    procData2 = ''
    procData3 = ''


    
    if prRefFromPO != []:
        prPOTimelineDetails = preq.getProCTimeLineDetails(prRefFromPO[0][0])
    
        if latestDelDate > prPOTimelineDetails[0][20]:
            iarDelRemarks = False
        else:
            iarDelRemarks = True  

        
        procData1 = prPOTimelineDetails[0][18]
        procData2 = prPOTimelineDetails[0][19]
        procData3 = prPOTimelineDetails[0][20]
         

        

    if len(iarList) != 1:
        iarCompltChck = ins.getDelStatusForMultiIAROfAPO(poRef)
      
    else:
        iarDetails = ins.getIARDetails(iarList[0][0])
        iarCompltChck = iarDetails[0][12]


    iarListToPage = []    
    
    for x in iarList:
        iarXDetails = ins.getIARDetails(x[0])
        totalIARCost = ins.getTotalIARCost(x[0])

        recOffDetails = e.getEmployeeDetails(iarXDetails[0][11])
        insOffDetails = e.getEmployeeDetails(iarXDetails[0][9])

        xDelRemarks = False

        if prRefFromPO != []:
            if iarXDetails[0][10] <= prPOTimelineDetails[0][20]:
                xDelRemarks = True
        
        recOffName = recOffDetails[0][6] + ' ' + recOffDetails[0][1] + ' ' + recOffDetails[0][7] + ' ' + recOffDetails[0][2] + ' ' + recOffDetails[0][8]
        InsOffName = insOffDetails[0][6] + ' ' + insOffDetails[0][1] + ' ' + insOffDetails[0][7] + ' ' + insOffDetails[0][2] + ' ' + insOffDetails[0][8]

        iarXItems = ins.getIARItems(x[0])
        iarXItemsToPage = f.getListFromItemList(iarXItems, 3)
        
        '''
        for x in iarXItems:
            if "$" in x[3]:
                descripArr = str(x[3]).split('$')
                iarXItemsToPage = iarXItemsToPage + [(x[0],x[1],x[2],descripArr, x[4],x[5], x[6],x[9],x[11]),]
            else:
                iarXItemsToPage = iarXItemsToPage + [(x[0],x[1],x[2],x[3], x[4],x[5], x[6],x[9],x[11]),]  
        '''
        iarListToPage = iarListToPage + [(x[0], xDelRemarks, iarXDetails[0][10], iarXDetails[0][5],iarXDetails[0][6], iarXDetails[0][12], 0, recOffName, InsOffName, iarXItemsToPage, totalIARCost),]
        



    return setReponse(request, templateFolder+'/iar_details_by_po.html', [(poRef, procData1, procData2, procData3),(latestDelDate, iarDelRemarks, iarCompltChck, lqDamage[0][0])], iarListToPage, [(refData, iarNum),], [], [])


def equi(request):

    totalQty = equip.getAllEquipmentQty()
    totalCost = equip.getAllEquipmentCost()
    totalOnAcct = equip.getAllEquipmentQtyonAcct()
    totalOnWaste = equip.getAllEquipmentQtyonWaste()
    
    particulars = equip.getAllEquiParticularswithDetails()

    toPageData = []

    for x in particulars:

        itemListByParticular = itemC.getAllItemsWithDetailsByClass(x[0])
        assetSavedItems = equip.getAllItemIDs()

        itemsListDetails = []
        
        if itemListByParticular != []:

            for y in itemListByParticular:

                if (y[0],) in assetSavedItems:
                    assetList = equip.getAllAssetsByItem(y[0])
                    
                    assetListDetails = []

                    for z in assetList:
                     
                        invQty = equip.getAllInvQtyByAssetID(z[0]) + equip.getAllInv_WQtyByAssetID(z[0])
                        invQtyAcct = equip.getAllAcctInvQtyByAssetID(z[0]) + equip.getAllAcctInv_WQtyByAssetID(z[0]) 
                        invQtyWaste = equip.getAllWasteInvQtyByAssetID(z[0]) + equip.getAllWasteInv_WQtyByAssetID(z[0])
                        
                        assetIDURL = str(z[0]).replace('-','_')

                        assetListDetails = assetListDetails + [z+(invQty, invQtyAcct, invQtyWaste, assetIDURL),]

                    toPageY = []

                    if '$' in y[1]:
                        toPageY = [str(y[1]).split('$'),'multi']
                    else:
                        toPageY = [y[1], 'non']       

                    itemsListDetails = itemsListDetails + [((toPageY, len(assetListDetails), y[4]), assetListDetails)]  

        toPageData = toPageData + [(x, itemsListDetails)]  
   

    itemlist = itemC.getAllEquipmentItemsWithDetails()

    return setReponse(request, templateFolder+'/equi-part.html', particulars, [(totalQty, totalCost, totalOnAcct, totalOnWaste),], itemlist, toPageData, [])

def inven(request):

    itemsSorted = itemC.getAllSupplyItemsSortedwithDetails()
    inventoryData = supplyC.getSupplyInventory()

    toPageInvData = []

    for x in inventoryData:
        toPageInvData = toPageInvData + [(x, (str(x[0]).replace('-','_')),),]
    
    risList = ris_Class.getAllPendingRIS()
    
    toPageStat = [f.getCurrQuarter(),(),(),(len(risList),)]

    suppList = f.getAllSupplies()

    return setReponse(request, templateFolder+'/inventory.html', toPageInvData, inventoryData, toPageStat, suppList, [])    

def getRIS(request):
    
    outputData = {}

    if request.method == 'POST':
        
        risList = ris_Class.getAllRIS()

        for x in risList:
            risDetails = ris_Class.getRISDetails(x[0])
            reqOfficer = e.getEmployeeDetails(risDetails[0][4])
            reqOff = off.getOfficeDetails(reqOfficer[0][4])
            outputData[x[0]] ={ 'risNum': risDetails[0][1],
                                'reqOff':reqOff[1],
                                'status':risDetails[0][5],
                                'relStatus':risDetails[0][9],
                                

            } 

    return HttpResponse(json.dumps(outputData), content_type="application/json")    

def getEquiParticulars(request):
    
    outputData = {}

    if request.method == 'POST':
        
        equipParticularList = equip.getAllEquiParticularswithDetails()

        for x in equipParticularList:
            
            outputData[x[0]] ={ 'name': x[1],                  

            } 
    
    return HttpResponse(json.dumps(outputData), content_type="application/json")    

def getApprovedRIS(request):
    
    outputData = {}

    if request.method == 'POST':
        pass

    return HttpResponse(json.dumps(outputData), content_type="application/json")    

def pcp(request):
    return setReponse(request, templateFolder+'/pcp.html', [], [], [], [], [])

def profile(request):
    return setReponse(request, templateFolder+'/profile.html', [], [], [], [], [])


'''
def receive(request):

    allPOs = pOrd.getAllPO()

    dataToPage = []

    for x in allPOs:
        
        iarNum = ins.getIARNumFromRef(x[0])

        
        if iarNum != None:
            
            iarDetails = ins.getIARDetails(iarNum)

            delStat = ""
            compStat = ""
            
            if iarDetails[0][9] == True:
                delStat = "Complete"
            else:
                delStat = "Incomplete"    
            if iarDetails[0][6] == True:
                compStat = "Working"   
            else:
                compStat = "Defective"    
                
            dataToPage = dataToPage + [(x[0], iarNum, iarDetails[0][10], delStat, compStat, iarNum.replace('-','_')),]

        else:
            
            dataToPage = dataToPage + [(x[0], "n/a", "n/a", "Incoming Del.", "n/a", iarNum.replace('-','_')),]    


    return setReponse(request, templateFolder+'/receive.html', dataToPage, [], [], [], [])
'''

def receive(request):

    allPOs = preq.getAllPRFromProcTimeline()

    dataToPage = []
    
    for x in allPOs:
        
        poDetails_2 = pOrd.getPODetails(x[0])

        

        iarNumList_2 = ins.getAllIARNumFromRef(x[0])
    
        if iarNumList_2 != None:
           
            dataToPage = dataToPage + [('po', x[0], 'Delivered', x[0].replace('-','_')),]
            
            for xx in iarNumList_2:
            
                iarDetails = ins.getIARDetails(xx[0])

                iarNum = xx[0]

                delStat = ""
                compStat = ""
                    
                if iarDetails[0][12] == True:
                    delStat = "Complete"
                else:
                    delStat = "Incomplete"    
                
                if iarDetails[0][6] == True:
                    compStat = "Working"   
                else:
                    compStat = "Defective"  

                totalCostOfIAR = ins.getTotalIARCost(iarNum)
     
                dataToPage = dataToPage + [('iar', iarNum, iarDetails[0][10], delStat, compStat, iarNum.replace('-','_'), totalCostOfIAR),]
        '''
        else:
                dataToPage = dataToPage + [('po', x[0], 'None', x[0].replace('-','_')),]
                dataToPage = dataToPage + [('iar', None),]
        '''
    return setReponse(request, templateFolder+'/receive.html', dataToPage, [], [], [], [])

def receiveList(request):

    dataToPage = []

    iarList = ins.getAllIARNums()
    
    for x in iarList:
        iarDetails = ins.getIARDetails(x[0])
        print(x)    
        print(iarDetails[0][2])

        prrefNum = preq.getPRNumforPONum(iarDetails[0][2])

        if prrefNum != []:
            #print(prrefNum[0][0])
            prProcDetails = preq.getProCTimeLineDetails(prrefNum[0][0])
            #poDetails = pOrd.getPODetails(iarDetails[0][2])
            dataToPage = dataToPage + [(iarDetails[0],prProcDetails[0], (str(iarDetails[0][2]).replace('-','_'), str(x[0]).replace('-','_'))),]
        
        else:
                
            dataToPage = dataToPage + [(iarDetails[0],(None,), (str(iarDetails[0][2]).replace('-','_'), str(x[0]).replace('-','_'))),]
    
    return setReponse(request, templateFolder+'/receive_iar.html', dataToPage, [], [], [], [])    

def receivedItem(request):

    dataToPage = []

    iarList = ins.getAllIARNums()

    for x in iarList:
        
        iarDetails = ins.getIARDetails(x[0])

        iarItems = ins.getIARItems(x[0])
        recItems = ins.getAvailableItems(x[0])

        profStat = ins.getProStatusOfIARItemsByIAR(x[0])

        itemsToPage = []
        
        if recItems != []:
            
            for idx, x  in enumerate(iarItems):

                descripString = str(x[3])
        
                if "$" in descripString :

                    arr = descripString.split('$')

                    itemsToPage = itemsToPage + [(x[0],x[1],x[2],arr[0],x[4],x[5],x[6])+recItems[idx],]


                    for y in range(1,len(arr)):
                        itemsToPage = itemsToPage + [('','','',arr[y],'','',''),]

                

                else:
                    itemsToPage = itemsToPage + [x+recItems[idx]]


            dataToPage = dataToPage + [[iarDetails[0]+(len(iarItems),profStat), itemsToPage]]

    return setReponse(request, templateFolder+'/received_items.html', dataToPage, [], [], [], [])

def waste(request):
    return setReponse(request, templateFolder+'/waste.html', [], [], [], [], [])

def equiDetails(request):

    equiID = getSessionData(request, 'theEquiID')
    
    equip_details =  equip.getAssetDetails(equiID)

    pageDataOffices = []

    offices = off.getAllOfficesSorted()

    for offid in offices:

        offDetails = off.getOfficeDetails(offid[0])
        pageDataOffices = pageDataOffices + [offDetails]


    return setReponse(request, templateFolder+'/equip_details.html', equip_details, [], [], pageDataOffices, [])


def equiDetailsWithName(request, refData):
     
    #equiID = getSessionData(request, 'theEquiID')
    
    #equip_details =  equip.getAssetDetails(equiID)

    assetId = refData.replace('_','-')
    assetDetails = equip.getAssetDetails(assetId)
    itemDetails = itemC.getItemDetails(assetDetails[0][1])
    partDetails = equip.getEquiParticularDetails(itemDetails[0][9])

    itemType = []

    if "$" in itemDetails[0][1]:
        itemType = [str(itemDetails[0][1]).split('$'),'multi']
    else:
        itemType = [itemDetails[0][1],'non']    
    
    invQty = equip.getAllInvQtyByAssetID(assetId) + equip.getAllInv_WQtyByAssetID(assetId)
    invQtyAcct = equip.getAllAcctInvQtyByAssetID(assetId) + equip.getAllAcctInv_WQtyByAssetID(assetId) 
    invQtyWaste = equip.getAllWasteInvQtyByAssetID(assetId) + equip.getAllWasteInv_WQtyByAssetID(assetId)

    pageDataOffices = []

    offices = off.getAllOfficesSorted()

    

    for offid in offices:

        offDetails = off.getOfficeDetails(offid[0])
        
        empList = e.getEmployeeByOff(offid[0])

        empListData = []

        if empList != None:

            for empid in empList:
                
                empDetails = e.getEmployeeDetails(empid[0])
                parList = propAR.getPAROFID(empid[0])

                parItems = []
                
                if parList != None:
                    


                    for parNum in parList:
                        
                        parItems = parItems + propAR.getInvenItemByAssetID(assetId, parNum[0]) 

                        parItems = parItems + propAR.getInvenWithOutNumItemByAssetID(assetId, parNum[0])
                        
 
                if parItems != []:
                    empListData = empListData + [(empDetails[0], parItems),]  

                    print("+++++++++++++++++++++++++++++++++++")
                    for xv in empListData:
                        print(xv)  

        pageDataOffices = pageDataOffices + [(offDetails , empListData),]
    
    return setReponse(request, templateFolder+'/equip_details.html', [assetDetails[0], itemType, itemDetails[0], partDetails[0],(invQty, invQtyAcct, invQtyWaste)], [], [], pageDataOffices, [])


def equiList(request):

    thePartCookie = getSessionData(request, 'thePartID')
    toPageData = []
    partDetails = equip.getEquiParticularDetails(thePartCookie)
    partItems = equip.getEquipmentByParticuar(thePartCookie)

    if partItems != []:
    
        for x in partItems:
            itemDetails = equip.getAssetDetails(x[0])

            toPageData = toPageData + [[itemDetails,],]

    return setReponse(request, templateFolder+'/equi_list.html', toPageData, [partDetails[0],], [], [], [])    

def itemDetails(request):

    itemNum = request.POST.get('itemDetails', '')

    itemDetails = itemC.getItemDetails(itemNum)

    return setReponse(request, templateFolder+'/item_details.html', itemDetails, [], [], [], [])

def supplyDetails(request, refData):

    refPO = refData.replace('_','-')
    
    pageDataOffices = []
    
    supply_Details = f.getCompleteSupplyDetails(refPO)
    offices = off.getAllOfficesSorted()

    for offid in offices:

        offDetails = off.getOfficeDetails(offid[0])
        pageDataOffices = pageDataOffices + [offDetails]

    offList = f.getAllOfficeComsuptionOfAnItem(refPO)   

    return setReponse(request, templateFolder+'/supply_details.html', supply_Details, [], [], offList, [])

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

    return setReponse(request, templateFolder+'/departments.html', [offDetails], completeDeptList, [], [], []) 

def generateIARDocument_Original(request):
    
    theCookieValue = getSessionData(request, 'iarCookie')

    iarDetails = ins.getIARDetails(theCookieValue)
    poDetails = pOrd.getPODetails(iarDetails[0][1])

    poItems = pOrd.getItemByPO(iarDetails[0][1]) 
    iarItems = ins.getIARItems(theCookieValue)
    suppName = suppl.getSupllierName(poDetails[0][1])

    prRef = preq.getReqNumFromPR(poDetails[0][13])
    prDetails = preq.getPRDetails(prRef[0][0])

    empDetails = e.getEmployeeDetails(prDetails[0][4])
    offDetails = off.getOfficeDetails(empDetails[0][4])

    insDetails = e.getEmployeeDetails(iarDetails[0][8])
    recDetails = e.getEmployeeDetails(iarDetails[0][11])

    insName = insDetails[0][6]+' '+insDetails[0][1]+' '+insDetails[0][7]+' '+insDetails[0][2]+' '+insDetails[0][8]
    recName = recDetails[0][6]+' '+recDetails[0][1]+' '+recDetails[0][7]+' '+recDetails[0][2]+' '+recDetails[0][8]

    loopRef = genLoopRangeString(20, poItems) 

    return renderPDF(request, 'pdf_templates/doc-iarTest2.html', iarDetails, poDetails, iarItems, [(suppName[0][0],offDetails[1], prDetails[0][2], insName, recName),], 'iar_'+theCookieValue, loopRef, 'legal')


def generateIARDocument(request):
    
    theCookieValue = getSessionData(request, 'iarCookie')

    iarDetails = ins.getIARDetails(theCookieValue)
    ponumref = iarDetails[0][2]

    poDate = 'n/a'

    prNumFromRef = preq.getPRNumforPONumForNew(ponumref)
   
    if prNumFromRef != []:
        prPOTimelineDetails = preq.getProCTimeLineDetails(prNumFromRef[0][0])
        poDate = prPOTimelineDetails[0][17]

    iarItems = ins.getIARItems(theCookieValue)
    
    iarItemstoPage = []
        
    for x in iarItems:
            
        descripString = str(x[3])
    
        if "$" in descripString :

            arr = descripString.split('$')
            
            iarItemstoPage = iarItemstoPage + [(x[0],x[1], x[2], arr[0], x[4],x[5],x[6]),]

            for y in range(1,len(arr)):
                iarItemstoPage = iarItemstoPage + [('','','','  • '+str(arr[y]),'','',''),]

        else:
            iarItemstoPage = iarItemstoPage + [x] 
    
    suppName = suppl.getSupllierName(iarDetails[0][7])
    #print(iarDetails)

    offName = ''
    purpose = 'Not a MSU-GSC ordered item'

    prRef = preq.getPRNumforPONumForNew(iarDetails[0][2])
    #print(prRef)

    if prRef != []:

        prDetails = preq.getPRDetails(prRef[0][0])

        empDetails = e.getEmployeeDetails(prDetails[0][4])
        offDetails = off.getOfficeDetails(empDetails[0][4])

        offName = offDetails[1]
        purpose = prDetails[0][2]

    insDetails = e.getEmployeeDetails(iarDetails[0][9])
    recDetails = e.getEmployeeDetails(iarDetails[0][11])

    insName = insDetails[0][6]+' '+insDetails[0][1]+' '+insDetails[0][7]+' '+insDetails[0][2]+' '+insDetails[0][8]
    recName = recDetails[0][6]+' '+recDetails[0][1]+' '+recDetails[0][7]+' '+recDetails[0][2]+' '+recDetails[0][8]

    loopRef = genLoopRangeString(20, iarItems) 

    return renderPDF(request, 'pdf_templates/doc-iarTest2.html', iarDetails, [], iarItemstoPage, [(suppName,offName, purpose, insName, recName, poDate),], 'iar_'+theCookieValue, loopRef, 'legal')

def generatePARDocument(request):

    theCookieValue = getSessionData(request, 'newPARCookie')

    parDetails = propAR.getPARDetails(theCookieValue)
    poDetails = pOrd.getPODetails(parDetails[0][6])
    parItems = propAR.getPARItems(theCookieValue)
    parItems = parItems + propAR.getPARItemsFromNoInvNum(theCookieValue)
    parTotal = propAR.getPARTotal(parItems)
    reqEmp = off.getOfficeHeadFromOffice('SMO')
    empDetails = e.getEmployeeDetails(reqEmp[0][0])
    recEmpDetails = e.getEmployeeDetails(parDetails[0][2])

    loopRef = genLoopRangeString(18, []) 

    return renderPDF(request, 'pdf_templates/doc-parTest.html', parDetails, parItems, [empDetails[0],recEmpDetails[0]], [], 'par_'+theCookieValue, loopRef, 'legal')    

def generateWMRDocument(request, refData):
    
    
    theCookieValue = refData.replace('_','-')

    wmrDetails = waste_Class.getWMRDetails(theCookieValue)
    wmrItems = waste_Class.getWMRItems(theCookieValue)

    parDetails = propAR.getPARDetails(wmrDetails[0][4])
    #iarDetails = ins.getIARDetails()

    toPageWMRItems = []

    for x in wmrItems:
        
        itemDetails = propAR.getInventoryItemByInvNum(x[1])
        descripString = itemDetails[2]
        if "$" in descripString:

            arr = descripString.split('$')
            
            toPageWMRItems = toPageWMRItems + [(itemDetails[0], itemDetails[1], arr[0], itemDetails[3],  itemDetails[4],itemDetails[5]),]

            for y in range(1,len(arr)):
                toPageWMRItems = toPageWMRItems + [('','','  • '+str(arr[y]),'','',''),]
            
        else:
            toPageWMRItems = toPageWMRItems + [itemDetails]

    
    
    reqEmp = off.getOfficeHeadFromOffice('SMO')
    appEmp = off.getOfficeHeadFromOffice('VCAF')

    reqEmpDetails = e.getEmployeeDetails(reqEmp[0][0])
    appEmpDetails = e.getEmployeeDetails(appEmp[0][0])
    insEmpDetails = e.getEmployeeDetails(wmrDetails[0][7])



    reqName = reqEmpDetails[0][6]+' '+reqEmpDetails[0][1]+' '+reqEmpDetails[0][7]+' '+reqEmpDetails[0][2]+' '+reqEmpDetails[0][8]
    appName = appEmpDetails[0][6]+' '+appEmpDetails[0][1]+' '+appEmpDetails[0][7]+' '+appEmpDetails[0][2]+' '+appEmpDetails[0][8]
    insName = insEmpDetails[0][6]+' '+insEmpDetails[0][1]+' '+insEmpDetails[0][7]+' '+insEmpDetails[0][2]+' '+insEmpDetails[0][8]

    loopRef = genLoopRangeString(10, wmrItems) 

    return renderPDF(request, 'pdf_templates/doc-wmrTest.html',wmrDetails, toPageWMRItems, [(reqName,reqEmpDetails[0][3]),(appName,appEmpDetails[0][3]),(insName,insEmpDetails[0][3])], [], 'wmr', loopRef, '')    


def generateOBRDocument(request, refData):
    
    return renderPDF(request, 'pdf_templates/doc-obrTest.html', [], [], [], [], 'wmr', '', 'Letter')    


def generateLDDocument(request, refData):
    
    refNum = refData.replace('_','-') 
    prnum = preq.getPRNumforPONumForNew(refNum)
    prPOTimelineDetails = preq.getProCTimeLineDetails(prnum[0][0])

    ldList = ldClass.getLiqDamageListFromPO(refNum)
    ldListToPage = []

    index = 1;
    
    for x in ldList:
        indexString = 'th'

        if index == 1:
            indexString = 'st'
        if index == 2:
            indexString = 'nd'
        if index == 3:
            indexString = 'rd'

        iarDetails = ins.getIARDetails(x[2]) 
        iarItems = ins.getIARItems(x[2])
        iarTotal = ins.getTotalIARCost(x[2])

        dateServed = prPOTimelineDetails[0][19]
        dateStart = datetime(dateServed.year, dateServed.month, dateServed.day)

        delDate = iarDetails[0][10]
        dateEnd = datetime(delDate.year, delDate.month, delDate.day)

        interv = genIntervalDays(dateStart, dateEnd)

        ldListToPage += [(str(index)+indexString,)+x+iarDetails[0]+(iarTotal, interv)]

        index += 1

    today = datetime.now()
    ldTotal = ldClass.getLiqDamageFromPO(refNum)

    return renderPDF(request, 'pdf_templates/doc-liquidating.html', [prPOTimelineDetails[0], (today, ldTotal[0][0])], ldListToPage, [], [], refNum+'_ld_Doc', '', 'Letter')    




#== Non-display functions with urls ============================================================================

def addNewItem(request):
    

    if request.method == 'POST':
        
        description = request.POST['description']
        partID = request.POST['part']
        #itemType = request.POST['type']
        itemClass = request.POST['class']
        unit = request.POST['unit']
        price = request.POST['price']
        
        itemC.addItem(description, '', itemClass, unit, price, partID)

    return HttpResponse('')

def addNewWMI(request):
    

    if request.method == 'POST':
        
        parRef = request.POST['parNum']
        requesterID = request.POST['insOff']
        inspectorID = request.POST['insOff2']
        wmrnum = request.POST['wmrnum']
        items = json.loads(request.POST.get('theItems'))

        reqNum = f.createWMR(requesterID, parRef, inspectorID, items, wmrnum)

    return HttpResponse(reqNum)

def addSupplyItem(request):
    
    if request.method == 'POST':
        
        description = request.POST['description']
        unit = request.POST['unit']
        unitcost = request.POST['price']
        quantity = request.POST['quantity']
        
        itemID = itemC.getItemNumfromDescription(description)

        if itemID == []:
            itemID = itemC.addItem(description, '', 'Supply', unit, unitcost, '')
        
        else:
            itemID = itemID[0][0]

        f.addItemToSupply('', description, unit, quantity, itemID, '')

    return HttpResponse('')

    
def updateItem(request):
    

    if request.method == 'POST':
        
        itemid = request.POST['itemid']
        description = request.POST['description']
        partID = request.POST['part']
        itemClass = request.POST['itemclass']
        unit = request.POST['unit']
        price = request.POST['price']
        
        f.updateItemData(itemid, description, itemClass, unit, price, partID)

    return HttpResponse('')

def getItemDetails(request):
    
    outputData = {}

    if request.method == 'POST':
        itemID = request.POST['itemID']
        itemDetails = itemC. getItemDetails(itemID)

        
        outputData = {  'descrip': itemDetails[0][1], 
                        'price' : itemDetails[0][5],
                        'unit':itemDetails[0][4],
                   }
                                  
    
    return HttpResponse(json.dumps(outputData), content_type="application/json")

def getPOItems(request):
    outputData = {}

    if request.method == 'POST':
        poNumRef = request.POST['poNum']
        poNum = pOrd.getPONumFromAppPONum(poNumRef)
        itemList = pOrd.getItemByPO(poNum)

        
        counter = 1
        for x in itemList:
            
            outputData[str(counter)] = {'itemnum': x[1],
                                        'decrip': x[4], 
                                        'quantity': x[2],
                                        'price' : x[5],
                                        'unit':x[3],
                                        }
            counter = counter + 1                           
    
    return HttpResponse(json.dumps(outputData), content_type="application/json")


def getPODetails(request):
   
    outputData = {}

    if request.method == 'POST':
        poNumRef = request.POST['poNum']
        poNum = pOrd.getPONumFromAppPONum(poNumRef)
        poDetails = pOrd.getPODetails(poNum)
        
        poQuantity = pOrd.getPOItemsQuantity(poNum)
        poItems = pOrd.getItemByPO(poNum)
        poAllQuantity = pOrd.getTotalNumOfItemsofPO(poItems)

        
        outputData = {  'supp': suppl.getSupllierName(poDetails[0][1]),
                        'amount': poDetails[0][8], 
                        'quantity': poQuantity[0][0],
                        'totalNumofItems': poAllQuantity,
                        'delTerm': str(poDetails[0][6]),
                        'dateServed': str(poDetails[0][17]),
                        'expDateofDel': str(poDetails[0][4]),
                     }
        print('//----------------------------------------')
        print(outputData)                              
    
    return HttpResponse(json.dumps(outputData), content_type="application/json")

def getPOFromTimeLineDetails(request):
   
    outputData = {}

    if request.method == 'POST':
        poNumRef = request.POST['poNum']

        prReF =  preq.getPRNumforPONumForNew(poNumRef)
        prPOTimelineDetails = preq.getProCTimeLineDetails(prReF[0][0])

        outputData = {  'supp': prPOTimelineDetails[0][18],
                        'expdate': str(prPOTimelineDetails[0][20]), 
                        'podate': str(prPOTimelineDetails[0][17]),
                     }
                                
    
    return HttpResponse(json.dumps(outputData), content_type="application/json")    


def receiveItems(request):
    
    outputData = {}
    poDetails = None
    
    if request.method == 'POST':

        itemList = json.loads(request.POST.get('theArray'))
        
        iarnum = request.POST['iarnum']
        ponum = request.POST['poNum']
        expdate = request.POST['expdate']
        asses = request.POST['asses']
        invnum = request.POST['invNum']
        recDate = request.POST['recDate']
        supplier = request.POST['supplier']
        insOff = request.POST['insOff']
        insdate = request.POST['insdate']
        receiveoff = request.POST['receiveoff']
        receivedate = request.POST['receivedate']
        compltstatus = request.POST['compltstatus']
        rectype = request.POST['rectype']

        

        f.addReceive2(iarnum, ponum, expdate, asses, invnum, recDate, supplier, receivedate, receiveoff, insdate, insOff, compltstatus, itemList, rectype)

        setSessionData(request, 'iarCookie', iarnum)

    return HttpResponse('')

def getAvailableItems(request):
    
    outputData = {}

    if request.method == 'POST':
        iarNum = request.POST['iarNum']
        
        itemList = ins.getAvailableItems(iarNum)
        counter = 1
        
        for x in itemList:
            
            outputData[str(counter)] = {'itemnum': x[5],
                                        'descrip': x[2], 
                                        'unitprice': x[4],
                                        'quantity': x[3],
                                        }
            counter = counter + 1                           
    
    return HttpResponse(json.dumps(outputData), content_type="application/json")

def getAvailableItemsbyPO(request):
    
    outputData = {}

    if request.method == 'POST':
        ponum = request.POST['ponum']
        
        print(ponum)

        
        iarList = ins.getAllIARNumFromRef(ponum)

        print("-- IAR List")
        print(iarList)

        counter = 1
        
        for xy in iarList:
            itemList = ins.getAvailableItems(xy[0])
            
            for x in itemList:
                
                outputData[str(counter)] = {'itemnum': x[5],
                                            'descrip': x[2], 
                                            'unitprice': x[4],
                                            'quantity': x[3],
                                            'iarnum': xy[0],
                                            }
                counter = counter + 1                           
    
    return HttpResponse(json.dumps(outputData), content_type="application/json")




def addEquiparticular(request):
   
    if request.method == 'POST':
        idname = request.POST['idname']
        name = request.POST['name']
        #subhead = request.POST['subhead']
        itemnum = request.POST['itemnum']

        equip.addEquiParticular(idname, name, '', itemnum)
        

    return HttpResponse()


def getPARItems(request):
    
    outputData = {}

    if request.method == 'POST':
        theCookieValue = request.POST['parNum']
        print('//-------------------->>>>>>>>>>>>>>>')
        print(theCookieValue)

        parItems = propAR.getPARItems(theCookieValue)
        
        print('//-------------------->>>>>>>>>>>>>>>')
        print(parItems)
        
        parTotal = propAR.getPARTotal(parItems)
        
        print('//-------------------->>>>>>>>>>>>>>>')
        print(parTotal)

        parItemJSON = f.getPARListItemsForJSON(theCookieValue)
        outputData = parItemJSON

        '''
        counter = 1
        
        for x in parItems:
            
            outputData[str(counter)] = {'invNum': x[0],
                                        'descrip': x[2],
                                        'unit': x[3], 
                                        'unitprice': x[4],
                                        'quantity': x[5],
                                        'total': x[8],
                                        }
            counter = counter + 1                           
        '''
    return HttpResponse(json.dumps(outputData), content_type="application/json")

def tranferPAR(request):
    
    if request.method == 'POST':    
        
        parnum = request.POST['parNum']
        offid = request.POST['offid']

        f.updateTranferPAR(parnum, offid)

    return HttpResponse()   

def updateItemAssetID(request):

    if request.method == 'POST':

        iarnum = request.POST['iarNum']
        itemnum = request.POST['itemnum']
        
        brand = request.POST['brand']
        model = request.POST['model']
        #iarDetails = ins.getIARDetails(iarnum)
        assetId = None
        assetID = equip.getAssetIDFromBrandAndModel(brand, model)

        itemId = ins.getItemIDFromInput(iarnum, itemnum)

        if assetID == []:
            assetId = equip.addEquipment(itemId, model, brand, '', '', '', 'NULL')

        else:
            assetId = assetID[0][0]

        ins.updateItemAssetID(iarnum, itemnum, assetId)
        #setSessionData(request, 'newPARCookie', parnum)

    return HttpResponse('')


def addToAcct(request):

    theCookieValue = getSessionData(request, 'theCookie')
    logDetails = l.getLogDetails(theCookieValue)

    if request.method == 'POST':

        itemList = json.loads(request.POST.get('toPARItems'))
        
        iarnum = request.POST['iarNum']
        byid = request.POST['byid']
        parnum = request.POST['parNum']
        recDate = request.POST['recDate']
        relDate = request.POST['relDate']
        iarDetails = ins.getIARDetails(iarnum)

        f.addPAR(parnum, byid, recDate, logDetails[0][1], relDate, iarDetails[0][2], iarnum, itemList)
        setSessionData(request, 'newPARCookie', parnum)

    return HttpResponse('')

def approveRIS(request):

    if request.method == 'POST':
        
        appQtyList = json.loads(request.POST.get('theMatrix'))
        slipnum = request.POST['slipnum']

        f.approveRIS(slipnum, appQtyList)

    return HttpResponse('')

def decideRIS(request):

    if request.method == 'POST':
        pass
        
    
    return HttpResponse('')

def releaseRIS(request):

    if request.method == 'POST':
        
        slipnum = request.POST['slipnum']
        recOfficer = request.POST['receiverID']
        
        f.realeaseRIS(slipnum, recOfficer)

    return HttpResponse('')

def updateSerial(request):
    
    if request.method == 'POST':
        
        invnum = request.POST['invnum']
        inputData = request.POST['inputData']
        
        propAR.updateSerialID(invnum, inputData)

    return HttpResponse('')

def acctdetails(request):
    
    reponse = None
    offID = request.POST.get('offDetails', '')

    offDetails = off.getOfficeDetails(offID)
    if offDetails[2] == 'college':
        
        reponse = HttpResponseRedirect(urlHead+'/account/departments')
        setSessionData(request, 'theDeptID', offID)
    
    else:
        reponse = HttpResponseRedirect(urlHead+'/account/item_list')
        setSessionData(request, 'theOffID', offID)  

    return reponse

def displayItemOfParticular(request):

    partID = request.POST.get('partIDButton', '')
    setSessionData(request, 'thePartID', partID)

    return HttpResponseRedirect(urlHead+'/equipment/list/')  

def displayEquipDetails(request):

    partID = request.POST.get('equiIDButton', '')
    setSessionData(request, 'theEquiID', partID)

    return HttpResponseRedirect(urlHead+'/equipment/details/')    

def displayRISDetails(request):
    
    slipnum = request.POST.get('slipNumButton', '')
    setSessionData(request, 'theSlipNum', slipnum)
    
    return HttpResponseRedirect(urlHead+'/ris/details/') 

#= Non-display functions =======================================================================================

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

        accessType = acctType[0]

        baseSource = {
                        3:['inventory_office/base_admin.html','active-menu-inven'],
                        30:['inventory_office/base.html','active-menu-inven'],
                        31:['inventory_office/base_inven.html','active-menu-inven-inv'],
                        32:['inventory_office/base_acct.html','active-menu-inven-acct'],
                        33:['inventory_office/base_rec.html','active-menu-inven-rec'],
                        34:['inventory_office/base_supp.html','active-menu-inven-supp'],

        }

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
            'baseSource': (baseSource[accessType])[0],
            'urlHead': urlHead,
            'cssActiveMenu' : (baseSource[accessType])[1],
        
        }

        

        if accessType == 3 or accessType == 30 or accessType == 31 or accessType == 32 or accessType == 33 or accessType == 34:
            
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

def genIntervalDays(inputDate1, inputDate2):
    
    output = []

    numDays = 0
    startDate = 0
    endDate = 0

    dateDict = {
                1:('January',31),
                2:('February',28),
                3:('March',31),
                4:('April',30),
                5:('May',31),
                6:('June',30),
                7:('July',31),
                8:('August',31),
                9:('September',30),
                10:('October',31),
                11:('November',30),
                12:('December',31),
    }

    dateMonth1 = inputDate1.month
    dateDay1 = inputDate1.day
    dateYear1 = inputDate1.year

    dateMonth2 = inputDate2.month
    dateDay2 = inputDate2.day
    dateYear2 = inputDate2.year

    if dateMonth1 == dateMonth2:

        dateData = dateDict[dateMonth1]

        numDays = dateDay2 - dateDay1
        startDate = dateDay1
        endDate = dateDay2 
    
        output += [(dateData[0], '('+str(startDate)+'-'+str(endDate)+')', inputDate1.year, numDays),]
    
    else:

        if dateYear1 == dateYear2:
            
            for x in range(dateMonth1, dateMonth2+1):
                
                dateData = dateDict[x]
                
                
                if x == dateMonth1 or x == dateMonth2:
                    if x == dateMonth1:
                        numDays = dateData[1] - dateDay1
                        startDate = dateDay1
                        endDate = dateData[1]
                    else:
                        numDays = dateDay2
                        startDate = 1 
                        endDate = dateDay2   
                     
                else:
                    numDays = dateData[1]
                    startDate = 1  
                    endDate = dateData[1]
                
                output += [(dateData[0], '('+str(startDate)+'-'+str(endDate)+')', inputDate1.year ,numDays),]
        else:
            for x in range(dateYear1, dateYear2+1):
                
                if x == dateYear1 or x == dateYear2:
                    
                    if x == dateYear1:

                        if dateMonth1 == 12:

                                    dateData = dateDict[12]
                                    numDays = 31 - dateDay1
                                    startDate = dateDay1
                                    endDate = 31
                                
                                    output += [(dateData[0], '('+str(startDate)+'-'+str(endDate)+')', inputDate1.year, numDays),]
                        
                        else:
                            for y in range(dateMonth1, 13):
                                            
                                            dateData = dateDict[x]
                                            
                                            
                                            if x == dateMonth1 or x == dateMonth2:
                                                if x == dateMonth1:
                                                    numDays = dateData[1] - dateDay1
                                                    startDate = dateDay1
                                                    endDate = dateData[1]
                                                else:
                                                    numDays = dateDay2
                                                    startDate = 1 
                                                    endDate = dateDay2   
                                                 
                                            else:
                                                numDays = dateData[1]
                                                startDate = 1  
                                                endDate = dateData[1]
                                            
                                            output += [(dateData[0], '('+str(startDate)+'-'+str(endDate)+')', x ,numDays),]
                    else:
                        
                        if dateMonth2 == 1:

                                    dateData = dateDict[1]
                                    numDays = dateDay2
                                    startDate = 1
                                    endDate = dateDay2
                                
                                    output += [(dateData[0], '('+str(startDate)+'-'+str(endDate)+')', x, numDays),]
                        
                        else:
                            for y in range(1, dateMonth2+1):
                                            
                                            dateData = dateDict[y]
                                            
                                            
                                            if y == dateMonth1 or y == dateMonth2:
                                                if x == dateMonth1:
                                                    numDays = dateData[1] - dateDay1
                                                    startDate = dateDay1
                                                    endDate = dateData[1]
                                                else:
                                                    numDays = dateDay2
                                                    startDate = 1 
                                                    endDate = dateDay2   
                                                 
                                            else:
                                                numDays = dateData[1]
                                                startDate = 1  
                                                endDate = dateData[1]
                                            
                                            output += [(dateData[0], '('+str(startDate)+'-'+str(endDate)+')', x ,numDays),]
                                

    return output

if __name__ == '__main__':
    
    date1 = datetime(2018,1,2)
    date2 = datetime(2018,5,15)

    print(genIntervalDays(date1, date2))