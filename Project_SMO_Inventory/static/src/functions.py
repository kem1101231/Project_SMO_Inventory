#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$11 3, 16 2:54:38 PM$"

from weasyprint import HTML, CSS

import random
import string
from random import randint
from datetime import datetime
import re

from datetime import date, timedelta


from connectdb import ConnectDB
from user import User
from purchase_request import PurchaseRequest
from notifications import Notification
from employees import Employees
from key_positions import KeyPositions
from request_for_quotation import RequestForQuotation
from abstract_of_canvass import AbstractOfCanvass
from suppliers import Suppliers
from purchase_order import PurchaseOrder
from inspect_accept_report import InsepectionAndAcceptanceReceipt
from inspect_accept_report_2 import InsepectionAndAcceptanceReceipt_2
from property_acc_receipt import PropertyAcceptanceReceipt
from office import Offices
from items import Items
from equipment import Equipment
from requisition_issuance_slip import RequisitionAndIssuanceSlip
from supply import Supply
from waste import Waste 
from workAddSub import WorkAddSub
from liquidating_damages import LiquidatingDamages
from tasks import Tasks


c = ConnectDB()
connection = c.connection()
cur = connection.cursor()

print("Initializing .......")

class Functions:

		user = None
		pr = None
		notif = None
		emp = None
		kp = None
		reqQ = None
		abc = None
		sup = None
		po = None
		ins = None
		ins_2 = None
		propAcc = None
		offc = None
		item_Class = None
		asset_Class = None
		risClass = None
		supply_Class = None
		wmrClass = None
		was = None
		ld_Class = None
		taskClass = None

		def __init__(self):
			
			
			self.user = User()
			self.userClass = User()
			self.pr = PurchaseRequest()
			self.notif = Notification()
			self.emp = Employees()
			self.kp = KeyPositions()
			self.reqQ = RequestForQuotation()
			self.abc = AbstractOfCanvass()
			self.sup = Suppliers()
			self.po = PurchaseOrder()
			self.ins = InsepectionAndAcceptanceReceipt()
			self.ins_2 = InsepectionAndAcceptanceReceipt_2()
			self.propAcc = PropertyAcceptanceReceipt()
			self.offc = Offices()
			self.item_Class = Items()
			self.asset_Class = Equipment()
			self.risClass = RequisitionAndIssuanceSlip()
			self.supply_Class = Supply()
			self.wmrClass = Waste()
			self.was = WorkAddSub()
			self.ld_Class = LiquidatingDamages()
			self.taskClass = Tasks()



		def generateIDNum(self):
		
			generatedID = ''
		
			generatedID = generatedID + random.choice(string.ascii_letters)
			generatedID = generatedID + random.choice(string.ascii_letters)
			generatedID = generatedID + random.choice(string.ascii_letters)
			generatedID = generatedID + random.choice(string.ascii_letters)

			generatedID = generatedID + '-'         
   
			generatedID = generatedID + str(randint(0,9))
			generatedID = generatedID + str(randint(0,9))
			generatedID = generatedID + str(randint(0,9))
			generatedID = generatedID + str(randint(0,9))

			return generatedID 
	


		def checkLogin(self, uname, password):

			if self.user.isUserRegistered(uname) == False:
					return "username does not exist"
			else:
					if self.user.checkUserPass(uname, password):

						if self.user.getUserDetails(uname)[0][5] == False:
							return "disabled"
						else:	
							userdata = self.user.getUserDetails(uname)
							currentUser = userdata[0][0]
							return "login complete"
					else:
							return "wrong password"
		
		def createUser(self, idnum, username, password):
				pass
		

		'''
=============================================================================================================================================================================================================================
					Create Functions
=============================================================================================================================================================================================================================

		'''
		def createPR(self, reqnum, purpose, details, idnum, itemList):

			employeeData = self.emp.getEmployeeDetails(idnum)

			eFname = employeeData[0][1]
			eSname = employeeData[0][2]
	
			self.pr.addPR(reqnum, purpose, details, idnum)
			self.pr.addPRLoc(reqnum)
			self.pr.addPRToProc(reqnum)
			
			checkAddNewItemData = False
			qtyOfNewItemData = 0
			
			stocknum = 1
			
			for x in itemList:

				itemData = itemList[x] 
				self.pr.addItemToPR(reqnum, stocknum, itemData['1'], itemData['2'], itemData['3'],itemData['4'])
				stocknum = stocknum + 1

				itemDataList = self.item_Class.findItem(itemData['1'])

				if itemData['2'] != " ":
					
					if itemDataList == []:
						
						self.item_Class.addItem(itemData['1'], '', '', itemData['2'], itemData['3'],'')
						checkAddNewItemData = True
						qtyOfNewItemData = qtyOfNewItemData + 1
					
					self.item_Class.updateItemCounter(itemData['1'], "prcounter")

		
			prTotal = self.pr.getTotalCostofPR(self.pr.getItemByPR(reqnum))
			prTotalstr = format(prTotal ,"0,.2f")

			offDetails = self.offc.getOfficeDetails(employeeData[0][4])

			self.notif.adNotif(Functions.generateNotifNum(self), idnum, self.kp.getVCAFRep(), '1', reqnum, "ARRAY ['3','4','<p style=\"margin-bottom:0px;font-weight:bold\">From:</p><p style=\"margin-left:20px;magin-top:0px;\">"+offDetails[1]+"</p>','<p style=\"margin-bottom:0px;font-weight:bold\">Total cost: </p><p style=\"text-indent:20px;magin-top:0px;\">"+prTotalstr+"</p>','A new request was prepared']",'1','pr','pr/'+str(reqnum).replace('-','_')+'/details/')
			self.notif.adNotif(Functions.generateNotifNum(self), idnum, self.kp.getVCAF(), '1', reqnum, "ARRAY ['3','4','<p style=\"margin-bottom:0px;font-weight:bold\">From:</p><p style=\"margin-left:20px;magin-top:0px;\">"+offDetails[1]+"</p>','<p style=\"margin-bottom:0px;font-weight:bold\">Total cost: </p><p style=\"text-indent:20px; magin-top:0px;\">"+prTotalstr+"</p>','A new request was prepared']",'1','pr','pr/'+str(reqnum).replace('-','_')+'/details')

			smoOfficers = self.emp.getEmployeeByOff('SMO')

			for x in smoOfficers:
				self.notif.adNotif(Functions.generateNotifNum(self), idnum, x[0], '1', reqnum, "ARRAY ['3','4','From: "+employeeData[0][4]+"','Total cost: "+prTotalstr+"','A new request was prepared']",'2','pr','pr/'+str(reqnum).replace('-','_')+'/details/')
			
				if checkAddNewItemData == True:
					self.notif.adNotif(Functions.generateNotifNum(self), idnum, x[0], '1', reqnum, "ARRAY ['3','4','"+str(qtyOfNewItemData)+" new item/s','','New Item information was detected that needed to be updated']",'1','item', 'items/')
	
			self.taskClass.addTrans(Functions.generateNotifNum(self), 'Create P.R.', idnum)

		def createPRStaff(self, reqnum, purpose, details, idnum, itemList):

			employeeData = self.emp.getEmployeeDetails(idnum)

			eFname = employeeData[0][1]
			eSname = employeeData[0][2]
	
			self.pr.addPRStaff(reqnum, purpose, details, idnum)
			self.pr.addPRLoc(reqnum)
			self.pr.addPRToProc(reqnum)
			
			checkAddNewItemData = False
			qtyOfNewItemData = 0
			
			stocknum = 1
			
			for x in itemList:

				itemData = itemList[x] 
				self.pr.addItemToPR(reqnum, stocknum, itemData['1'], itemData['2'], itemData['3'],itemData['4'])
				stocknum = stocknum + 1

				itemDataList = self.item_Class.findItem(itemData['1'])

				if itemData['2'] != " ":
					
					if itemDataList == []:
						
						self.item_Class.addItem(itemData['1'], '', '', itemData['2'], itemData['3'],'')
						checkAddNewItemData = True
						qtyOfNewItemData = qtyOfNewItemData + 1
					
					self.item_Class.updateItemCounter(itemData['1'], "prcounter")

		
			prTotal = self.pr.getTotalCostofPR(self.pr.getItemByPR(reqnum))
			prTotalstr = format(prTotal ,"0,.2f")

			offDetails = self.offc.getOfficeDetails(employeeData[0][4])

			self.notif.adNotif(Functions.generateNotifNum(self), idnum, offDetails[3], '1', reqnum, "ARRAY ['3','4','<p style=\"margin-bottom:0px;font-weight:bold\">From:</p><p style=\"margin-left:20px;magin-top:0px;\">"+employeeData[0][1]+" "+employeeData[0][2]+"</p>','<p style=\"margin-bottom:0px;font-weight:bold\">Total cost: </p><p style=\"text-indent:20px;magin-top:0px;\">"+prTotalstr+"</p>','A new request was prepared']",'1','pr', 'off_pr/'+str(reqnum).replace('-','_')+'/details/')
			
			smoOfficers = self.emp.getEmployeeByOff('SMO')

			for x in smoOfficers:
				if checkAddNewItemData == True:
					self.notif.adNotif(Functions.generateNotifNum(self), idnum, x[0], '1', reqnum, "ARRAY ['3','4','"+str(qtyOfNewItemData)+" new item/s','','New Item information was detected that needed to be updated']",'1','item', 'items/')
	
			self.taskClass.addTrans(Functions.generateNotifNum(self), 'Create Staff P.R.', idnum)

		def createNewTimeline(self, reqnum, prnum, prnumdate):

			ceCount = self.pr.getPRCountForNewTimeline(reqnum)
			reqnumNew = reqnum +'-'+ str(ceCount)
			self.pr.addPRToProcNewLine(reqnumNew, prnum, prnumdate)

			prDetails = self.pr.getPRDetails(reqnum)

			self.notif.adNotif(Functions.generateNotifNum(self), '', prDetails[0][4], '1', reqnum, "ARRAY ['5','3','P.R. No.:"+prDetails[0][1]+"','Some items of this request will not be delivered due to some reasons','Your request will undergo recanvassing']",'2','pr')

			return reqnumNew
		
		def addReqQuo(self, refnum, projName, projLoc, canvasser, suppliers, itemList):
			

			quotNum = self.reqQ.generateReqNum()
			self.reqQ.addRequest(quotNum,refnum, projName, projLoc, canvasser)

			
			'''
			for x in suppliers:

				supplierData = suppliers[x]
				compID = self.sup.getCompIDfromName(supplierData['1'])
				
				if compID is None:
					
					self.sup.addSupplier(supplierData['1'], supplierData['2'], supplierData['3'], supplierData['4'], supplierData['5'], '')
					compIDNew = self.sup.getCompIDfromName(supplierData['1'])
					self.reqQ.addComToReq(quotNum, compIDNew)
				
				else:
					self.reqQ.addComToReq(quotNum, compID)
			'''


			counter = 1


			for x in itemList:
				  itemData = itemList[x]
				  self.reqQ.addItemToReq(quotNum, counter, itemData['1'], itemData['2'], itemData['3'], itemData['4'])   
				  counter = counter + 1 

		def addReqQuoWithRQNumIn(self, quotNum, refnum, projName, projLoc, canvasser, suppliers, itemList):
			
			self.reqQ.addRequest(quotNum,refnum, projName, projLoc, canvasser)

			for x in suppliers:

				supplierData = suppliers[x]
				compID = self.sup.getCompIDfromName(supplierData['1'])
				
				if compID is None:
					
					self.sup.addSupplier(supplierData['1'], supplierData['2'], supplierData['3'], supplierData['4'], supplierData['5'], '')
					compIDNew = self.sup.getCompIDfromName(supplierData['1'])
					self.reqQ.addComToReq(quotNum, compIDNew)
				
				else:
					self.reqQ.addComToReq(quotNum, compID)
			
			print(itemList)		

			counter = 1
			for x in itemList:
				  itemData = itemList[x]
				  self.reqQ.addItemToReq(quotNum, counter, itemData['1'], itemData['2'], itemData['3'], itemData['4'])   
				  counter = counter + 1 

		def updateSuppliersOfRQ(self, quotNum, suppliers):
			
			for x in suppliers:
				
				supplierData = suppliers[x]
				compID = self.sup.getCompIDfromName(supplierData['1'])
				
				if compID is None:
					
					self.sup.addSupplier(supplierData['1'], supplierData['2'],'', '', '', '')
					compIDNew = self.sup.getCompIDfromName(supplierData['1'])
					self.reqQ.addComToReq(quotNum, compIDNew)
				
				else:
					
					self.reqQ.addComToReq(quotNum, compID)

			print("Done")

		def addAbsCanv(self, quotNum, openingDate, openingTime, bidData):
					  
			reqDetails =  self.reqQ.getRequestDetails(quotNum)
			reqItems = self.reqQ.getReqItems(quotNum)
			reqComs = self.reqQ.getReqComp(quotNum)
		 
			self.abc.addAbstract(quotNum, quotNum, openingDate, openingDate)


			if reqItems != []:
				
				for x in reqItems:
					self.abc. addItemToAbstract(quotNum, x[1], x[2], x[4], x[3])

				
			if bidData != []:
				
				for x in reqComs:
					
					comData = bidData[x[1]]
					
					itemsBids = comData['itemBidList']

					
					warr = comData['warranty']
					deli = comData['delivery']
					vali = comData['validity']

					comprep = comData['namerep']
					reptel = comData['telrep']
					repemail = comData['emailrep']
				   
					self.reqQ.updateComTerms(quotNum, x[1], warr, deli, vali)
					self.sup.updateSupplierRepInfo(x[1], comprep, reptel, repemail)
				

					for y in itemsBids:                  
						
						bids = itemsBids[y]

						itemNum = self.reqQ.getItemNumFromDescription(quotNum, y)

						self.abc.addSupplierBid(quotNum, x[1], itemNum)

						unitprice = ''
						print('bids '+ str(bids[1]))
						
						if bids[1] == '':
							unitprice = '0'
						else:
							unitprice = bids[1]	

						self.abc.updateSupplierBid(quotNum, itemNum, unitprice , x[1], bids[0])

				
			#preqNum = self.pr.getReqNumFromPR(reqDetails[0][1])       
			#preqDetails = self.pr.getPRDetails(preqNum[0][0])
			prNumArr = (reqDetails[0][1]).split('-')
			preqDetails = self.pr.getPRDetails(str(prNumArr[0])+"-"+str(prNumArr[1]))
					  
			#self.notif.adNotif(Functions.generateNotifNum(self), '', preqDetails[0][4], '1', quotNum, "ARRAY ['3','4','For PR: "+preqDetails[0][1]+"','','You have an Abstract of Canvass to Process']",'1','abstract')
			#self.notif.adNotif(Functions.generateNotifNum(self), '', preqDetails[0][4], '1', quotNum, "ARRAY ['3','4','For PR: "+preqDetails[0][1]+"','You will expect a document containing the bids to your requested item for you to choose on.','Abstract was prepared for your request']",'2','pr')
			Functions.addNotifForPRRequisitioner(self, str(prNumArr[0])+"-"+str(prNumArr[1]), '○ An Abstract of Canvass was created containing the bids for your request items.','○ Expect the document to be delivered or to be fetch to or by your office.','Abstract was prepared for you Request',1,1)

			print("Done Creating Abstract of Canvass")

		def addMultiPOList(self, poList, prnum): # poList is an array in the form "(x,y,z)"
			
			for x in poList:
				self.pr.addMultiPO(prnum, x)
				Functions.createPO(self,  x, '', '', '0001-01-01', '', '0', '', 0, '', prnum, [])
				#789 (self,  ponum, suppID, procmode, deldate, delplace, delterm, payterm, amount, conf, prref, itemList)
		
		def addNewOffice(self, offid, offname, offtype): # poList is an array in the form "(x,y,z)"
			
			self.offc.addOffice(offid, offname, offtype, '', '', '')
			self.offc.addOfficetoLatest(offid)
			

		'''
=============================================================================================================================================================================================================================
					View Functions
=============================================================================================================================================================================================================================

		'''


		#  ---  PURCHASE REQUESTS   ---------------------------------------------------------------

		def getAllPRListByStatus(self, status, statustype):
			output = []

			prList = self.pr.getAllPRByStatus(status, statustype)
			
			for x in prList:
				prDetails = Functions.getPRCompleteDetails(self, x[0], '')
				output = output + [prDetails]

			return output
		
		def getAllPRList(self):
			output = []

			prList = self.pr.getAllPR()

			for x in prList:
				prDetails = Functions.getPRCompleteDetails(self, x[0], '')
				output = output + [prDetails]

			return output		

		def getPRListByPersonnel(self, idnum):
			
			output = []
			
			prList = self.pr.getAllPRbyID(idnum)
			for x in prList:
				prDetails = Functions.getPRCompleteDetails(self, x[0], '')
				output = output + [prDetails]

			return output
		
		def getPRListByStaffPersonnel(self, idnum):
			
			output = []
			
			prList = self.pr.getAllPRbyIDStaff(idnum)
			for x in prList:
				prDetails = Functions.getPRCompleteDetails(self, x[0], 'staff')
				output = output + [prDetails]

			return output

		def getPRListByPersonnelByStatus(self, idnum, status, statustype):
			output = []
			
			
			prList = self.pr.getAllPRByStatusByID(self, status, statustype, idnum)
			
			for x in prList:
				prDetails = Functions.getPRCompleteDetails(self, x[0], '')
				output = output + [prDetails]

			return output				
		
		def getPRlistByOffice(self, offid, detailsType):
			output = []

			empList = self.emp.getEmployeeByOff(offid)
			
			for x in empList:
				
				prList = []

				if detailsType == 'staff':
					prList = Functions.getPRListByStaffPersonnel(self, x[0])
				else:
					prList = Functions.getPRListByPersonnel(self, x[0])

				output = output + prList

			return output    

		def getPRCompleteDetails(self, refNum, detailsType):
			
			output = ()
			prProcDetails = []
			prProcData = None
			prProcCount = 0

			prBasicDetails = self.pr.getPRDetails(refNum)
			prLocDetails = self.pr.getPRLocDetails(refNum)
			
			if prBasicDetails[0][1] != None:
				prProcData = self.pr.getPRNumforPONumForNew(prBasicDetails[0][1])
				prProcCount = len(prProcData)
			

			if prProcCount > 1:
				
				for x in prProcData:

					prProcXData = self.pr.getProCTimeLineDetails(x[0])

					
					toListData = (prProcXData[0], (x[0]).replace('-','_'))

					if prProcXData[0][12] != None and "$" in prProcXData[0][12]:
						multiPOList = self.pr.getMultiPONum(refNum)
						toListData = (prProcXData[0], (x[0]).replace('-','_'), multiPOList)
					
					
					if len(x[0]) == 9:
						prProcDetails.insert(0, toListData)
					
					else:
						prProcDetails = prProcDetails + [toListData,]

			
			else:

					if self.pr.getProCTimeLineDetails(refNum)[0][12] != None and "$" in self.pr.getProCTimeLineDetails(refNum)[0][12]:
						multiPOList = self.pr.getMultiPONum(refNum)
						prProcDetails = (self.pr.getProCTimeLineDetails(refNum)[0], refNum.replace('-','_'), multiPOList)
					
					else:
						prProcDetails = (self.pr.getProCTimeLineDetails(refNum)[0], refNum.replace('-','_'))

					
			urlString = refNum.replace('-','_')
			totalCostOfPR = self.pr.getTotalCostofPRItems(refNum)
			requestingOfficer = ''
			
			if detailsType == 'staff':
				requestingOfficer = self.emp.getEmployeeDetails(prBasicDetails[0][15])
			else:
				requestingOfficer = self.emp.getEmployeeDetails(prBasicDetails[0][4])
			
			requestingOffice = self.offc.getOfficeDetails(requestingOfficer[0][4])

			output = (prBasicDetails[0], prLocDetails[0], prProcDetails, (totalCostOfPR, requestingOfficer[0], requestingOffice), (urlString, prProcCount, Functions.genRepeaterString(self, prProcCount)))

			return output	
	
		def getPRBasicDetails(self, refNum, detailsType):
			
			output = ()
			prProcDetails = []
			prProcData = None
			prProcCount = 0

			prBasicDetails = self.pr.getPRDetails(refNum)
			
			urlString = refNum.replace('-','_')
			totalCostOfPR = self.pr.getTotalCostofPRItems(refNum)
			requestingOfficer = ''
			
			if detailsType == 'staff':
				requestingOfficer = self.emp.getEmployeeDetails(prBasicDetails[0][15])
			else:
				requestingOfficer = self.emp.getEmployeeDetails(prBasicDetails[0][4])
			
			requestingOffice = self.offc.getOfficeDetails(requestingOfficer[0][4])

			output = (prBasicDetails[0], (totalCostOfPR, requestingOfficer[0], requestingOffice), (urlString))

			return output	
		
		def getPRCompleteDetailsWithItems(self, refNum):
			
			output = []

			prBasicDetails = self.pr.getPRDetails(refNum)
			prLocDetails = self.pr.getPRLocDetails(refNum)
			prProcDetails = self.pr.getProCTimeLineDetails(refNum)
			urlString = refNum.replace('-','_')
			totalCostOfPR = self.pr.getTotalCostofPRItems(refNum)
			requestingOfficer = self.emp.getEmployeeDetails(prBasicDetails[0][4])
			requestingOffice = self.offc.getOfficeDetails(requestingOfficer[0][4])

			prItems = self.pr.getItemByPR(refNum)
			prItemToOutput = []
			for x in prItems:
				if '$' in x[2]:
					prItemDescription = str(x[2]).split('$')
					prItemToOutput = prItemToOutput + [(x[0], x[1], prItemDescription, x[3], x[4], x[5], x[6] ),]
				else:
					prItemToOutput = prItemToOutput + [(x[0], x[1], x[2], x[3], x[4], x[5], x[6] ),]	

			output = [prBasicDetails[0], prLocDetails[0], prProcDetails[0], (totalCostOfPR,  requestingOfficer[0], requestingOffice), (urlString,), prItemToOutput]

			return output	
		
		def getRQCompleteDetailsWithItemss(self, rqNum):
			
			rqDetails = self.reqQ.getRequestDetails(rqNum)

			canvasserDetails = []
			
			if rqDetails[0][5] != None:
				canvasserDetails = self.emp.getEmployeeDetails(rqDetails[0][5])

			abcNum = self.abc.getAbstractNumFromBidNum(rqNum)
			abcDetails = []

			if abcNum != None:
				abcDetails = self.abc.getAbstractDetails(abcNum)

			
			prRefNumArr = str(rqDetails[0][1]).split('-') 
			prRefNum = prRefNumArr[0]+'-'+prRefNumArr[1]

			prCDetails = Functions.getPRBasicDetails(self, prRefNum, '')
			prPDetails = self.pr.getProCTimeLineDetails(prRefNum)

			rqCompListDetails = []
			
			rqCompList = self.reqQ.getReqComp(rqNum)

			for x in rqCompList:

				supcompDetails = self.sup.getSupllierDetails(x[1])
				rqCompListDetails = rqCompListDetails + [((x),supcompDetails[0]),]

			return [prCDetails, (rqDetails[0], canvasserDetails), abcDetails, rqCompListDetails, prPDetails]	

		def genRepeaterString(self, inputNum):
			output = ''

			for x in range(0,inputNum):
				output = output + '*'

			return output

		def getFunction(self, refNum):
				pass	

		#  -------  REQUEST FOR QUOTATIONS --------------------------------------------------------------------------------		

		#  -------  PAR --------------------------------------------------------------------------------		

		def getPARListItems(self, parNumRef):

			output = []
			
			parItemsList = self.asset_Class.getAllEquiListbyPARNum(parNumRef)
			parItemsNoNumList = self.asset_Class.getAllEquiNoNumListbyPARNum(parNumRef)

			counter = 1
			for x in parItemsList:

				toArrX = ['1',x]
				itemDetails = self.asset_Class.getEquiIndiDetailsbyPARNum(x[0], parNumRef)


				if "$" in x[0]:
					
					descripArr = (x[0]).split('$')
					toArrXx = list(x)

					toArrXx[0] = descripArr
					toArrX[0] = '2'
					toArrX[1] = tuple(toArrXx)

				output = output + [(toArrX, len(itemDetails), itemDetails, counter)]
				counter = counter + 1
			
			counter = 1
			for x in parItemsNoNumList:
				toArrX = ['1',x]
				itemDetails = self.asset_Class.getEquiIndiDetailsNoNumbyPARNum(x[0], parNumRef)

				if "$" in x[0]:
					
					descripArr = (x[0]).split('$')
					toArrXx = list(x)

					toArrXx[0] = descripArr
					toArrX[0] = '2'
					toArrX[1] = tuple(toArrXx)

				output = output + [(toArrX, len(itemDetails), itemDetails, counter)]
				counter = counter + 1
			
			return output    

		def getPARListItemsForJSON(self, parNumRef):

			output = {}

			parItemsList = self.asset_Class.getAllEquiListbyPARNum(parNumRef)

			counter = 1

			for x in parItemsList:

				toArrX = x

				itemDetails = self.asset_Class.getEquiIndiDetailsbyPARNum(x[0], parNumRef)

				itemDetailsList = {}

				counter2 = 1
				for xx in itemDetails:
					itemDetailsList[str(counter2)]= {
													 'invnum':xx[0],
													 'serialnum':xx[2],
													 'status':xx[1],

													}
					counter2 = counter2 + 1

				output[str(counter)] = {'invNum': len(itemDetails),
		        						'descrip': x[0],
		        						'unit': x[1],
		        						'unitprice': x[2],
		        						'quantity': x[4],
		        						'total': x[5],
		        						'list': itemDetailsList,

								        }

				counter = counter + 1

			return output

		def getItemsByPersonelID(self, idnum):
			
			output = []
			tempref = {}

			parlist = self.propAcc.getPAROFID(idnum)
			
			counter = 0
			
			for x in parlist:
				itemlist = Functions.getPARListItems(self, x[0])

				for xx in itemlist:
					check = False
					refData = xx[0][1][0]
					
					if str(type(refData)) == "<class 'list'>":
						check = True
						refData1 = ''
						for x in refData:
							refData1 = refData1 + x

						refData = refData1	
					

					if refData in tempref:
					

						output[tempref[refData]][1]	= output[tempref[refData]][1] + xx[0][1][4]
						output[tempref[refData]][2] = output[tempref[refData]][2] + xx[0][1][5]
						output[tempref[refData]][3] = output[tempref[refData]][3] + xx[2]
						output[tempref[refData]][4] = output[tempref[refData]][4] + len(xx[2])

					else:
						
						tempref[refData] = counter
						output = output + [[xx[0][1]+(check,), xx[0][1][4],  xx[0][1][5], xx[2], len(xx[2])],]
					
					counter = counter + 1
				
			return output

		def getItemsByOffice(self, officeid):
			output = []
			tempref = {}
			empList = self.emp.getEmployeeByOff(officeid)
			
			counter = 0
			
			for x in empList:
				itemList = Functions.getItemsByPersonelID(self, x[0])
				empDetails = self.emp.getEmployeeDetails(x[0])
				

				for xx in itemList:
					refData = xx[0][0]
					
					if str(type(refData)) == "<class 'list'>":
						refData1 = ''
						for x in refData:
							refData1 = refData1 + x

						refData = refData1	
					
					if refData in tempref:

						output[tempref[refData]][1]	= output[tempref[refData]][1] + xx[1]
						output[tempref[refData]][2] = output[tempref[refData]][2] + xx[2]
						output[tempref[refData]][3] = output[tempref[refData]][3] + xx[3]
						output[tempref[refData]][4] = output[tempref[refData]][4] + len(xx[3])

					else:
						tempref[refData] = counter
						output = output + [xx + [empDetails[0],]]
						
					counter = counter + 1	
			
			
			return output


