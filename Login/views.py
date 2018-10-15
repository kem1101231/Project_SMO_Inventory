from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.template import RequestContext
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import HttpResponse
from os.path import dirname, abspath
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


def index(request):
    
    reponse = None

    if f.user.checkAdminUser() == False:
      response = render(request,'login/create_admin.html', None)
    
    else:
      uname = request.POST.get('unmField', '')
      password = request.POST.get('passField', '')
      
      outstring = None
      
      userdata = None
      employeeData = None
      logid = None

      notifNum = None
      taskNum = None
      tasks = None
      notifs = None

      eFname = ''
      eSname = ''
      designation = ''
      dept = ''
      cookieValue = ''
      error = ''

      
      if idSessionValueEmpty(request, 'theCookie'):
        
        if uname == "":
          outstring = 'login/login.html'
      
        else:
        
          output = f.checkLogin(uname, password)
        
          if output == "username does not exist":
                outstring = 'login/login.html'
                error = 'username'
          
          if output == "wrong password":
                outstring = 'login/login.html'
                error = 'password'
          
          if output == "disabled":
                outstring = 'login/login.html'
                error = 'disabled'
          
          if output == "login complete":
              
            userdata = u.getUserDetails(uname)
            acctype = userdata[0][3]
            logid = l.addLog(userdata[0][2])
            cookieValue = logid

            taskNum = n.getTaskNum(userdata[0][2]) 
            notifNum = n.getNotifNum(userdata[0][2])
            notifs = setNotifDetails(userdata[0][2])
            tasks = setTaskDetails(userdata[0][2])
            employeeData = e.getEmployeeDetails(userdata[0][2])


            eFname = employeeData[0][1]
            eSname = employeeData[0][2]
            designation = employeeData[0][3]
            dept = employeeData[0][4]

            
            outstring = getOutStringValue(userdata[0][3])

            chancellor = kp.getChancellor()
            vcaf = kp.getVCAF()

            pendingInitPRs = preq.getAllInitPendingPR()
            pendingPRs = preq.getAllPendingPR()
            
            toPageData = None
            usertype = ''
            
            if userdata[0][2] == vcaf and vcaf != None:
              toPageData = len(pendingInitPRs)
              usertype = 'vcaf'
            
            if userdata[0][2] == chancellor and chancellor != None:
              toPageData = len(pendingPRs)
              usertype = 'chancellor'

            

      else:

        theCookieValue = getSessionData(request, 'theCookie')

        logDetails = l.getLogDetails(theCookieValue)
        unameData = u.getUnameFromID(logDetails[0][1]) 
        userdata = u.getUserDetails(unameData[0][0])
        
        taskNum = n.getTaskNum(userdata[0][2]) 
        notifNum = n.getNotifNum(userdata[0][2])
        notifs = setNotifDetails(userdata[0][2])
        tasks = setTaskDetails(userdata[0][2])
        employeeData = e.getEmployeeDetails(userdata[0][2])
        cookieValue = logDetails[0][0]
        
        outstring = getOutStringValue(userdata[0][3])
        
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
        

      
      if outstring != 'login/login.html':

          link = getOutLinkValue(userdata[0][3])

          setSessionData(request, 'theCookie', cookieValue)
          
          response = HttpResponseRedirect(link)
          
      
      else:
        c = {

          'error': error,
          'uname': uname,
            }


        c.update(csrf(request))
        
        response = render(request, outstring, c)
      
      
    return response


def login(request):

  reponse = HttpResponseRedirect('/')
  del request.session['theCookie']

  return reponse

def create_acct(request):

  offList = off.getAllOfficesSorted()
  offListToPage = []


  for x in offList:
      offDetails = off.getOfficeDetails(x[0])
      offListToPage = offListToPage + [offDetails, ]


  datatoPage = {'pageData1': offListToPage,

  }

  response = render(request, 'login/create_acct.html', datatoPage)

  return response  

def createAcct(request):

  response = None 
  
  if request.method == 'POST':
    
    idnum = request.POST['idnum']
    uname = request.POST['uname']
    password = request.POST['pass1']
    idExist = request.POST['idExist']
    lname = request.POST['lname']
    fname = request.POST['fname']
    mini = request.POST['mini']
    #rank = request.POST['rank']
    #desig = request.POST['desig']
    office = request.POST['office']
    

    print("id :"+str(idExist))

    acctType = f.createUser(uname, password, idnum, idExist, lname, fname, mini, '', '', office)

    logid = l.addLog(idnum)
    cookieValue = logid
    setSessionData(request, 'theCookie', cookieValue)
  
  return HttpResponse(str(acctType))

def create_admin(request):
  
  if request.method == 'POST':

    uname = request.POST['uname']
    passw = request.POST['passw']

    f.emp.addEmployee('0000-0001', 'System', 'Administrator', 'System Administrator', '', '', '', '', '')
    f.user.addUser(uname, passw, '0000-0001', '0')
    f.user.updateUserStatus(uname, 'TRUE')

    return HttpResponse('')

