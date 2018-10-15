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

templateFolder = 'inventory_office'
urlHead = '/inventory_office_rec_off'

def index(request):
    return setReponse(request, templateFolder+'/home_new_again.html', [], [], [], [], [('inventory_office/base.html',),])

def search(request):


    theCookieValue = getSessionData(request, 'theCookie')
    logDetails = l.getLogDetails(theCookieValue)

    reference = request.POST.get('search_input','')

    result = f.findInfo(reference)

    return setReponse(request, templateFolder+'/search.html', result, [], [], [], [])
    

def searchRedirectDetails(request, refData, refType):
    
    return HttpResponse(refData)

def addAcct(request):

    parNum = propAR.generateRecNum()

    return setReponse(request, templateFolder+'/add-acct.html', [(parNum,),], [], [], [], [])

def acct(request):

    pageData = []

    colleges = off.getColleges()
    academics = off.getAcademics()
    administratives = off.getAdministratives()

    offices = off.getAllOfficesSorted()

    for offid in offices:

        offDetails = off.getOfficeDetails(offid[0])
        pageData = pageData + [offDetails]

    return setReponse(request, templateFolder+'/all_par.html', pageData, [], [], [], [])

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

        offDetails = off.getOfficeDetails(offid[0])
        pageData = pageData + [offDetails]
    
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

def offDetails(request):
    return setReponse(request, templateFolder+'/off_details.html', [], [], [], [], [])

def createWMR(request):

    return setReponse(request, templateFolder+'/create_wmr.html', [], [], [], [], [])

def wmrDetails(request, refData):

    return setReponse(request, templateFolder+'/wmr_details.html', [], [], [], [], [])

def prDetails(request, refData):

    return setReponse(request, templateFolder+'/pr_details.html', [], [], [], [], [])

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

def displayPODetails(request, refData):

    refPO = refData.replace('_', '-')

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

    return setReponse(request, templateFolder+'/po_details_new.html',[poDetails[0]+(poTotal,),prDetails[0]+(str(poDetails[0][13]).replace('-','_'), delDate), empDetails[0], (offDetails[1],), suppDetails[0], iarDetails, (quoNum, quoNumRef)], poItems, [], [], [])

def empDetails(request):

    return setReponse(request, templateFolder+'/emp_details.html', [], [], [], [], [])

def supplyDetails(request, refData):

    refPO = refData.replace('_', '-')
       
    return setReponse(request, templateFolder+'/supply_details.html', [], [], [], [], [])

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

    allPRnum = preq.getAllApprovedPR()

    for x in allPRnum:
        prDetails = preq.getPRDetails(x[0])
        empDetails = e.getEmployeeDetails(prDetails[0][4])
        offDetails = off.getOfficeDetails(empDetails[0][4])

        toPageData = toPageData + [prDetails[0]+empDetails[0]+(prDetails[0][1].replace('-','_'),offDetails[1]),]


    return setReponse(request, templateFolder+'/all_pr.html', toPageData, [], [], [], [])   

def poList(request):

    toPageData = [] 

    poList = pord.getAllApprovedPO()

    for x in poList:
        suppDetails = suppl.getSupllierDetails(x[1])
        toPageData = toPageData + [x + suppDetails[0]+ (x[0].replace('-','_'),),]
    
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

    return setReponse(request, templateFolder+'/add-receive-new-v3.html', [(iarnum, ),], [], [], [], [])

def addReceiveNew(request):

    iarnum = ins.generateReqNum()

    return setReponse(request, templateFolder+'/add-receive-new.html', [(iarnum, ),], [], [], [], [])

def addReceiveNewer(request):

    iarnum = ins.generateReqNum()

    return setReponse(request, templateFolder+'/add-receive-new-v4.html', [(iarnum, ),], [], [], [], [])



def itemList(request):
    
    itemlist = itemC.getAllItemsWithDetails()

    return setReponse(request, templateFolder+'/item_list.html', itemlist, [], [], [], [])