#      ++--------------------------------------------------------------------------------
#			Supplies
		
		def getAllSupplies(self):
			
			output = []
			suppList = self.supply_Class.getAllSupplyInventoryID()

			for x in suppList:
				suppDetails = Functions.getCompleteSupplyDetails(self, x[0])
				output = output + [suppDetails,]


			return output	

		def getAllSuppliesWithOfficeInfo(self, officeid):
			
			output = []
			suppList = self.supply_Class.getAllSupplyInventoryID()
			
			currQuarter = Functions.getCurrQuarter(self)
			currentDate = datetime.now()
			
			dateFrom = datetime(int(currentDate.year), int(currQuarter[2][0]), 1)
			dateTo = datetime(currentDate.year, int(currQuarter[2][2]), currentDate.day) 


		

			for x in suppList:
				suppDetails = Functions.getCompleteSupplyDetails(self, x[0])
				suppDetails1 = self.supply_Class.getSupplyDetails(x[0])

				allConsumed = self.risClass.getAllRISByItemConsumtion(suppDetails1[0][1])
				curQuarConsumed = self.risClass.getQuarRISByItemConsumtion(dateFrom, dateTo, suppDetails1[0][1])

				suppOffDetails = Functions.getOfficeComsumptionOfItem(self, officeid, x[0])

				output = output + [[suppDetails, suppOffDetails, [curQuarConsumed, allConsumed]],]

			return output				

		def getCompleteSupplyDetails(self, suppId):
			
			supplyDetails = self.supply_Class.getSupplyDetails(suppId)
			itemDetails = self.item_Class.getItemDetails(supplyDetails[0][4])
			rank = [0,'message']

			availRate = (supplyDetails[0][5]/supplyDetails[0][6])*100

			availRateString = []
			if supplyDetails[0][5] != 0:
				if availRate > 59 and availRate < 101:
					availRateString = ['High','Plenty','Available for request', availRate,'#00a65a','#1a755b']

				if availRate > 34 and availRate < 60:
					availRateString = ['Medium','Partly Consumed', 'Still available for request', availRate,'#00a65a','#1a755b']
				
				if availRate > 19 and availRate < 35:
					availRateString = ['Low','Near Depletion','Only few remaining', availRate,'#d2983c','#a97b00']
				
				
				if availRate > 0 and availRate < 20:
					availRateString = ['Very Low','Almost Consumed','Very few remaining',availRate,'#a94442','#841614']
				

			else:		
				availRateString = ['Zero','Depleted','All was consumed',0,'#a94442','#841614']

			return [supplyDetails[0], itemDetails[0], rank, availRateString, (suppId.replace('-','_'), str(itemDetails[0][0]).replace('-','_'))]	

		def getOfficeComsumptionOfItem(self, officeid, suppid):
		  	
		  	currQuarter = Functions.getCurrQuarter(self)
		  	currentDate = datetime.now()

		  	dateFrom = datetime(int(currentDate.year), int(currQuarter[2][0]), 1)
		  	
		  	dateTo = datetime(currentDate.year, int(currQuarter[2][2]), int(currQuarter[3][0])) 

		  	suppDetails = self.supply_Class.getSupplyDetails(suppid)

		  	allConsumed = self.risClass.getAllRISByItemConsumtion(suppDetails[0][1])
		  	curQuarConsumed = self.risClass.getQuarRISByItemConsumtion(dateFrom, dateTo, suppDetails[0][1])

		  	empList = self.emp.getEmployeeByOff(officeid)
		  	
		  	offConsumed = 0
		  	offRequested = 0
		  	numOfQurRIs = 0
		  	perAppQuar = 0
		  	perToAllQuarConsumed = 0
		  	perToAllQuarRequestd = 0
		  	avgQuarReqQty = 0

		  	allOffConsumed = 0
		  	allOffRequested = 0
		  	numOfAllRIS = 0
		  	perAppAll = 0
		  	perToAllConsumed = 0
		  	perToAllRequestd = 0
		  	avgReqQty = 0		  	


		  	if empList != []:

			  	for x in empList:
					  	allrisList = self.risClass.getAllRISbyID(x[0]);
				  		currQuarRISList = self.risClass.getAllRISbyIDTimeFrame(x[0], dateFrom.strftime('%Y-%m-%d'), dateTo.strftime('%Y-%m-%d'))

				  		consumedQTY = 0;
				  		requestedQTY = 0;
				  		
				  		if currQuarRISList != []:
						  	for xx in currQuarRISList:

						  		consumed = self.risClass.getRISByItemConsumtion(xx[0], suppDetails[0][1]);

						  		if consumed[0][0] != None:
							  		consumedQTY = consumedQTY + consumed[0][0];
							  		requestedQTY = requestedQTY + consumed[0][1];

						  	offConsumed = offConsumed + consumedQTY;
						  	offRequested = offRequested + requestedQTY;
						  	numOfQurRIs = numOfQurRIs + len(currQuarRISList);

					  	allConsumedQTY = 0;
					  	allRequestedQTY = 0;
					  	

					  	if allrisList != []:
					  		
						  	for xx in allrisList:
						  		
						  		consumed = self.risClass.getRISByItemConsumtion(xx[0], suppDetails[0][1]);
						  		
						  		if consumed[0][0] != None:
							  		allConsumedQTY = allConsumedQTY + consumed[0][0];
							  		allRequestedQTY = allRequestedQTY + consumed[0][1];

						  	allOffConsumed = allOffConsumed + allConsumedQTY;
						  	allOffRequested = allOffRequested + allRequestedQTY;
						  	numOfAllRIS = numOfAllRIS + len(allrisList);

				
		  		if offConsumed != 0:
			  		perAppQuar = (offConsumed/offRequested)*100;
			  		perToAllQuarConsumed = (offConsumed/curQuarConsumed[0])*100
			  		perToAllQuarRequestd = (offRequested/curQuarConsumed[1])*100
			  		avgQuarReqQty = offRequested/numOfAllRIS

			  	if allOffConsumed != 0:
			  		perAppAll = (allOffConsumed/allOffRequested)*100
			  		perToAllConsumed = (allOffConsumed/allConsumed[0][0])*100
			  		perToAllRequestd = (allOffRequested/allConsumed[0][1])*100
			  		avgReqQty = allOffRequested/numOfAllRIS

		  		return [[offConsumed, offRequested, numOfQurRIs, perAppQuar, perToAllQuarConsumed, perToAllQuarRequestd, avgQuarReqQty],[allOffConsumed, allOffRequested, numOfAllRIS, perAppAll, perToAllConsumed, perToAllRequestd, avgReqQty]]

		  	else:
		  		return [[0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0]]	

		def getAllOfficeComsuptionOfAnItem(self, suppid):
		  	
		  	output = []

		  	offList = self.offc.getAllOfficesSorted()

		  	for x in offList:
		  		offDetails = self.offc.getOfficeDetails(x[0])
		  		
		  		output = output + [[offDetails, Functions.getOfficeComsumptionOfItem(self, x[0], suppid)],]	

		  	return output			


		'''
=============================================================================================================================
						Update Functions
=============================================================================================================================
		'''

		def acceptPR(self, reqnum, purpose, details, itemList, isEdit, decision):
			print("++++++++++++++++++++++++++++++++++++++++")
			print(decision)
			print(isEdit)
			
			if decision == 'false':
				self.pr.updateStaffPRAcceptance(reqnum, False, 'NULL')
			
			else:	
				
				self.pr.updateStaffPRAcceptance(reqnum, True, isEdit)

				if isEdit:
					self.pr.removeItemsFromPR(reqnum)

					stocknum = 1
				
					for x in itemList:

						itemData = itemList[x] 
						self.pr.addItemToPR(reqnum, stocknum, itemData['1'], itemData['2'], itemData['3'],itemData['4'])
						stocknum = stocknum + 1

						itemDataList = self.item_Class.findItem(itemData['1'])

						if itemData['2'] != " ":
							
							if itemDataList == []:
								
								self.item_Class.addItem(itemData['1'], '', '', itemData['2'], itemData['3'],'')
								checkAddNewItemData = True
								qtyOfNewItemData = qtyOfNewItemData + 1
							
							self.item_Class.updateItemCounter(itemData['1'], "prcounter")


				prDetails = self.pr.getPRDetails(reqnum)			
				empDetails = self.emp.getEmployeeDetails(prDetails[0][15])
				offDetails = self.offc.getOfficeDetails(empDetails[0][4])

				self.notif.adNotif(Functions.generateNotifNum(self), '', prDetails[0][15], '1', prDetails[0][0], "ARRAY ['3','4','Your request was accepted by your office head official.','It is now being reviewed for approval.','Request was Accepted']",'2','pr', 'pr/'+str(prDetails[0][0]).replace('-','_')+'/details/')
				
				prTotal = self.pr.getTotalCostofPR(self.pr.getItemByPR(reqnum))
				prTotalstr = format(prTotal ,"0,.2f")
				
				self.notif.adNotif(Functions.generateNotifNum(self), '', self.kp.getVCAFRep(), '1', prDetails[0][0], "ARRAY ['3','4','<p style=\"margin-bottom:0px;font-weight:bold\">From:</p><p style=\"margin-left:20px;magin-top:0px;\">"+offDetails[1]+"</p>','<p style=\"margin-bottom:0px;font-weight:bold\">Total cost: </p><p style=\"text-indent:20px;magin-top:0px;\">"+prTotalstr+"</p>','A new request was prepared']",'1','pr','pr/'+str(prDetails[0][0]).replace('-','_')+'/details/')
				self.notif.adNotif(Functions.generateNotifNum(self), '', self.kp.getVCAF(), '1', prDetails[0][0], "ARRAY ['3','4','<p style=\"margin-bottom:0px;font-weight:bold\">From:</p><p style=\"margin-left:20px;magin-top:0px;\">"+offDetails[1]+"</p>','<p style=\"margin-bottom:0px;font-weight:bold\">Total cost: </p><p style=\"text-indent:20px; magin-top:0px;\">"+prTotalstr+"</p>','A new request was prepared']",'1','pr','pr/'+str(prDetails[0][0]).replace('-','_')+'/details')


				self.pr.updatePRTable('requester_id', 'String', offDetails[3], reqnum)
				self.pr.updatePRTable('date_created', 'date', datetime.now().strftime('%Y-%m-%d'), reqnum)	

				self.taskClass.addTrans(Functions.generateNotifNum(self), 'Accept P.R.', prDetails[0][4])		
		
		def holdCancelPR(self, reqnum, decision):
			
			if decision == 'false':
				self.pr.updatePRStatus(reqnum, 'FALSE')
			if decision == '':
				self.pr.updatePRStatus(reqnum, 'NULL')	
			if decision == 'true':
				self.pr.updatePRStatus(reqnum, 'TRUE')									

		def approvePR(self, reqnum, editstat, theMatrix):
			
			self.pr.updatePRApproval(reqnum, 'approval_status', 'TRUE', '')
			self.pr.updatePRApprovalDate(reqnum)

			prDetails = self.pr.getPRDetails(reqnum)
			prTotal = self.pr.getTotalCostofPRItems(reqnum)

			if editstat == 'true':
				self.pr.updatePRTable('init_app_edit', 'boolean', 'TRUE', reqnum)

				for x in theMatrix:
					mData = theMatrix[x]
					self.pr.updatePRItemInfo(mData['1'], mData['4'], mData['3'], reqnum, x)
			
			procUsers = self.user.getProcUsers();

			for x in procUsers:
				self.notif.adNotif(Functions.generateNotifNum(self), self.kp.getChancellor(), x[0], '1', reqnum, "ARRAY ['5','3','A PR has been approved by the Chancellor','Expect a document to be delivered to your office.']",'2','pr')

			Functions.addNotifForPRRequisitioner(self, reqnum, 'For the Request with Purpose:', '  '+prDetails[0][2], 'The Chancellor had Approved the Request', 1, 1)


		def approvePRWithEdit(self, reqnum):
			
			self.pr.updatePRApproval(reqnum, 'approval_status', 'TRUE', '')
			self.pr.updatePRApprovalDate(reqnum)

			prDetails = self.pr.getPRDetails(reqnum)
			prTotal = self.pr.self.pr.getTotalCostofPRItems(reqnum)
			
			procUsers = self.user.getProcUsers();

			for x in procUsers:
				self.notif.adNotif(Functions.generateNotifNum(self), self.kp.getChancellor(), x[0], '1', reqnum, "ARRAY ['3','1','','Expect a document to be delivered to your office.','A PR has been approved by the Chancellor']",'2','pr')

			self.notif.adNotif(Functions.generateNotifNum(self), self.kp.getChancellor(), prDetails[0][4], '1', reqnum, "ARRAY ['1','1','Some changes were made on your request.','The document will be sent to the Procurement Off. to proceed.','Your Purchase Request was Approved.']",'2','pr')

			
		def declinePR(self, reqnum, reason):
			
			self.pr.updatePRApproval(reqnum, 'approval_status', 'FALSE', reason)

			prDetails = self.pr.getPRDetails(reqnum)
			prTotal = self.pr.self.pr.getTotalCostofPRItems(reqnum)
			
			Functions.addNotifForPRRequisitioner(self, reqnum, 'Reason:', reason, 'The Chancellor had Denied the Request', 5, 3)
			#self.notif.adNotif(Functions.generateNotifNum(self), self.kp.getChancellor(), prDetails[0][4], '1', reqnum, "ARRAY ['5','3','Reason: ','	"+reason+"','Your Purchase Request was Declined.']",'2','pr')

		
		def initApprovePR(self, reqnum, editstat, theMatrix):

			reqDetails = self.pr.getPRDetails(reqnum)
			reqid = reqDetails[0][4]

			employeeData = self.emp.getEmployeeDetails(reqid)

			eFname = employeeData[0][1]
			eSname = employeeData[0][2]

			self.pr.updatePRApproval(reqnum, 'init_approval_status', 'TRUE', '')

			if editstat == 'true':
				self.pr.updatePRTable('init_app_edit', 'boolean', 'TRUE', reqnum)

				for x in theMatrix:
					mData = theMatrix[x]
					self.pr.updatePRItemInfo(mData['1'], mData['4'], mData['3'], reqnum, x)

			prTotal = self.pr.getTotalCostofPR(self.pr.getItemByPR(reqnum))
			prTotalstr = format(prTotal ,"0,.2f")
			
			Functions.addNotifForPRRequisitioner(self, reqnum, 'For the Request with Purpose:', '  '+reqDetails[0][2], 'The VCAF had accepted the Request', 1, 1)
			
			self.notif.adNotif(Functions.generateNotifNum(self), reqid, self.kp.getChancellor(), '1', reqnum, "ARRAY ['3','4','From: "+employeeData[0][4]+"','Total cost: "+prTotalstr+"','You have a new Purchase Request']",'1','pr','pr/'+str(reqnum).replace('-','_')+'/details')
			self.notif.adNotif(Functions.generateNotifNum(self), reqid, self.kp.getChancellorRep(), '1', reqnum, "ARRAY ['3','4','From: "+employeeData[0][4]+"','Total cost: "+prTotalstr+"','You have a new Purchase Request']",'1','pr','pr/'+str(reqnum).replace('-','_')+'/details')

		def initDeclinePR(self, reqnum, reason):
			
			prDetails = self.pr.getPRDetails(reqnum)
			prTotal = self.pr.getTotalCostofPRItems(reqnum)

			prTotalstr = format(prTotal ,"0,.2f")

			self.notif.adNotif(Functions.generateNotifNum(self), self.kp.getVCAF(), prDetails[0][4], '1', reqnum, "ARRAY ['5','3','Reason: ','	"+reason+"','Your Purchase Request was Declined.']",'2','pr')
		
		def cancelPR(self, reqnum):

			self.pr.updatePRStatus(reqnum, 'FALSE')


		def updateOfficeHead(self, offid, offidnum):

			offDetails = self.offc.getOfficeDetails(offidnum)

			if offDetails[3] != None:
				self.user.updateUserAccessType(offDetails[3], 4, 5)

			if offidnum == 'VCAF' or offidnum == 'OC' or offidnum == 'SMO' or offidnum == 'PROC' or offidnum == 'AcctO':
				offHeadEqui = {
								'VCAF' : 1,
								'OC' : 1,
								'SMO' : 30,
								'PROC' : 2,
								'AcctO' : 6,
				}
				
				if offidnum == 'VCAF':
					self.kp.setVCAF(offid)
				
				if offidnum == 'OC':
					self.kp.setChancellor(offid)
				
				self.user.updateUserAccessType(offid, 5, offHeadEqui[offidnum])
			
			else:
				self.user.updateUserAccessType(offid, 5, 4)


			self.offc.updateHead(offidnum, offid)
		

		def updateMultiPOData(self, updateList, reqnum):
			pass
				