def chckUname(request):
  
  uname ='' 
  outMsg = ''
  
  if request.method == 'POST':
    
      uname = request.POST['uname']


  if u.isUserRegistered(uname) == False:    
     outMsg = 'True'

  else:
      outMsg = 'False'


  return HttpResponse(outMsg)  


def chckIdnum(request):
  
  idnum ='' 
  outMsg = ''
  
  if request.method == 'POST':
    
      idnum = request.POST['uname']



  if e.isUserRegistered(idnum) == False:    
     outMsg = 'non-existing'

  else:

    if u.isIDRegistered(idnum) == True:
      outMsg = 'acct-existing'
    else:
      outMsg = 'True'
    
  return HttpResponse(outMsg)  

def getUserAccessType(request):

  response = ''
  uname = ''
  if request.method == 'POST':
      uname = request.POST['uname']
  unameData = u.getUserDetails(uname)
  
  accsType = unameData[0][3]

  response = HttpResponse(json.dumps({'accsType':accsType}), content_type="application/json")  

  return response


def chckPass(request):

  response = ''
  password = ''
  uname = ''
  
  if request.method == 'POST':
      uname = request.POST['uname']
      password = request.POST['password']
  


  passchck = u.checkUserPass(uname, password)

  response = HttpResponse(json.dumps({'passChckReturn':str(passchck)}), content_type="application/json")  

  return response

def getEmpDetails(request):
    
    idnum = ''

    if request.method == 'POST':
      idnum = request.POST['idnum']

    empDetails = e.getEmployeeDetails(idnum)
    offDetails = off.getOfficeDetails(empDetails[0][4])

    output = {
              'name': empDetails[0][6]+";"+empDetails[0][1]+";"+empDetails[0][7]+";"+empDetails[0][2]+";"+empDetails[0][8],
              'rank':empDetails[0][5],
              'desig': empDetails[0][3],
              'office':offDetails[1]+";"+offDetails[0],

    }
    
    response = HttpResponse(json.dumps(output), content_type="application/json")  

    return response

#==================================================================================================================

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

    return False
  else:

    return True 

def getCookieValue(request, key):
  
  value = request.COOKIES[key]
  return value

def getOutStringValue(input):
  
  out = ''
  
  if input == [33]:
     out = 'inventory_office_rec_off/home.html'

  if input == [31]:
     out = 'inventory_office_inv_clerk/home.html'

  if input == [5]:
     out = 'non_requisitioner/index.html'

  if input == [32]:
     out = 'inventory_office_acct_mgr/home.html'

  if input == [4]:
     out = 'requisitioner/index.html'
                
  if input == [3]:
     out =  'inventory_office/home.html'
                
  if input == [2]:
     out =  'procurement/index.html' 
                  
  if input == [1]:
     out =  'approving_office/index.html'

  if input == [0]:
     out =  'super_user/home.html'

  return out 

def getOutLinkValue(input):
  
  out = ''

  if input == [33]:
     out = '/inventory_office/'

  if input == [31]:
     out = '/inventory_office/'

  if input == [5]:
     out = '/non_requisitioner/'

  if input == [32]:
     out = '/inventory_office/'

  if input == [4]:
     out = '/requisitioner/'
                
  if input == [3]:
     out =  '/inventory_office/'
                
  if input == [2]:
     out =  '/procurement_office/' 
                  
  if input == [1]:
     out =  '/approving_officer/'

  if input == [12]:
     out =  '/approving_officer_representative'
   
  if input == [6]:
     out =  '/accounting/'
  
  if input == [30]:
     out =  '/inventory_office/'
  
  if input == [34]:
     out =  '/inventory_office/'
  
  if input == [0]:
     out =  '/system_admin/'   
   

  return out    


'''
def getOutLinkValue(input):
  
  out = ''

  if input == [33]:
     out = '/inventory_office_rec_off/'

  if input == [31]:
     out = '/inventory_office_inv_clerk/'

  if input == [5]:
     out = '/non_requisitioner/'

  if input == [32]:
     out = '/inventory_office_acct_mgr/'

  if input == [4]:
     out = '/requisitioner/'
                
  if input == [3]:
     out =  '/inventory_office_admin/'
                
  if input == [2]:
     out =  '/procurement_office/' 
                  
  if input == [1]:
     out =  '/approving_officer/'

  if input == [12]:
     out =  '/approving_officer_representative'
   
  if input == [6]:
     out =  '/accounting/'
  
  if input == [30]:
     out =  '/inventory_office/'
  
  if input == [34]:
     out =  '/inventory_office_sup_off/'
  
  if input == [0]:
     out =  '/system_admin/'   
   

  return out    

'''
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