def iarDisplayDetails(request):
    return setReponse(request, templateFolder+'/iar_details.html', [], [], [], [], [])

def equi(request):

    totalQty = equip.getAllEquipmentQty()
    totalCost = equip.getAllEquipmentCost()
    totalOnAcct = equip.getAllEquipmentQtyonAcct()
    totalOnWaste = equip.getAllEquipmentQtyonWaste()
    
    particulars = equip.getAllEquiParticularswithDetails()

    itemlist = itemC.getAllEquipmentItemsWithDetails()

    return setReponse(request, templateFolder+'/equi-part.html', particulars, [(totalQty, totalCost, totalOnAcct, totalOnWaste),], itemlist, [], [])

def inven(request):

    itemsSorted = itemC.getAllSupplyItemsSortedwithDetails()
    inventoryData = supplyC.getSupplyInventory()
    
    return setReponse(request, templateFolder+'/inventory.html', itemsSorted, inventoryData, [], [], [])    

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
                        
                dataToPage = dataToPage + [('iar', iarNum, iarDetails[0][10], delStat, compStat, iarNum.replace('-','_')),]
        '''
        else:
                dataToPage = dataToPage + [('po', x[0], 'None', x[0].replace('-','_')),]
                dataToPage = dataToPage + [('iar', None),]
        '''
    return setReponse(request, templateFolder+'/receive.html', dataToPage, [], [], [], [])

def iarDisplayDetailsFromRef(request, refData):


    return setReponse(request, templateFolder+'/iar_details.html', [], [], [], [], [])

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

def equiList(request):

    thePartCookie = getSessionData(request, 'thePartID')
    toPageData = []
    partDetails = equip.getEquiParticularDetails(thePartCookie)
    partItems = equip.getEquipmentByParticuar(thePartCookie)

    if partItems != []:
    
        for x in partItems:
            itemDetails = equip.getAssetDetails(x[0])

            toPageData = toPageData + itemDetails

    return setReponse(request, templateFolder+'/equi_list.html', toPageData, [partDetails[0],], [], [], [])    

def itemDetails(request):

    itemNum = request.POST.get('itemDetails', '')

    itemDetails = itemC.getItemDetails(itemNum)

    return setReponse(request, templateFolder+'/item_details.html', itemDetails, [], [], [], [])

def supplyDetails(request, refData):

    pageDataOffices = []
    offices = off.getAllOfficesSorted()

    for offid in offices:

        offDetails = off.getOfficeDetails(offid[0])
        pageDataOffices = pageDataOffices + [offDetails]

    return setReponse(request, templateFolder+'/supply_details.html', itemDetails, [], [], pageDataOffices, [])

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

def generateIARDocument(request):
    
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

def generatePARDocument(request):

    theCookieValue = getSessionData(request, 'newPARCookie')

    parDetails = propAR.getPARDetails(theCookieValue)
    poDetails = pOrd.getPODetails(parDetails[0][6])
    parItems = propAR.getPARItems(theCookieValue)
    parTotal = propAR.getPARTotal(parItems)
    empDetails = e.getEmployeeDetails(parDetails[0][4])
    recEmpDetails = e.getEmployeeDetails(parDetails[0][2])

    loopRef = genLoopRangeString(18, []) 

    return renderPDF(request, 'pdf_templates/doc-parTest.html', parDetails, parItems, [empDetails[0],recEmpDetails[0]], [], 'par_'+theCookieValue, loopRef, 'legal')    