#   ==================================================================================
#		PAR Update
		
		def updateTranferPAR(self, parnum, idnum):
			
			parDetails = self.propAcc.getPARDetails(parnum)

			self.propAcc.tranferPAR(parnum, idnum)


		'''
=============================================================================================================================
						Special Functions
=============================================================================================================================
		'''
		def getListFromItemList(self, input, idxref):
			
			itemlist = input

			for idx, x in enumerate(itemlist):
				if "$" in x[idxref]:
					xList = list(x)
					xList[idxref] = ('multi', str(x[idxref]).split('$'))
					xTuple = tuple(xList)

					itemlist[idx] = xTuple

			return itemlist		

		def getCurrQuarter(self):
			
			curMon = datetime.now().month

			quarters = {
						1:[(1,2,3),('1st','First', 'January - March'),(31,)],
						2:[(4,5,6),('2nd','Second', 'April - June'),(30,)],	
						3:[(7,8,9),('3rd','Third', 'July - September'),(30,)],
						4:[(10,11,12),('4th','Forth', 'October - December'),(31,)],			
			}
			
			idx = 1
			
			while curMon not in quarters[idx][0]:
				idx = idx + 1;	

			return (idx, quarters[idx][1], quarters[idx][0], quarters[idx][2])	

		def addNotifForPRRequisitioner(self, reqnum, msg1, msg2, titlemsg, iconnum, typenum):
			prDetails = self.pr.getPRDetails(reqnum)
			self.notif.adNotif(Functions.generateNotifNum(self), '', prDetails[0][4], '1', reqnum, "ARRAY ['"+str(iconnum)+"','"+str(typenum)+"','"+msg1+"','"+msg2+"','"+titlemsg+"']",'2','pr', 'pr/'+str(reqnum).replace('-','_')+'/details')			
				

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
		
		


		def createRIS(self, reqnum, purpose, details, idnum, itemList):

			employeeData = self.emp.getEmployeeDetails(idnum)

			eFname = employeeData[0][1]
			eSname = employeeData[0][2]

			self.risClass.addRIS(reqnum, purpose, details, idnum)
			
			stocknum = 1
			
			for x in itemList:

				itemData = itemList[x] 
				self.risClass.addItemToRIS(reqnum, stocknum, itemData['1'], itemData['2'], itemData['3'])
				stocknum = stocknum + 1

				itemDataList = self.item_Class.findItem(itemData['1'])

				self.item_Class.updateItemCounter(itemData['1'], "riscounter")
				self.item_Class.updateItemQuantityOnRequest(itemData['1'], itemData['3'])


			smoAdminUser = self.user.getSMOAdminUser();
			
			self.notif.adNotif(Functions.generateNotifNum(self), idnum, smoAdminUser[0][0], '1', reqnum, "ARRAY ['3','4','From: "+employeeData[0][4]+"','purpose: "+purpose+"','Your have a new R.I.S. waiting for your approval']",'1','ris','ris/'+str(reqnum).replace('-','_')+'/details/')
			
		def createPRBasic(self, reqnum, purpose, details, idnum, itemList):
			
			employeeData = self.emp.getEmployeeDetails(idnum)

			eFname = employeeData[0][1]
			eSname = employeeData[0][2]

			self.pr.addPR(reqnum, purpose, details, idnum)
			
			stocknum = 1
			for x in itemList:

				itemData = itemList[x] 
				self.pr.addItemToPR(reqnum, stocknum, itemData['1'], itemData['2'], itemData['3'],itemData['4'])
				stocknum = stocknum + 1

			prTotal = self.pr.getTotalCostofPR(self.pr.getItemByPR(reqnum))
			prTotalstr = format(prTotal ,"0,.2f")
			
			procUsers = self.user.getProcUsers();
			
			for x in procUsers:

				self.notif.adNotif(Functions.generateNotifNum(self), idnum, x[0], '1', reqnum, "ARRAY ['3','4','From: "+employeeData[0][4]+"','Total cost: "+prTotalstr+"','A new Pruchase Request was create and now under consideration for approval']",'1','pr')
			
		def numberPR(self, reqnum):
			
			prnum = self.pr.generateReqNum()
			
			reqDetails = self.pr.getPRDetails(reqnum)
			reqid = reqDetails[0][4]

			self.pr.setPRNumber(reqnum)

			prTotal = self.pr.getTotalCostofPR(self.pr.getItemByPR(reqnum))

			self.notif.adNotif(Functions.generateNotifNum(self), '',reqid, '1', reqnum, "ARRAY ['1','1','','PR Number: "+prnum+"','Your Purchase Request was Approved']",'2','pr')

			procUsers = self.user.getProcUsers();
			
			for x in procUsers:
				
				if prTotal < 500000:
					self.notif.adNotif(Functions.generateNotifNum(self), self.kp.getChancellor(), x[0], '1', reqnum, "ARRAY ['5','1','','PR Number: "+prnum+"','There is a New Approved Purchase Request']",'2','pr')
		
		def numberPRFromInput(self, reqnum, inputprnum):
			
			prnum = self.pr.generateReqNum()
			
			reqDetails = self.pr.getPRDetails(reqnum)
			reqid = reqDetails[0][4]

			self.pr.setPRNumberFromInput(reqnum, inputprnum)


			#prTotal = self.pr.getTotalCostofPR(self.pr.getItemByPR(reqnum))

			#self.notif.adNotif(Functions.generateNotifNum(self), '',reqid, '1', reqnum, "ARRAY ['1','1','','PR Number: "+prnum+"','Your Purchase Request was Approved']",'2','pr')
			
			'''
			procUsers = self.user.getProcUsers();
			
			for x in procUsers:
				
				if prTotal < 500000:
					self.notif.adNotif(Functions.generateNotifNum(self), self.kp.getChancellor(), x[0], '1', reqnum, "ARRAY ['5','1','','PR Number: "+prnum+"','There is a New Approved Purchase Request']",'2','pr')
			'''

			print('Done')

		def approveRIS(self, slipnum, itemData):
			
			risDetails = self.risClass.getRISDetails(slipnum)
			self.risClass.updateRISApproval(slipnum, 'TRUE', '')	
			self.risClass.setRISNumber(slipnum)
			
			for x in itemData:
				apprQty = itemData[x]
				self.risClass.updateRISApprovedQty(slipnum, x, apprQty)

			self.notif.adNotif(Functions.generateNotifNum(self), '', risDetails[0][4], '1',slipnum, "ARRAY ['1','1','You or your representative may now claim your requested items','View the details and follow the instructions indicated to claim the items','Your RIS was approved.']",'2','ris')	

		def realeaseRIS(self, slipnum, recOfficer):

			risDetails = self.risClass.getRISDetails(slipnum)
			self.risClass.releaseRIS(slipnum, recOfficer)
			risItems = self.risClass.getItemByRIS(slipnum)
			empDetails = self.emp.getEmployeeDetails(recOfficer)	

			for x in risItems:
				itemIDCode = self.supply_Class.getSupplyIDFromDescription(x[2])
				self.supply_Class.updateSupplySubQuantity( itemIDCode, x[5])
				self.item_Class.updateSubtractItemQuantityOnRequest(x[2], x[5])

			self.notif.adNotif(Functions.generateNotifNum(self), '', risDetails[0][4], '1',slipnum, "ARRAY ['1','1','RIS No. "+risDetails[0][1]+"','Claimed by: "+empDetails[0][2]+ ", "+empDetails[0][1]+"','Your request Items on a RIS has been claimed']",'2','ris','')		
			print("Done")

		def getPRbyID(self, idnum):
			output = []
			prList = self.pr.getAllPRbyID(idnum)

			for reqNum in prList:
				prDetails = self.pr.getPRDetails(reqNum[0])
				prTotal = self.pr.getTotalCostofPR(self.pr.getItemByPR(reqNum[0]))
				completeDetails = prDetails[0] + (prTotal,)
				output = output + [completeDetails]

			return output

		def getReqStat(self, idnum):
			
			allPRs = len(self.pr.getAllPRbyID(idnum))
			approvedPRs = len(self.pr.getAllApprovedPRbyID(idnum))
			initPendingPRs = len(self.pr.getAllInitPendingPRbyID(idnum))
			pendingPRs = len(self.pr.getAllPendingPRbyID(idnum))
			deniedPRs = len(self.pr.getAllDeclinedPRbyID(idnum))


			print("---------------------------+++++++++++-----------------------------")
			print(self.pr.getAllInitPendingPRbyID(idnum))
			print(initPendingPRs + pendingPRs)

			return [(allPRs, approvedPRs, initPendingPRs + pendingPRs, deniedPRs),]

		def getPARStat(self, idnum):
			
			allPARTotal = 0
			allPARQuantity = 0
			parList = self.propAcc.getPAROFID(idnum)

			for x in parList:
				parTotal = self.propAcc.getPARTotal(self.propAcc.getPARItems(x[0]))
				parItemTotal = self.propAcc.getTotalQuantityOfPAR(self.propAcc.getPARItems(x[0]))

				allPARTotal = allPARTotal + parTotal
				allPARQuantity = allPARQuantity +parItemTotal


			return (len(parList), allPARTotal, allPARQuantity)   
		
		def updateItemData(self, itemid, description, itemClass, unit, price, partID):
				
			self.item_Class.updateItemInfo(itemid, description, '', itemClass, unit, price, partID)

			prList = self.pr.getUnclassifiedPRByDescription(description)

			for x in prList:
				self.pr.updatePRType(x[0], itemClass)


			print("Done")

		def getPRItemsbyID(self, idnum):
			output = []
			prList = self.pr.getAllPRbyID(idnum)

			for reqNum in prList:
				prItems = self.pr.getItemByPR(reqNum[0])
				output = output + prItems

			return output    

		def getProcUsers(self):
			pass    
		

		def updateAbstractBids(self, canvnum, updateData, recomendation):

				for x in updateData:
					self.abc.setSelectedBid(canvnum, x, updateData[x])

				self.abc.updateRecomendation(canvnum, recomendation)
				self.abc.setAbstractAsProcessed(canvnum)
				numOfWinners = len(self.abc.getWinningSuppliers(canvnum))    
				
				procUsers = self.user.getProcUsers();
				
				for x in procUsers:

					self.notif.adNotif(Functions.generateNotifNum(self), '', x[0], '1', canvnum, "ARRAY ['1','1','Abstract No.: "+canvnum+"','Num. of Winner/s: "+str(numOfWinners)+" Bidder/s','Bid winners has been seleted']",'2','abstract')
		   
				print("Update Complete")    
		
		def createPO(self,  ponum, suppID, procmode, deldate, delplace, delterm, payterm, amount, conf, prref, itemList):

			self.po.addPO(ponum, suppID, procmode, deldate, delplace, delterm, payterm, amount, conf, prref)
			
			stocknum = 1
			for x in itemList:

				itemData = itemList[x] 
				self.po.addItemToPO(ponum, stocknum, itemData['4'], itemData['2'], itemData['1'], itemData['3'])
				stocknum = stocknum + 1

			
			poItems = self.po.getItemByPO(ponum)    

			poTotal = self.po.getTotalCostofPO(poItems)  
			self.po.updatePOAmount(ponum, poTotal)
	
			reqNum = self.pr.getReqNumFromPR(prref)
			reqDetails = self.pr.getPRDetails(prref)

			#self.notif.adNotif(Functions.generateNotifNum(self), '', self.kp.getChancellor(), '1', ponum, "ARRAY ['3','4','Reference: PR no. "+prref+"','Total Cost: "+str(poTotal)+"','A new Purchase Order has been prepared']",'2','po')
			#self.notif.adNotif(Functions.generateNotifNum(self), '', reqDetails[0][4], '1', reqNum[0][0], "ARRAY ['1','1','Reference: PR no. "+prref+"','Total Cost: "+str(poTotal)+"','The Purchase Order has been prepared for your request']",'2','pr')
			
			#Functions.addNotifForPRRequisitioner( self, prref, '  Purchase Order was prepared and now being processed to be served.','','The Purchase Order has been prepared for your request',1,1)

			procUsers = self.user.getProcUsers();
			
			'''
			for x in procUsers:

				self.notif.adNotif(Functions.generateNotifNum(self), '', x[0], '1', ponum, "ARRAY ['3','4','Reference: PR no. "+prref+"','Total Cost: "+str(poTotal)+"','Please validate the approval status of the Purchase Order']",'1','po','')
	   		
			'''

			print("Done Creating PO")

		def createPOFromAbs(self, absNum):
				
				rqDetails = self.reqQ.getRequestDetails(absNum)
				prnum = rqDetails[0][1]
				
				suppIDs = []
				items = []

				supps = self.abc.getWinningSuppliers(absNum)
				
				for x in supps:

					suppDetails = self.sup.getSupllierDetails(x[0])
					suppIDs = suppIDs + suppDetails

				poCounter = self.po.getMaxCounter()
				suppCount = len(suppIDs)


				for y in supps:

					genPONum = Functions.generatePONum(self)
					suppDetails = self.sup.getSupllierDetails(y[0])
					
					rqSuppDetails = self.reqQ.getComTerms(absNum, y[0])


					self.po.addPO(genPONum, y[0], 'procmode', '2017-02-01', 'Mindanao State University', str(rqSuppDetails[0][3]), 'on account', 1000, str(suppDetails[0][3]), prnum)


					suppWinnigItems = self.abc.getSupplierWinningItems(absNum, y[0])
					
					stocknum = 1
					itemAllTotal = 0
					
					for cc in suppWinnigItems:
						
						itemDescrip = self.abc.getDescriptionFromItemNum(absNum, cc[2])
						itemAddDetails = self.abc.getItemTotalCost(absNum, cc[2], y[0])

						toPODescrip = ''

						if cc[6] == '':
							toPODescrip = itemDescrip
						else:
							toPODescrip = cc[6]


						self.po.addItemToPO(genPONum, stocknum, itemAddDetails[1], itemAddDetails[0], toPODescrip, itemAddDetails[2])
						
						itemAllTotal = itemAllTotal + itemAddDetails[3]
						
						stocknum = stocknum + 1

					self.po.updatePOAmount(genPONum, itemAllTotal)
					self.notif.adNotif(Functions.generateNotifNum(self), '', self.kp.getChancellor(), '1', genPONum, "ARRAY ['3','4','Expect a new P.O. to be delivered to youre office in a couple of days','Total Cost: "+str(itemAllTotal)+"','A new Purchase Order has been prepared']",'2','po')
					
					poCounter = poCounter + 1  

				
					procUsers = self.user.getProcUsers();
				
					for x in procUsers:

						self.notif.adNotif(Functions.generateNotifNum(self), '', x[0], '1', genPONum, "ARRAY ['3','4','Reference: PR no. "+prnum+"','PO Num: "+genPONum+"','Please validate the approval status of this Purchase Order']",'1','po')
			
		def validateApprovePO(self, ponum, appPO, fundref, approvalDate, servingDate):
			
			 self.po.approvePO(ponum, appPO, fundref, approvalDate, servingDate)

			 servDateArr = servingDate.split('-')
			 servDate = date(int(servDateArr[0]),int(servDateArr[1]),int(servDateArr[2]))


			 

			 poDetails = self.po.getPODetails(ponum)
			 prRef = poDetails[0][13]
			 reqNum = self.pr.getReqNumFromPR(prRef)
			 reqDetails = self.pr.getPRDetails(reqNum[0][0])
			 print("///=================================================================================================")
			 print(str(servDate)+", "+str(poDetails[0][6]))

			 expDelDate = Functions.workdayadd(self, servDate, poDetails[0][6])
			 expDelDateString = expDelDate.strftime('%Y-%m-%d')

			 self.po.updatePODelDate(ponum, expDelDateString)

			 self.notif.adNotif(Functions.generateNotifNum(self), '', reqDetails[0][4], '1', reqNum[0][0], "ARRAY ['1','1','Reference: PR no. "+reqDetails[0][1]+"','Delivery Date: "+str(approvalDate)+"','Purchase Order was approved and have been served to the supplier']",'2','pr')
			 self.notif.adNotif(Functions.generateNotifNum(self), '', self.kp.getChancellor(), '1', ponum, "ARRAY ['3','4','Approved on: "+str(approvalDate)+"','Date Served: "+str(servingDate)+"','Your approved P.O. was successfully served to the supplier']",'2','po')
					
			 poItems = self.po.getItemByPO(ponum)    
			 poTotal = self.po.getTotalCostofPO(poItems)  

			 smoUser = self.user.getSMOUsers()
			 smoInvenUsers = self.user.getSMOInvenUsers()
			 
			 for x in smoUser:
			 	self.notif.adNotif(Functions.generateNotifNum(self), '', x[0], '1', ponum, "ARRAY ['1','1','P.O. No. "+appPO+"','Expect Del. by: "+str(expDelDate.strftime('%B %d, %Y'))+"','New purchase order was prepared, expect delivery upon up-coming days']",'2','po')
	   		

			 for x in smoInvenUsers:
			 	self.notif.adNotif(Functions.generateNotifNum(self), '', x[0], '1', ponum, "ARRAY ['1','1','P.O. No. "+appPO+"','Total Cost: "+str(poTotal)+"','New P.O. items needed to be profiled according to specific particular']",'1','po')
	   		
			 
			 print('Done Validating')

		def validateDeclinePO(self, ponum, reason):
				pass    

		def addReceive2(self, iarnum, ponum, expdate, asses, invnum, invdate, supplier, receivedate, recOfficer, inspectdate, insOfficer, compltstatus, itemList, rectype):
				
				totalCostOfDelivery = 0
				ponumString = ponum
				
				if rectype == 'true':
					ponumString = ponum +'-n'

				self.ins_2.addIAR(iarnum, ponumString, expdate, asses, invnum, invdate, supplier, inspectdate, insOfficer, receivedate, recOfficer, compltstatus)
				
				saveDestination = None
				prPOTimelineDetails = None

				

				if rectype == 'false':

					poFind  = self.po.isPONumExist(ponum)

					if poFind == False:
						Functions.createPO(self,  ponum, supplier, '', expdate, '', 'NULL', '', 0, '', '', '')

					prNumRef = 	self.pr.getPRNumforPONumForNew(ponum)

					if prNumRef != []:
						prPOTimelineDetails = self.pr.getProCTimeLineDetails(prNumRef[0][0])
						saveDestination = Functions.checkItemSavingDestination(self, prNumRef[0][0])
				
				if rectype == 'true':
					Functions.createPO(self,  ponumString, supplier, '', '', '', 'NULL', '', 0, '', '', '')
				
				stocknum = 1
				
				for x in itemList:
					itemData = itemList[x] 
					
					itemID = self.item_Class.getItemNumfromDescription(itemData['1'])

					if itemID == []:

						itemID = self.item_Class.addItem(itemData['1'], '', '', itemData['2'], itemData['3'], '')

					else:
						itemID = itemID[0][0]

					self.ins_2.addItemToIAR(iarnum, stocknum, itemData['1'], itemData['2'], itemData['4'], itemID, itemData['3'], itemData['5'])

					if saveDestination != 'Supp-Req' or saveDestination != 'Supp-Inven': 
						self.ins_2.addReceiveItems(iarnum, itemData['1'], itemData['4'],itemData['3'], stocknum)

					totalCostOfDelivery = totalCostOfDelivery + (float(itemData['4']) * float(itemData['3']))

					stocknum = stocknum + 1
				

				if prPOTimelineDetails != None:
					
					expDateOfDel_11 = prPOTimelineDetails[0][20]
					expDateOfDel_1 = datetime(expDateOfDel_11.year, expDateOfDel_11.month, expDateOfDel_11.day)
					delDateInterval = expDateOfDel_1 - datetime.now() 
					delDateIntervalDays = int(delDateInterval.days) + 1
					
					ldCost = 0
					
					if delDateIntervalDays < 0:
						ldCost = totalCostOfDelivery * 0.001 * (delDateIntervalDays * -1)
					
						self.ld_Class.addLD(ponum, iarnum, ldCost, (delDateIntervalDays * -1))
					
					else:
						self.ld_Class.addLD(ponum, iarnum, 0, 0)
					
				#======================================================================================================

				
				smoUser = self.user.getSMOUsers()
				smoInvenUsers = self.user.getSMOInvenUsers()

				qtyOfNewItemData = 0
				
				if saveDestination == 'Supp-Inven':
					
					
					iarItems = self.ins_2.getIARItems(iarnum)

					for x in iarItems:
						
						qtyOfNewItemData = qtyOfNewItemData + Functions.addItemToSupply(iarnum, x[3], x[2], x[4], itemIDNumber, '')
						

				if saveDestination == 'Supp-Req': 

					reqRISNum = Functions.generateRISNum(self)

					preqDetails1 = self.pr.getPRDetails(prReqNum[0][0])
					
					self.risClass.addRIS(reqRISNum, preqDetails1[0][2], '', preqDetails1[0][4])
					
					self.risClass.updateRISApproval(reqRISNum, 'TRUE', '')	
					
					self.risClass.setRISNumber(reqRISNum)
					
					iarItemsForRIS = self.ins_2.getIARItems(iarnum)
					
					stocknum = 1
					
					for x in iarItemsForRIS:

						self.risClass.addItemToRIS(reqRISNum, stocknum, x[3], x[2], x[4])
						self.risClass.updateRISApprovedQty(reqRISNum, stocknum, x[4])
						
						stocknum = stocknum + 1
		
		
		def addItemToSupply(self, iarnum, description, unit, quantity, itemid, itemtype):

			itemIDNum = self.supply_Class.getSupplyIDFromDescription(description)
			
			qtyOfNewItemData = 0			

			if itemIDNum is None:
							
				genNum = Functions.generateSupplyNum(self)
							
				itemIDNumber = self.item_Class.getItemNumfromDescription(description)[0][0]

				self.supply_Class.addSupply(genNum, description, '', unit, itemIDNumber , quantity)
				self.supply_Class.updateSupplyQuantity(genNum, quantity)
				self.supply_Class.updateSupplyLatest(iarnum, datetime.now().strftime('%Y-%m-%d'))
							
				qtyOfNewItemData = 1
							
			else:	
							
				supplYDetails = self.supply_Class.getSupplyDetails(itemIDNum)
				self.supply_Class.updateSupplyQuantity(itemIDNum, (float(quantity) + supplYDetails[0][5]))
				self.supply_Class.updateSupplyLatest(iarnum, datetime.now().strftime('%Y-%m-%d'))

				self.supply_Class.updateSupplyAddQuantity(itemIDNum, quantity)

			
			return qtyOfNewItemData


							
		def addReceive(self, iarnum, ponum, podate, reqoff, receiptnum, receiptdate, insdate, insofficer, receivedate, receiveoff, itemList, comArray):
			
			self.ins.addIAR(iarnum, ponum, podate, reqoff, receiptnum, receiptdate, insdate, insofficer, receivedate, receiveoff)

			saveDestination = Functions.checkItemSavingDestination(self, prReqNum[0][0])

			totalCostOfDelivery = 0
			
			if itemList == {}:
				iarItems = self.po.getItemByPO(ponum)
				
				stocknum = 1

				for x in iarItems:
					
					self.ins.addItemToIAR(iarnum, x[1], x[4], x[3], x[2])
					self.ins.addReceiveItems(iarnum, x[4], x[2], x[5], stocknum)

					totalCostOfDelivery = totalCostOfDelivery + (float(x[2]) * float(x[5]))

					stocknum = stocknum + 1
					
			else:
				
				stocknum = 1
				
				for x in itemList:

					itemData = itemList[x] 
					#self.po.addItemToIAR(iarnum, stocknum, itemData['1'], itemData['2'], itemData['4'])
					self.ins.addItemToIAR(iarnum, stocknum, itemData['1'], itemData['2'], itemData['4'])
					self.ins.addReceiveItems(iarnum, itemData['1'], itemData['4'],itemData['3'], stocknum)

					totalCostOfDelivery = totalCostOfDelivery + (float(itemData['4']) * float(itemData['3']))

					stocknum = stocknum + 1

	
			compChecker = True
			
			print('Checking Items completion')
			
			for y in comArray:
				
				data = comArray[y]

				yy = type({})

				if type(data) != yy:
					
					self.ins.setItemCompStatus(iarnum, data, receivedate, y, 0)
				
				else:

					self.ins.setItemCompStatus(iarnum, data['status'], receivedate, y, data['quantity'])

					compChecker = False

		

			self.ins.updateItemComp(iarnum, compChecker, receivedate)
			

			prRef = self.po.getPODetails(ponum)[0][13]
			prReqNum = self.pr.getReqNumFromPR(prRef)
			
			#=============== The New Code =========================================================================
			
			expDateOfDel_11 = self.po.getPODetails(ponum)[0][4]
			expDateOfDel_1 = datetime(expDateOfDel_11.year, expDateOfDel_11.month, expDateOfDel_11.day)
			delDateInterval = (expDateOfDel_1 - datetime.now()) - 1

			
			ldCost = 0
			
			if delDateInterval.days < 0:
				ldCost = totalCostOfDelivery * 0.001 * ((delDateInterval.days * -1))
			
			self.ld_Class.addLD(ponum, iarnum, ldCost, (delDateInterval.days * -1)) 

			#======================================================================================================

			
			
			smoUser = self.user.getSMOUsers()
			smoInvenUsers = self.user.getSMOInvenUsers()

			qtyOfNewItemData = 0
			 
			print("checking Destination,  " + saveDestination)
			
			if saveDestination == 'Supp-Inven':
				
				
				iarItems = self.ins.getIARItems(iarnum)

				for x in iarItems:
					
					
					print(str(iarnum)+"  "+ str(x[1])+"  "+  str(x[4]) +"  "+ str(x[3])+"  "+  str(x[2]))
					#iarnum, x[1], , x[3], x[2]
					
					itemIDNum = self.supply_Class.getSupplyIDFromDescription(x[3])
					

					if itemIDNum is None:
						
						genNum = Functions.generateSupplyNum(self)
						
						itemIDNumber = self.item_Class.getItemNumfromDescription(x[3])[0][0]

						self.supply_Class.addSupply(genNum, x[3], '', x[2], itemIDNumber ,x[4])
						
						qtyOfNewItemData = qtyOfNewItemData + 1
						
					else:	

						self.supply_Class.updateSupplyQuantity(itemIDNum, x[4])	

			if saveDestination == 'Supp-Req': 

				reqRISNum = Functions.generateRISNum(self)

				preqDetails1 = self.pr.getPRDetails(prReqNum[0][0])
				
				self.risClass.addRIS(reqRISNum, preqDetails1[0][2], '', preqDetails1[0][4])
				
				self.risClass.updateRISApproval(reqRISNum, 'TRUE', '')	
				
				self.risClass.setRISNumber(reqRISNum)
				
				iarItemsForRIS = self.ins.getIARItems(iarnum)
				
				stocknum = 1
				
				for x in iarItemsForRIS:

					self.risClass.addItemToRIS(reqRISNum, stocknum, x[3], x[2], x[4])
					self.risClass.updateRISApprovedQty(reqRISNum, stocknum, x[4])
					
					stocknum = stocknum + 1
		

				self.notif.adNotif(Functions.generateNotifNum(self), '', reqoff, '1', reqRISNum, "ARRAY ['4','1','','Click the View Details button and follow the instructions indicated to claim the items','Your requested supplies has arrived, Proceed to the next task to claim the Items']",'1','ris')
			
			if saveDestination == 'Equi-Replace':
				
				for x in smoUser:
			 		self.notif.adNotif(Functions.generateNotifNum(self), '', x[0], '1', iarnum, "ARRAY ['1','1','I.A.R. No. "+iarnum+"','','Newly received Item/s is refered to a P.R. with a purpose indicated as replacement']",'2','iar')
	   	

			if saveDestination == 'Equi-New':
				
				for x in smoUser:
			 		self.notif.adNotif(Functions.generateNotifNum(self), '', x[0], '1', iarnum, "ARRAY ['1','1','I.A.R. No. "+iarnum+"','"+str(qtyOfNewItemData)+" item/s to update','New equipment items was receieved']",'1','iar')
	   		

			for x in smoInvenUsers:
			 	self.notif.adNotif(Functions.generateNotifNum(self), '', x[0], '1', iarnum, "ARRAY ['1','1','I.A.R. No. "+iarnum+"','"+str(qtyOfNewItemData)+" item/s to update','Newly received Items information is in need to be updated']",'1','supply')
	   	
			#self.notif.adNotif(Functions.generateNotifNum(self), '', reqoff, '1', iarnum, "ARRAY ['4','1','','','Your requested items has finally arrived']",'2','pr')
			
			print("DONE")

		def addPAR(self, parnum, byid, bydate, fromid, fromdate, ponum, iarnum, itemsList):
			
			self.propAcc.addPAR(parnum, byid, bydate, fromid, fromdate, ponum, iarnum)

			for x in itemsList:

				itemData = itemsList[x]

				#itemUnit = self.po.getUnitFromDescription(itemData['descrip'], ponum)
				
				invNum = '' 
				assetID = self.ins_2.getAssetIDFromInput(iarnum, x)

				if itemData['invnum'] == '':
					
					for y in range(0, int(itemData['quantity'])):
						
						self.propAcc.addItemToPARWithoutInvNum(parnum, itemData['descrip'], 'unit', itemData['price'], 1, assetID)
						
				else:	
					
					invNum = itemData['invnum']
					
					invAddNum = 0
					
					for y in range(0, int(itemData['quantity'])):
						
						self.propAcc.addItemToPAR(int(invNum) + invAddNum, parnum, itemData['descrip'], 'unit', itemData['price'], 1, assetID)
						invAddNum = invAddNum + 1
					
				
				self.ins.updateAvailableItems(iarnum, itemData['quantity'], x)
				self.ins.updateAvailability(iarnum, x)

			
			self.notif.adNotif(Functions.generateNotifNum(self), '', byid, '1', parnum, "ARRAY ['5','1','P.A.R. no. "+parnum+"','Date Added: "+str(bydate)+"','New items were added into your account']",'2','par','accounts/par/'+parnum.replace('-','_')+'/details/')            
			print("Done")    
		

		def createWMR(self,reqID, parref, insID, items, wmrnum):
			
			reqNum = self.wmrClass.generateWMRID()
			
			self.wmrClass.addWMRReportWithIns(wmrnum, reqID, parref, insID)

			for x in items:

				data = items[x]

				self.wmrClass.addWMRItem(wmrnum, x) #reqNum and InvNum


			return reqNum	

		def getPRStatus_Original(self, reqnum):
			
			outputData = {}

			prDetails = self.pr.getPRDetails(reqnum)

			if prDetails[0][1] == None and prDetails[0][8] == None:
				outputData = {'status':'approval', 'msg':"Waiting for the Chancellor's decision on the approval of the request."}   

			if prDetails[0][7] == False or prDetails[0][8] == False:
				outputData = {'status':'declinedpr', 'msg':"Request was denied due to some reasons."}

			if prDetails[0][7] and prDetails[0][8]:

				prnum = prDetails[0][1]
				
				if prnum == None:
					outputData = {'status':'quotation', 'msg':"P.R. is currently being delivered to the Procuremnt Office for numbering"}
				
				else:
					
					rqnum = self.reqQ.getReqNumFromRefNum(prnum)

					if rqnum == None:
						outputData = {'status':'quotation', 'msg':"A Request for Quotation is currently being prepared regarding your request."}
					
					if rqnum != None:
						
						rqDetails = self.reqQ.getRequestDetails(rqnum)
						absDetails = self.abc.getAbstractDetails(rqnum)

						if absDetails == []:
							
							outputData = {'status':'abstract', 'msg':"Items are being canvassed, Currently waiting for suppliers' reply."}  
						
						else:
							
							if absDetails[0][5] == False:
								
								outputData = {'status':'abstract_sel', 'msg':"Abstract of Canvass is waiting for your selection of your prefered items to be ordered."}  
							
							else:
								
								ponum = self.po.getPONumFromPRRef(prnum)

								if ponum is None:
									outputData = {'status':'po_prep', 'msg':"Purchase Order is currently prepared for your request."}   
								
								else:

									poDetails = self.po.getPODetails(ponum)

									if poDetails[0][16] is None:
										if poDetails[0][9] == False:
											outputData = {'status':'po_deny', 'msg':"Purchase Order was declined for some reasons."}
										else:
											outputData = {'status':'po_read', 'msg':"Purchase Order is currently waiting for approval for it to be served."}    
									else:

										iarnumRef = self.ins.getIARNumFromRef(ponum)
										
										if iarnumRef is None:
											outputData = {'status':'po_serve', 'msg':"Purchase Order has been approved and served. Waiting for your items to be delivered."}

										else:

											parNumRef = self.propAcc.getPARNumFromRef(ponum)
											iarDetails = self.ins.getIARDetails(iarnumRef)
											
											if parNumRef is None:
												
												if iarDetails[0][9] == True:
													outputData = {'status':'iar_delcomp', 'msg':"Requested items has finally delivered. Preparing to be tranfered into accounts."}

												else:
													outputData = {'status':'iar_delmiss', 'msg':"Requested items has finally delivered but not yet complete. Preparing to be tranfered into accounts"}   

											else:
												
												disburstStatus = self.ins.checkIARItemsDisburstComplete(iarnumRef)
												
												if disburstStatus:
													outputData = {'status':'par_comp', 'msg':"Requested items has been completely tranfered into accounts"}   
												
												else:
													outputData = {'status':'par_pend', 'msg':"Transfering requested items into accounts"}      


										
			return outputData 
		
		def getPRStatus(self, reqnum):
			
			outputData = {}

			prDetails = self.pr.getPRDetails(reqnum)
			prLocDetails = self.pr.getPRLocDetails(reqnum)
			prPOTimeline = self.pr.getProCTimeLineDetails(reqnum)
			poNum = prPOTimeline[0][12]
			iarNumList = None
			iarNumListLength = 0

			if poNum != None:
				iarNumList = self.ins_2.getAllIARNumFromRef(poNum)

				if iarNumList != None:
					iarNumListLength = len(iarNumList)

			iarCompltCheck = False

			if iarNumListLength > 1:
				iarCompltCheck = self.ins_2.getDelStatusForMultiIAROfAPO(poNum)

			if iarNumListLength == 1:
				iarDetails = self.ins_2.getIARDetails(iarNumList[0][0])
				iarCompltCheck = iarDetails[0][12]
				
			if iarNumList != None:
				for x in iarNumList:
					iarDetailsOfNum = self.ins_2.getIARDetails(x[0])
			
			if prLocDetails[0][1] == None:
				outputData = {'status':'approval', 'msg':"The Office of V.C.A.F. is waiting for the signed document of this request."}

			if prLocDetails[0][1] == True and (prDetails[0][7] == None or prDetails[0][7] == True )and prLocDetails[0][3] == None:
				outputData = {'status':'approval', 'msg':"Waiting for VCAF's Decission on the request."}

			if prLocDetails[0][1] == True and prDetails[0][7] == False:
				outputData = {'status':'declinedpr', 'msg':"The VCAF had declined this request for some reasons."}
	
			if prLocDetails[0][3] == True and prDetails[0][7] == True and prLocDetails[0][5] == None:
				outputData = {'status':'approval', 'msg':"Document has been sent to the Office of the Chancellor."}
			
			if prLocDetails[0][5] == True and prDetails[0][8] == None:
				outputData = {'status':'approval', 'msg':"Waiting for the Chancellor's Decission on the request."}
			
			if prLocDetails[0][5] == True and prDetails[0][8] == False:
				outputData = {'status':'declinedpr', 'msg':"The Chancellor had declined this request for some reasons."}
			
			if prLocDetails[0][5] == True and prDetails[0][8] == True and prLocDetails[0][7] == None :
				outputData = {'status':'quotation', 'msg':"This purchase request was approved."}
			
			if  prLocDetails[0][7] == True and prLocDetails[0][9] == None and prDetails[0][8] == True and prDetails[0][7] == True:
				outputData = {'status':'quotation', 'msg':"The Approved P.R. was sent to the Procurement Office for numbering"}
			
			if prLocDetails[0][9] == True and prPOTimeline[0][3] == None:
				outputData = {'status':'quotation', 'msg':"Request was successfully numbered and currently being prepared for canvass"}

			if prPOTimeline[0][3] != None and prPOTimeline[0][4] == None:
				outputData = {'status':'quotation', 'msg':"A Request for Quotation was prepared to canvass your requested items."}
			
			if prPOTimeline[0][4] != None and prPOTimeline[0][5] == None:
				outputData = {'status':'quotation', 'msg':"Your requested items are currently being canvassed."}
			
			if prPOTimeline[0][5] != None and prPOTimeline[0][7] == None:
				outputData = {'status':'quotation', 'msg':"Your requested items have been canvassed, an Abstract is currently being prepared."}				
			
			if prPOTimeline[0][9] != None and prPOTimeline[0][10] == None:
				outputData = {'status':'quotation', 'msg':"The Abstract of Canvass has been prepared, expect a document to be delivered to your office."}
			
			if prPOTimeline[0][11] != None and prPOTimeline[0][12] == None:
				outputData = {'status':'po_read', 'msg':"The Procurement Office has received the abstract containing your select bids, a Purchase Order is now being prepared."}
			
			if prPOTimeline[0][13] != None and prPOTimeline[0][15] == None:
				outputData = {'status':'po_read', 'msg':"Purchase Order was prepared and now undergoing checking and approval."}

			if prPOTimeline[0][15] == True and prPOTimeline[0][18] == None:
				outputData = {'status':'po_read', 'msg':"The Purchase Order was approved and now being prepared to be served"}
			
			if prPOTimeline[0][15] == False and prPOTimeline[0][18] == None:
				outputData = {'status':'po_read', 'msg':"The Purchase Order was declined due to some reason rendering the agency to unable to acquire the items."}
			
			if prPOTimeline[0][18] != None and iarNumList == None:
				outputData = {'status':'po_serve', 'msg':"The Purchase Order was served to the receiving supplier, the agency will now wait for the delivery of your items."}
			
			if iarNumList != None and iarCompltCheck == True:
				outputData = {'status':'iar_delcomp', 'msg':"Requested items has finally delivered. Preparing to be tranfered into accounts."}	
			
			if iarNumList != None and iarCompltCheck == False:
				outputData = {'status':'iar_delmiss', 'msg':"Requested items has finally delivered but not yet complete. Preparing to be tranfered into accounts."}	


			'''	
			if prDetails[0][1] == None and prDetails[0][8] == None:
				outputData = {'status':'approval', 'msg':"Waiting for the Approving Officers' decision on the approval of the request."}   

			if prDetails[0][7] == False or prDetails[0][8] == False:
				outputData = {'status':'declinedpr', 'msg':"Request was denied due to some reasons."}

			if prDetails[0][7] and prDetails[0][8]:

				prnum = prDetails[0][1]
				
				if prnum == None:
					outputData = {'status':'quotation', 'msg':"P.R. is currently being delivered to the Procuremnt Office for numbering"}
				
				else:
					
					rqnum = self.reqQ.getReqNumFromRefNum(prnum)

					if rqnum == None:
						outputData = {'status':'quotation', 'msg':"A Request for Quotation is currently being prepared regarding your request."}
					
					if rqnum != None:
						
						rqDetails = self.reqQ.getRequestDetails(rqnum)
						absDetails = self.abc.getAbstractDetails(rqnum)

						if absDetails == []:
							
							outputData = {'status':'abstract', 'msg':"Items are being canvassed, Currently waiting for suppliers' reply."}  
						
						else:
							
							if absDetails[0][5] == False:
								
								outputData = {'status':'abstract_sel', 'msg':"Abstract of Canvass is waiting for your selection of your prefered items to be ordered."}  
							
							else:
								
								ponum = self.po.getPONumFromPRRef(prnum)

								if ponum is None:
									outputData = {'status':'po_prep', 'msg':"Purchase Order is currently prepared for your request."}   
								
								else:

									poDetails = self.po.getPODetails(ponum)

									if poDetails[0][16] is None:
										if poDetails[0][9] == False:
											outputData = {'status':'po_deny', 'msg':"Purchase Order was declined for some reasons."}
										else:
											outputData = {'status':'po_read', 'msg':"Purchase Order is currently waiting for approval for it to be served."}    
									else:

										iarnumRef = self.ins.getIARNumFromRef(ponum)
										
										if iarnumRef is None:
											outputData = {'status':'po_serve', 'msg':"Purchase Order has been approved and served. Waiting for your items to be delivered."}

										else:

											parNumRef = self.propAcc.getPARNumFromRef(ponum)
											iarDetails = self.ins.getIARDetails(iarnumRef)
											
											if parNumRef is None:
												
												if iarDetails[0][9] == True:
													outputData = {'status':'iar_delcomp', 'msg':"Requested items has finally delivered. Preparing to be tranfered into accounts."}

												else:
													outputData = {'status':'iar_delmiss', 'msg':"Requested items has finally delivered but not yet complete. Preparing to be tranfered into accounts"}   

											else:
												
												disburstStatus = self.ins.checkIARItemsDisburstComplete(iarnumRef)
												
												if disburstStatus:
													outputData = {'status':'par_comp', 'msg':"Requested items has been completely tranfered into accounts"}   
												
												else:
													outputData = {'status':'par_pend', 'msg':"Transfering requested items into accounts"}      

							'''
										
			return outputData 

		def generatedPDF(self, template, pdfName):
			
			HTML(template).write_pdf('out.pdf', stylesheets=[CSS(string='@page {size: Legal; margin:35px;}')])

		
		def createUser(self, uname, password, idnum, idExist, lname, fname, mini, rank, desig, office):
			
			acctType = ''
			idnumRef = ''

			if idExist == 'false':
				self.emp.addEmployee(idnum, fname, lname, desig, office, mini, rank, '', '')
				idnumRef = idnum
			else:
				idnumRef = self.user.getIDnumFromName(fname, lname)

			empDetails = self.emp.getEmployeeDetails(idnumRef)
			offDetails = self.offc.getOfficeDetails(empDetails[0][4])

			if idnumRef == offDetails[3]:
				
				if empDetails[0][4] == 'OC':
					acctType = 'chan'
				else:
					acctType = 'head'
						
			else:
				acctType = 'staff'

			acctTypeInt = 0

			if idnumRef == offDetails[3]:
				
				if empDetails[0][4] == 'OC' or empDetails[0][4] == 'PROC' or empDetails[0][4] == 'SMO' or empDetails[0][4] == 'VCAF' or empDetails[0][4] == 'Acctc' or empDetails[0][4] == 'Budget':
					
					acctTypeHeadEqui = {
									'OC': 1,
									'PROC': 2,
									'SMO': 3,
									'VCAF': 1,
									'Acctc': 6,
									'Budget': 6,
									}
					acctTypeInt = acctTypeHeadEqui[empDetails[0][4]]				
				
				else:
					acctTypeInt = 4
						
			else:
				

				if  empDetails[0][4] == 'PROC' or  empDetails[0][4] == 'Acctc' or empDetails[0][4] == 'Budget':
					
					acctTypeHeadEqui = {
									'PROC': 21,
									'Acctc': 61,
									'Budget': 61,
									}

					acctTypeInt = acctTypeHeadEqui[empDetails[0][4]]				
				
				else:
					acctTypeInt = 5

			self.user.addUser(uname, password, idnumRef, acctTypeInt)
			self.user.updateUserStatus(uname, "TRUE") 

			return acctType

		
		def requiSearch(self, reference, idnum): # Find any info from database with the requisitioner's access privelage
			
			outData = []

			loweredInput = inputData.lower()
			inputList = loweredInput.split()

			
			docSearch = Functions.checkIfInputIsToFindDocument(self, inputList) 

			if docSearch[0]:
					
				docType = docSearch[1]
				docNumber = Functions.getDocumentNumber(self, inputList)

				if docType == 'pr':
					
					prData = Functions.findPRforSearch(self, docNumber)

					rqFromRef = self.reqQ.getReqNumFromRefNum(docNumber)
					rqData = Functions.findRQforSearch(self,rqFromRef)

					acData = Functions.findACforSearch(self,rqFromRef)

					poRef = self.po.getPONumFromPRRef(docNumber)
					poData = Functions.findPOforSearch(self,poRef)


					outData = outData + prData + rqData + acData + poData

				if docType == 'po':
					
					poData = Functions.findPOforSearch(self, docNumber)
					iarData = Functions.findIARforSearch(self, '')
					parData = Functions.findPARforSearch(self, '')	
					
					outData = outData + poData + iarData + parData

				if docType == 'rq':
					
					rqData = Functions.findRQforSearch(self, docNumber)
					acData = Functions.findACforSearch(self, docNumber)
					
					outData = outData + rqData + acData
				
				if docType == 'ac':
					rqData = Functions.findACforSearch(self, docNumber)
					outData = outData + rqData	

			else:
				
				fetchDocNumber = Functions.getDocumentNumber(self, inputList)

				prDataN = Functions.findPRforSearch(self, fetchDocNumber)
				poDataN = Functions.findPOforSearch(self, fetchDocNumber)
				rqDataN = Functions.findRQforSearch(self, fetchDocNumber)
				acDataN = Functions.findACforSearch(self, fetchDocNumber)
				parDataN = Functions.findPARforSearch(self, fetchDocNumber)

				compFound = Functions.findSupplierforSearch(self, loweredInput)

				itemsFound = Functions.findItemforSearch(self, loweredInput)
				assetsFound = Functions.findEquipmentforSearch(self, loweredInput)

				outData = prDataN + poDataN + rqDataN + acDataN + iarDataN + parDataN + namesFound + compFound + itemsFound + assetsFound

			return outData


		def generateNotifNum(self):

			notifNum = Functions.generateIDNum(self)

			while self.notif.isNotifNumExist(notifNum):
				notifNum = Functions.generateIDNum(self)

			return notifNum  

		def generateSupplyNum(self):

			notifNum = Functions.generateIDNum(self)

			while self.supply_Class.isItemExist(notifNum):
				notifNum = Functions.generateIDNum(self)

			return notifNum  

		
		def generatePONum(self):

			notifNum = Functions.generateIDNum(self)

			while self.po.isPONumExist(notifNum):
				notifNum = Functions.generateIDNum(self)

			return notifNum  
		
		def generatePRNum(self):

			notifNum = Functions.generateIDNum(self)

			while self.pr.isPRNumExist(notifNum):
				notifNum = Functions.generateIDNum(self)

			return notifNum  

		def generateRISNum(self):

			notifNum = Functions.generateIDNum(self)

			while self.risClass.isRISNumExist(notifNum):
				notifNum = Functions.generateIDNum(self)

			return notifNum  
	

		def generatePONumfromInput(self, counter):

			maxCounter = str(counter).zfill(3)
			year = datetime.now().year
			suffix = float(str(year)[-3:]) if '.' in str(year)[-2:] else int(str(year)[-2:])

			return maxCounter+"-"+str(suffix)




