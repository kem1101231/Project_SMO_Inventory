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
from inspect_accept_report import InsepectionAndAcceptanceReceipt
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


f = Functions()
u = User()
l = Log()
e = Employees()
n = Notification()
ins = InsepectionAndAcceptanceReceipt()
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


def index(request):
	
	return setReponse(request, 'accounting/index.html', [], [], [], [], [])

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
        
        }

        if any( 6 == code for code in acctType):
            
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
          
            ll = ll + (kk[0][2],kk[0][3],kk[0][4],notifTimeDate[0][0], notifTimeDate[0][1],kk[0][11]) 
          
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
          
            ll = ll + (kk[0][2],kk[0][3],kk[0][4],notifTimeDate[0][0], notifTimeDate[0][1],kk[0][11]) 
          
            outputList = outputList + [ll]

        return outputList

def genLoopRangeString(maxRange, refList):
    
    output = ''
    maxInRange = maxRange - len(refList)
    
    for x in range(2, maxInRange):
        output = output + 'x'

    return output   