def generateWMRDocument(request, refData):
    
    
    theCookieValue = refData.replace('_','-')

    wmrDetails = waste_Class.getWMRDetails(theCookieValue)
    wmrItems = waste_Class.getWMRItems(theCookieValue)

    toPageWMRItems = []

    for x in wmrItems:
        
        itemDetails = propAR.getInventoryItemByInvNum(x[1])
        toPageWMRItems = toPageWMRItems + [itemDetails]

    
    reqEmp = off.getOfficeHeadFromOffice('SMO')
    appEmp = off.getOfficeHeadFromOffice('VCAF')

    reqEmpDetails = e.getEmployeeDetails(reqEmp[0][0])
    appEmpDetails = e.getEmployeeDetails(appEmp[0][0])
    insEmpDetails = e.getEmployeeDetails(wmrDetails[0][7])



    reqName = reqEmpDetails[0][6]+' '+reqEmpDetails[0][1]+' '+reqEmpDetails[0][7]+' '+reqEmpDetails[0][2]+' '+reqEmpDetails[0][8]
    appName = appEmpDetails[0][6]+' '+appEmpDetails[0][1]+' '+appEmpDetails[0][7]+' '+appEmpDetails[0][2]+' '+appEmpDetails[0][8]
    insName = insEmpDetails[0][6]+' '+insEmpDetails[0][1]+' '+insEmpDetails[0][7]+' '+insEmpDetails[0][2]+' '+insEmpDetails[0][8]

    loopRef = genLoopRangeString(14, wmrItems) 

    return renderPDF(request, 'pdf_templates/doc-wmrTest.html',wmrDetails, toPageWMRItems, [(reqName,reqEmpDetails[0][3]),(appName,appEmpDetails[0][3]),(insName,insEmpDetails[0][3])], [], 'wmr', loopRef, '')    


def generateOBRDocument(request, refData):
    
    return renderPDF(request, 'pdf_templates/doc-obrTest.html', [], [], [], [], 'wmr', '', 'Letter')    




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
        items = json.loads(request.POST.get('theItems'))

        reqNum = f.createWMR(requesterID, parRef, inspectorID, items)

    return HttpResponse(reqNum)
    
    
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
                     }
        print('//----------------------------------------')
        print(outputData)                              
    
    return HttpResponse(json.dumps(outputData), content_type="application/json")
    
def receiveItems(request):
    
    outputData = {}
    poDetails = None
    if request.method == 'POST':

        itemList = json.loads(request.POST.get('theArray'))
        compStat = json.loads(request.POST.get('compArray'))
        
        iarnum = request.POST['iarnum']
        poNumRef = request.POST['poNum']
        poNum = pOrd.getPONumFromAppPONum(poNumRef)
        invNum = request.POST['invNum']
        recDate = request.POST['recDate']
        insOff = request.POST['insOff']
        insdate = request.POST['insdate']
        receiveoff = request.POST['receiveoff']
        receivedate = request.POST['receivedate']

        print(poNum)

        if itemList != {}:
            pass
        
        else:
            poDetails = pOrd.getPODetails(poNum)
            reqnum = preq.getReqNumFromPR(poDetails[0][13])
            prDetails = preq.getPRDetails(reqnum[0][0])
        


        f.addReceive(iarnum, poNum, poDetails[0][2], prDetails[0][4], invNum, recDate, insdate, insOff, receivedate, receiveoff, itemList, compStat)

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
    
    return HttpResponse(json.dumps(outputData), content_type="application/json")

def addToAcct(request):

    theCookieValue = getSessionData(request, 'theCookie')
    logDetails = l.getLogDetails(theCookieValue)

    if request.method == 'POST':

        itemList = json.loads(request.POST.get('toPARItems'))
        
        iarnum = request.POST['iarNum']
        byid = request.POST['byid']
        parnum = request.POST['parNum']
        iarDetails = ins.getIARDetails(iarnum)

        f.addPAR(parnum, byid, '', logDetails[0][1], '', iarDetails[0][1], iarnum, itemList)
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
            'baseSource': 'inventory_office_rec_off/base.html',
            'urlHead': urlHead,
            'cssActiveMenu' : 'active-menu-inven-rec',
        
        }

        if any( 33 == code for code in acctType):
            
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