##=============================== Search Algorithm ==================================================================================

		def findInfo(self, inputData):
			
			outData = []

			loweredInput = inputData.lower()
			inputList = loweredInput.split(' ')

			
			docSearch = Functions.checkIfInputIsToFindDocument(self, inputList)
			print(docSearch) 

				
			if docSearch[0]:
					
				docType = docSearch[1]
				docNumber = Functions.getDocumentNumber(self, inputList)
				print("Doc Lang nio")
				print(docNumber)

				if docType == 'pr':
					
					prData = Functions.findPRforSearch(self, docNumber)
					prnum = self.pr.getReqNumFromPR(docNumber)

					rqFromRef = self.reqQ.getReqNumFromRefNum(prnum[0][0])
					
					rqData = Functions.findRQforSearch(self,rqFromRef)

					acData = Functions.findACforSearch(self,rqFromRef)

					poData = [] #Functions.findPOforSearchFromRef(self,docNumber)


					outData = outData + prData + rqData + acData + poData

				

				if docType == 'po':
					
					poData = Functions.findPOforSearch(self, docNumber)
					iarData = Functions.findIARforSearch(self, '')
					parData = Functions.findPARforSearch(self, '')	
					
					outData = outData + poData + iarData + parData

				if docType == 'rq':
					
					rqData = Functions.findRQforSearch(self, docNumber)
					acData = Functions.findACforSearch(self, docNumber)
					
					outData = outData + rqData + acData
				
				if docType == 'ac':
					rqData = Functions.findACforSearch(self, docNumber)
					outData = outData + rqData	

			else:
				
				fetchDocNumber = Functions.getDocumentNumber(self, inputList)
		
				prDataN = Functions.findPRforSearch(self, fetchDocNumber)
			
				poDataN = Functions.findPOforSearch(self, fetchDocNumber)

				rqDataN = Functions.findRQforSearch(self, fetchDocNumber)
				acDataN = Functions.findACforSearch(self, fetchDocNumber)
				
				iarDataN = Functions.findIARforSearch(self, fetchDocNumber)
				parDataN = Functions.findPARforSearch(self, fetchDocNumber)
				risDataN = Functions.findRISforSearch(self, fetchDocNumber)
				

				namesFound = Functions.findNameforSearch(self, loweredInput)
				compFound = Functions.findSupplierforSearch(self, loweredInput)

				itemsFound = Functions.findItemforSearch(self, loweredInput)
				assetsFound = Functions.findEquipmentforSearch(self, loweredInput)
				suppliesFound = Functions.findSupplyforSearch(self, loweredInput)

				outData = prDataN + poDataN + rqDataN + acDataN + iarDataN + parDataN + risDataN + namesFound + compFound + itemsFound + assetsFound +suppliesFound

			if inputData == '':
				return [None,'No',]
			else:
				return outData

		def getDocumentNumber(self, inputData):
				
			docNumber = ''
				
			pattern = re.compile("\d{2,3}-\d{2,3}")
			
			for x in inputData:
				
				if pattern.match(x) is not None and len(x) > 4:
					
					docNumber = x
			

			return docNumber        
					

		def checkIfInputIsToFindDocument(self, inputData):
			

			result = [False,'']
			hits = 0
			hitRef = []

			docKeyReference = [ 'pr',
								'po',
								'rq',
								'ac',
								'par',
								'iar',
								'p.r.',
								'p.o.',
								'r.q.',
								'a.c.',
								'p.a.r.',
								'i.a.r.',
								'request',
								'purchase',
								'order',
								'quotation',
								'abstract',
								'canvass',
								'bids',
								'inspection',
								'acceptance',
								'report',
								'prno.',
								'pono.',
								'rqno.',
								'acno.',
								'parno.',
								'iarno.',
								]


			for x in inputData:
				if x in docKeyReference:
					result[0] = True
					hitRef = hitRef + [x,]
					hits = hits + 1



			if hits == 1:
				
				hitDictfor1 = {
								'pr':'pr',
								'po':'po',
								'rq':'rq',
								'ac':'ac',
								'par':'par',
								'iar':'iar',
								'p.r.':'pr',
								'p.o.':'po',
								'r.q.':'rq',
								'a.c.':'ac',
								'p.a.r.':'par',
								'i.a.r.':'iar',
								'order':'po',
								'quotation':'rq',
								'abstract':'ac',
								'canvass':'ac',
								'bids':'ac',
								'inspection':'iar',
								'acceptance':'iar',
								'prno.':'pr',
								'pono.':'po',
								'rqno.':'rq',
								'acno.':'ac',
								'parno.':'par',
								'iarno.':'iar',
								'p.r.no.':'pr',
								'p.o.no.':'po',
								'r.q.no.':'rq',
								'a.c.no.':'ac',
								'p.a.r.no.':'par',
								'i.a.r.no.':'iar',

				}

				result[1] = hitDictfor1[hitRef[0]]


			else:
				
				if 'request' in hitRef and 'purchase' in hitRef:
				  result[1] = 'pr'
				if 'order' in hitRef and 'purchase' in hitRef:
					result[1] = 'po'
				if 'request' in hitRef and 'quotation' in hitRef:
					result[1] = 'rq'
				if 'abstract' in hitRef and 'canvass' in hitRef or 'bids' in hitRef:
					result[1] = 'ac'
				if 'inspection' in hitRef and 'acceptance' in hitRef or 'report' in hitRef:
					result[1] = 'iar'  
				if 'property' in hitRef and 'acceptance' in hitRef or 'receipt' in hitRef:
					result[1] = 'par'                          

			return result       


		def findPRforSearch(self, inputRef):
			
			result = []

			prResult = self.pr.getReqNumFromPRForSearch(inputRef)

			if prResult != []:
				
				prDetails = Functions.getPRBasicDetails(self, prResult[0][0], '')

				result = [('pr',inputRef, prDetails[0][6], prDetails[1][1], prDetails[1][2], prDetails[0][2], prDetails[2], prDetails[1][0]),]

			return result		
		
		def findPOforSearch(self, inputRef):
			
			result = []

			poRefData = self.po.getPONumFromAppPONum(inputRef)
			
			if poRefData != None:
				
				poData = self.po.getPODetails(poRefData)
				
				#poItems = self.po.getItemByPO(inputRef)
				#poTotal = self.po.getTotalCostofPO(poItems)
				#suppData = self.sup.getSupllierDetails(poData[0][1])


				result = [('po',poData[0][13], '', poData[0][4], '000', inputRef, inputRef.replace('-', '_')),]
			
			return result	


		def findPOforSearchFromRef(self, inputRef):
			
			result = []

			poRefData = self.po.getPONumFromPRRefAll(inputRef)

			for x in poRefData:
				
				poData = self.po.getPODetails(x[0])

				if poData != []:
						
						poItems = self.po.getItemByPO(inputRef)
						poTotal = self.po.getTotalCostofPO(poItems)
						suppData = self.sup.getSupllierDetails(poData[0][1])


						result = result + [('po',poData[0][13], suppData[0][1], poData[0][4], poTotal, inputRef, inputRef.replace('-', '_')),]
					
			return result				

		def findRQforSearch(self, inputRef):
			
			result = []

			reqQDetails = self.reqQ.getRequestDetails(inputRef)
			

			if reqQDetails != []:
				
				prDetails = self.pr.getPRDetails(reqQDetails[0][1])
				suppNum = self.reqQ.getReqComp(inputRef)
				suppList = []

				if suppNum != []:
					for x in suppNum:
						suppData = self.sup.getSupllierDetails(x[1])
						suppList = suppList + [suppData[0],]


				result = [('rq', reqQDetails[0][0], suppList, reqQDetails[0][4], prDetails[0][1], inputRef.replace('-', '_')),]

			return result	
		
		def findRQforSearchFromRef(self, inputRef):
			
			result = []

			reqQDetails = self.reqQ.getRequestDetails(inputRef)

			if reqQDetails != []:
				
				suppNum = len(self.reqQ.getReqComp(inputRef))

				result = [('rq', reqQDetails[0][0], suppNum, reqQDetails[0][4], reqQDetails[0][1], inputRef.replace('-', '_')),]

			return result	
		
		def findACforSearch(self, inputRef):
			
			result = []

			acData = self.abc.getAbstractDetails(inputRef)

			if acData != []:
				result = [('ac', acData[0][2],acData[0][5], inputRef, inputRef.replace('-', '_')),]

			return result
		
		def findPARforSearch(self, inputRef):
			
			result = []

			parData = self.propAcc.getPARDetails(inputRef)

			if parData != []:

				empDetails = self.emp.getEmployeeDetails(parData[0][2])
				offDetails = self.offc.getOfficeDetails(empDetails[0][4])

				result = [('par', [empDetails[0], offDetails], parData[0][5], parData[0][3], inputRef, inputRef.replace('-', '_')),]

			return result

		def findRISforSearch(self, inputRef):
			
			result = []

			risData = self.risClass.getRISDetailsByRISNum(inputRef)
			print("++++++++++++++++++++++++++++")
			print("RIS")
			print(risData)

			if risData != []:

				#empDetails = self.emp.getEmployeeDetails(parData[0][2])
				#offDetails = self.offc.getOfficeDetails(empDetails[0][4])

				result = [('ris', [], '', '', inputRef, inputRef.replace('-', '_')),]

			return result



		def findIARforSearch(self, inputRef):
			
			result = []

			iarData = self.ins_2.getIARDetails(inputRef)

			if iarData != []:
				
				poData = self.po.getPODetails(iarData[0][2])
				#suppData = self.sup.getSupllierDetails(poData[0][1])

				result = [('iar', iarData[0][1], iarData[0][10], '',  iarData[0][10], iarData[0][12], inputRef, [inputRef.replace('-', '_'), (iarData[0][2]).replace('-','_')]),]


			return result

		def findNameforSearch(self, inputRef):
			
			result = []

			foundNames = self.emp.findEmployee(inputRef)

			if foundNames != []:
				
				for x in foundNames:
					
					empDetails = self.emp.getEmployeeDetails(x[0])
					parStatus = Functions.getPARStat(self, x[0])

					result = result + [('name', empDetails[0][1], empDetails[0][2], empDetails[0][3], empDetails[0][4], parStatus[1])]


			foundRepNames = self.sup.findCompRepName(inputRef)

			if foundRepNames != []:
				
				for x in foundRepNames:

					suppDetails = self.sup.getSupllierDetails(x[1])

					result = result + [('supplier', suppDetails[0][1], suppDetails[0][2], suppDetails[0][3], 0)]

			

			return result
		
		def findSupplierforSearch(self, inputRef):
			result = []

			foundSuppliers = self.sup.findCompName(inputRef)

			if foundSuppliers != []:

				for x in foundSuppliers:

					suppDetails = self.sup.getSupllierDetails(x[1])
					
					result = result + [('supplier', suppDetails[0][1], suppDetails[0][2], suppDetails[0][3], 0)]

			return result				
	
		def findItemforSearch(self, inputRef):
			result = []

			itemsFound = self.item_Class.findItem(inputRef)

			if itemsFound != []:
				
				for x in itemsFound:
					itemDetails = self.item_Class.getItemDetails(x[1])

					result = result + [('item', str(itemDetails[0][2]) +" - "+ str(itemDetails[0][1]), itemDetails[0][2], itemDetails[0][3]),]

			return result
		
		'''
		def findEquipmentforSearch(self, inputRef):
			result = []

			itemsFound = self.item_Class.findItem(inputRef)

			if itemsFound != []:
				
				for x in itemsFound:
					itemDetails = self.item_Class.getItemDetails(x[1])
					
					if itemDetails[0][3] == 'Equipment':
						pass
					
					else:
						

					result = result + [('item', str(itemDetails[0][2]) +" - "+ str(itemDetails[0][1]), itemDetails[0][2], itemDetails[0][3]),]

			return result
		'''

		def findSupplyforSearch(self, inputRef):
			result = []

			itemsFound = self.supply_Class.findSupply(inputRef)
			print(itemsFound)

			if itemsFound != []:
				
				for x in itemsFound:
					
					supplyDetails = Functions.getCompleteSupplyDetails(self, x[0])
					suppInfo = (supplyDetails[3][1], supplyDetails[0][5], supplyDetails[1][8])

					result = result + [('supply', str(supplyDetails[0][1]), suppInfo, str(x[0]).replace('-','_')),]

						
			return result
		
		
		def findEquipmentforSearch(self, inputRef):
			result = []

			assetsFound = self.asset_Class.findEquipment(inputRef)

			if assetsFound != []:
				
				for x in assetsFound:
					
					assetDetails = self.asset_Class.getAssetDetails(x[1])
					itemDetails = self.item_Class.getItemDetails(assetDetails[0][1])
					
					searchHeader = ''

					if itemDetails[0][3] == 'equipment':
						searchHeader = 'equi'
					else:
						searchHeader = 'supp'
						


					result = result + [(searchHeader, itemDetails[0][3], assetDetails[0][2], assetDetails[0][3], assetDetails[0][4]),]

			return result	

			
	#=============================================================================================================
		def checkItemSavingDestination(self, inputRef):

			outputData = ''			
			prDetails = self.pr.getPRDetails(inputRef)
			reqIDOff = self.emp.getEmployeeDetails(prDetails[0][4])[0][4]
			purpose = prDetails[0][2].lower()

			print("++==============+++++++==================+++++++++++++")
			print(inputRef)
			print(purpose)

			if prDetails[0][3] == 'Equipment':
				if 'replace' in purpose or 'replacement' in purpose:
						outputData = 'Equi-Replace'
				else:
						outputData = 'Equi-New'

			else:
				
				if ("quarterly" in purpose or "quarter" in purpose) and ("supply" in purpose or "supplies" in purpose and reqIDOff  == 'SMO'):
						outputData = 'Supp-Inven'
				else:
						outputData = 'Supp-Req'


			return outputData			




##===================================  Special Functions ==================================================================================
		
		(MON, TUE, WED, THU, FRI, SAT, SUN) = range(7)

		def workdaysub(self, start_date, end_date, whichdays=(MON,TUE,WED,THU,FRI)):
		    '''
		    Calculate the number of working days between two dates inclusive
		    (start_date <= end_date).
		    The actual working days can be set with the optional whichdays
		parameter
		    (default is MON-FRI)
		    '''
		    delta_days = (end_date - start_date).days + 1
		    full_weeks, extra_days = divmod(delta_days, 7)
		    # num_workdays = how many days/week you work * total # of weeks
		    num_workdays = (full_weeks + 1) * len(whichdays)
		    # subtract out any working days that fall in the 'shortened week'
		    for d in range(1, 8 - extra_days):
		                if (end_date + timedelta(d)).weekday() in whichdays:
		                                num_workdays -= 1
		    return num_workdays
		
		def workdayadd(self, start_date,work_days, whichdays=(MON,TUE,WED,THU,FRI)):
		    '''
		    Adds to a given date a number of working days 
		    2009/12/04 for example is a friday - adding one weekday
		    will return 2209/12/07
		    >>> workdayadd(date(year=2009,month=12,day=4),1) 
		    datetime.date(2009, 12, 7)
		    '''
		    
		    weeks, days = divmod(work_days,len(whichdays))
		    new_date = start_date + timedelta(weeks=weeks)
		    for i in range(days):
		        while new_date.weekday() not in whichdays:
		            new_date += timedelta(days=1)
		    return new_date

#===================================================================================================================

print("Done initializing")
print("System is running")


if __name__ == '__main__':
	f = Functions()

	print(type(f.user))

	#print(f.getCompleteSupplyDetails('MMdB-0748'))
	#print(f.findSupplyforSearch('Folder'))
	#print(f.getItemsByPersonelID('2017-0001'))
	#print(f.getItemsByOffice('CBAA'))
	#=========
	#print(f.getDocumentNumber('00-15'))
	#print(f.getCurrQuarter())
	#print(f.getOfficeComsumptionOfItem('CBAA','IwQd-7977'))
	#dd = f.getAllOfficeComsuptionOfAnItem('IwQd-7977')
	#dd = f.getAllSuppliesWithOfficeInfo('CBAA')
	#for x in dd:
	#	print("============================")
	
	#	print(x)

	#prDetails = self.pr.getPRDetails('nulw-7673')
	#print(f.generateSupplyNum())
	#print('theSavingDes')
	#print(f.checkItemSavingDestination('nulw-7673'))
	#print(self.po.getPODetails('001-17')[0][13])
	#print(prDetails[0][2].lower().split())
	#print(self.sup.getCompIDfromName('1234'))
	#print("the Data " + str(f.findInfo("S")))
	#print("check"+str(f.checkIfInputIsToFindDocument(['yty','ui','op','pr','dfdf'])))
	#print(f.getDocumentNumber(['00111','2222','011-17','12345','dxgdfgdfgd']))
	#print(f.generateSupplyNum())
	#print(f.workdayadd(date(2009, 12, 7),15))
	#prDetails = f.getPRCompleteDetails('gxbH-8973', '')
	#for x in prDetails:
	#	print("----------------------------------")
	#	print(x)
	#prLts = f.getAllPRList()
	#for x in prLts:
	#	print("========================================================")
	#	print("PR Num.:"+ x[0][0])
	#	print("========================================================")
	#	print(x)

