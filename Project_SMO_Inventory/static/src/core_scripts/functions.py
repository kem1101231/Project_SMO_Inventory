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


c = ConnectDB()
connection = c.connection()
cur = connection.cursor()

user = User()
pr = PurchaseRequest()
notif = Notification()
emp = Employees()
kp = KeyPositions()
reqQ = RequestForQuotation()
abc = AbstractOfCanvass()
sup = Suppliers()
po = PurchaseOrder()
ins = InsepectionAndAcceptanceReceipt()
ins_2 = InsepectionAndAcceptanceReceipt_2()
propAcc = PropertyAcceptanceReceipt()
offc = Offices()
item_Class = Items()
asset_Class = Equipment()
risClass = RequisitionAndIssuanceSlip()
supply_Class = Supply()
wmrClass = Waste()
was = WorkAddSub()
ld_Class = LiquidatingDamages()



class Functions:
		
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

			if user.isUserRegistered(uname) == False:
					return "username does not exist"
			else:
					if user.checkUserPass(uname, password):
							userdata = user.getUserDetails(uname)
							currentUser = userdata[0][0]
							return "login complete"
					else:
							return "wrong password"
		
		def createUser(self, idnum, username, password):
			pass
		

'''
============================================================================================================================================			
							Create Functions
============================================================================================================================================
'''
		
		def createPR(self, reqnum, purpose, details, idnum, itemList):

			employeeData = emp.getEmployeeDetails(idnum)

			pr.addPR(reqnum, purpose, details, idnum)
			pr.addPRLoc(reqnum)
			pr.addPRToProc(reqnum)
			
			checkAddNewItemData = False
			qtyOfNewItemData = 0
			
			stocknum = 1
			
			for x in itemList:

				itemData = itemList[x] 
				pr.addItemToPR(reqnum, stocknum, itemData['1'], itemData['2'], itemData['3'],itemData['4'])
				stocknum = stocknum + 1

				itemDataList = item_Class.findItem(itemData['1'])

				if itemData['2'] != " ":
					
					if itemDataList == []:
						
						item_Class.addItem(itemData['1'], '', '', itemData['2'], itemData['3'],'')
						checkAddNewItemData = True
						qtyOfNewItemData = qtyOfNewItemData + 1
					
					item_Class.updateItemCounter(itemData['1'], "prcounter")


			prTotal = pr.getTotalCostofPR(pr.getItemByPR(reqnum))
			prTotalstr = format(prTotal ,"0,.2f")

			notif.adNotif(Functions.generateNotifNum(self), idnum, kp.getVCAFRep(), '1', reqnum, "ARRAY ['3','4','From: "+employeeData[0][4]+"','Total cost: "+prTotalstr+"','A new request was prepared']",'1','pr')

			
			if checkAddNewItemData == True:

				smoAdminUser = offc.getOfficeHeadFromOffice('SMO');
				notif.adNotif(Functions.generateNotifNum(self), idnum, smoAdminUser[0][0], '1', reqnum, "ARRAY ['3','4','"+str(qtyOfNewItemData)+" new item/s','','New Item information was detected that needed to be updated']",'1','item')
	

	# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	







'''
============================================================================================================================================			
							View Details Functions
============================================================================================================================================
'''

'''
============================================================================================================================================			
						
============================================================================================================================================
'''

		def createRIS(self, reqnum, purpose, details, idnum, itemList):

			employeeData = emp.getEmployeeDetails(idnum)

			eFname = employeeData[0][1]
			eSname = employeeData[0][2]

			risClass.addRIS(reqnum, purpose, details, idnum)
			
			stocknum = 1
			
			for x in itemList:

				itemData = itemList[x] 
				risClass.addItemToRIS(reqnum, stocknum, itemData['1'], itemData['2'], itemData['3'])
				stocknum = stocknum + 1

				itemDataList = item_Class.findItem(itemData['1'])

				item_Class.updateItemCounter(itemData['1'], "riscounter")
				item_Class.updateItemQuantityOnRequest(itemData['1'], itemData['3'])


			smoAdminUser = user.getSMOAdminUser();
			
			notif.adNotif(Functions.generateNotifNum(self), idnum, smoAdminUser[0][0], '1', reqnum, "ARRAY ['3','4','From: "+employeeData[0][4]+"','purpose: "+purpose+"','Your have a new R.I.S. waiting for your approval']",'1','ris')
			
		
		def createPRBasic(self, reqnum, purpose, details, idnum, itemList):
			
			employeeData = emp.getEmployeeDetails(idnum)

			eFname = employeeData[0][1]
			eSname = employeeData[0][2]

			pr.addPR(reqnum, purpose, details, idnum)
			
			stocknum = 1
			for x in itemList:

				itemData = itemList[x] 
				pr.addItemToPR(reqnum, stocknum, itemData['1'], itemData['2'], itemData['3'],itemData['4'])
				stocknum = stocknum + 1

			prTotal = pr.getTotalCostofPR(pr.getItemByPR(reqnum))
			prTotalstr = format(prTotal ,"0,.2f")
			
			procUsers = user.getProcUsers();
			
			for x in procUsers:

				notif.adNotif(Functions.generateNotifNum(self), idnum, x[0], '1', reqnum, "ARRAY ['3','4','From: "+employeeData[0][4]+"','Total cost: "+prTotalstr+"','A new Pruchase Request was create and now under consideration for approval']",'1','pr')
			

		def numberPR(self, reqnum):
			
			prnum = pr.generateReqNum()
			
			reqDetails = pr.getPRDetails(reqnum)
			reqid = reqDetails[0][4]

			pr.setPRNumber(reqnum)

			prTotal = pr.getTotalCostofPR(pr.getItemByPR(reqnum))

			notif.adNotif(Functions.generateNotifNum(self), '',reqid, '1', reqnum, "ARRAY ['1','1','','PR Number: "+prnum+"','Your Purchase Request was Approved']",'2','pr')

			procUsers = user.getProcUsers();
			
			for x in procUsers:
				
				if prTotal < 500000:
					notif.adNotif(Functions.generateNotifNum(self), kp.getChancellor(), x[0], '1', reqnum, "ARRAY ['5','1','','PR Number: "+prnum+"','There is a New Approved Purchase Request']",'2','pr')
		
		
		def numberPRFromInput(self, reqnum, inputprnum):
			
			prnum = pr.generateReqNum()
			
			reqDetails = pr.getPRDetails(reqnum)
			reqid = reqDetails[0][4]

			pr.setPRNumberFromInput(reqnum, inputprnum)


			#prTotal = pr.getTotalCostofPR(pr.getItemByPR(reqnum))

			#notif.adNotif(Functions.generateNotifNum(self), '',reqid, '1', reqnum, "ARRAY ['1','1','','PR Number: "+prnum+"','Your Purchase Request was Approved']",'2','pr')
			
			'''
			procUsers = user.getProcUsers();
			
			for x in procUsers:
				
				if prTotal < 500000:
					notif.adNotif(Functions.generateNotifNum(self), kp.getChancellor(), x[0], '1', reqnum, "ARRAY ['5','1','','PR Number: "+prnum+"','There is a New Approved Purchase Request']",'2','pr')
			'''

			print('Done')


		def approveRIS(self, slipnum, itemData):
			
			risDetails = risClass.getRISDetails(slipnum)
			risClass.updateRISApproval(slipnum, 'TRUE', '')	
			risClass.setRISNumber(slipnum)
			
			for x in itemData:
				apprQty = itemData[x]
				risClass.updateRISApprovedQty(slipnum, x, apprQty)

			notif.adNotif(Functions.generateNotifNum(self), '', risDetails[0][4], '1',slipnum, "ARRAY ['1','1','You or your representative may now claim your requested items','View the details and follow the instructions indicated to claim the items','Your RIS was approved.']",'2','ris')	

		def realeaseRIS(self, slipnum, recOfficer):

			risDetails = risClass.getRISDetails(slipnum)
			risClass.releaseRIS(slipnum, recOfficer)
			risItems = risClass.getItemByRIS(slipnum)
			empDetails = emp.getEmployeeDetails(recOfficer)	

			for x in risItems:
				itemIDCode = supply_Class.getSupplyIDFromDescription(x[2])
				supply_Class.updateSupplyQuantity(itemIDCode, x[5])
				item_Class.updateSubtractItemQuantityOnRequest(x[2], x[5])

			notif.adNotif(Functions.generateNotifNum(self), '', risDetails[0][4], '1',slipnum, "ARRAY ['1','1','RIS No. "+risDetails[0][1]+"','Claimed by: "+empDetails[0][2]+ ", "+empDetails[0][1]+"','Your request Items on a RIS has been claimed']",'2','ris')		
			print("Done")

		def approvePR(self, reqnum):
			
			pr.updatePRApproval(reqnum, 'approval_status', 'TRUE', '')
			#pr.addPRToProc(reqnum)
			pr.updatePRApprovalDate(reqnum)

			prTotal = pr.getTotalCostofPR(pr.getItemByPR(reqnum))
			
			##Functions.numberPR(self, reqnum)

			procUsers = user.getProcUsers();
			
		def declinePR(self, reqnum, reason):
			
			reqDetails = pr.getPRDetails(reqnum)
			reqid = reqDetails[0][4]
			
			pr.updatePRApproval(reqnum, 'approval_status', 'FALSE', reason)
			prTotal = pr.getTotalCostofPR(pr.getItemByPR(reqnum))
			prTotalstr = format(prTotal ,"0,.2f")
			
			#notif.adNotif(Functions.generateNotifNum(self), kp.getChancellor(), reqid, '1', reqnum, "ARRAY ['5','3','Total cost: "+prTotalstr+"','Reason: "+reason+"','Your Purchase Request was Declined by the Chancellor']",'2','pr')

		def initApprovePR(self, reqnum):

			reqDetails = pr.getPRDetails(reqnum)
			reqid = reqDetails[0][4]

			employeeData = emp.getEmployeeDetails(reqid)

			eFname = employeeData[0][1]
			eSname = employeeData[0][2]

			pr.updatePRApproval(reqnum, 'init_approval_status', 'TRUE', '')
			prTotal = pr.getTotalCostofPR(pr.getItemByPR(reqnum))
			prTotalstr = format(prTotal ,"0,.2f")
			
			notif.adNotif(Functions.generateNotifNum(self), reqid, kp.getChancellor(), '1', reqnum, "ARRAY ['3','4','From: "+employeeData[0][4]+"','Total cost: "+prTotalstr+"','You have a new Purchase Request']",'1','pr')

		def initDeclinePR(self, reqnum, reason):
			

			reqDetails = pr.getPRDetails(reqnum)
			reqid = reqDetails[0][4]
			
			pr.updatePRApproval(reqnum, 'init_approval_status', 'FALSE', reason)
			prTotal = pr.getTotalCostofPR(pr.getItemByPR(reqnum))
			prTotalstr = format(prTotal ,"0,.2f")
			
			notif.adNotif(Functions.generateNotifNum(self), kp.getVCAF(), reqid, '1', reqnum, "ARRAY ['5','3','Total cost: "+prTotalstr+"','Reason: "+reason+"','Your Purchase Request was Declined by the VCAF']",'2','pr')

		
		def cancelPR(self, reqnum):

			pr.updatePRStatus(reqnum, 'FALSE')

		
		def getPRbyID(self, idnum):
			output = []
			prList = pr.getAllPRbyID(idnum)

			for reqNum in prList:
				prDetails = pr.getPRDetails(reqNum[0])
				prTotal = pr.getTotalCostofPR(pr.getItemByPR(reqNum[0]))
				completeDetails = prDetails[0] + (prTotal,)
				output = output + [completeDetails]

			return output

		def getReqStat(self, idnum):
			
			allPRs = len(pr.getAllPRbyID(idnum))
			approvedPRs = len(pr.getAllApprovedPRbyID(idnum))
			initPendingPRs = len(pr.getAllInitPendingPRbyID(idnum))
			pendingPRs = len(pr.getAllPendingPRbyID(idnum))
			deniedPRs = len(pr.getAllDeclinedPRbyID(idnum))

			return [(allPRs, approvedPRs, initPendingPRs + pendingPRs, deniedPRs),]

		def getPARStat(self, idnum):
			
			allPARTotal = 0
			allPARQuantity = 0
			parList = propAcc.getPAROFID(idnum)

			for x in parList:
				parTotal = propAcc.getPARTotal(propAcc.getPARItems(x[0]))
				parItemTotal = propAcc.getTotalQuantityOfPAR(propAcc.getPARItems(x[0]))

				allPARTotal = allPARTotal + parTotal
				allPARQuantity = allPARQuantity +parItemTotal


			return (len(parList), allPARTotal, allPARQuantity)   
		

		def updateItemData(self, itemid, description, itemClass, unit, price, partID):
				
			item_Class.updateItemInfo(itemid, description, '', itemClass, unit, price, partID)

			prList = pr.getUnclassifiedPRByDescription(description)

			for x in prList:
				pr.updatePRType(x[0], itemClass)


			print("Done")

		def getPRItemsbyID(self, idnum):
			output = []
			prList = pr.getAllPRbyID(idnum)

			for reqNum in prList:
				prItems = pr.getItemByPR(reqNum[0])
				output = output + prItems

			return output    

		def getProcUsers(self):
			pass    
		
		def addReqQuo(self, refnum, projName, projLoc, canvasser, suppliers, itemList):
			

			quotNum = reqQ.generateReqNum()
			reqQ.addRequest(quotNum,refnum, projName, projLoc, canvasser)

			for x in suppliers:

				supplierData = suppliers[x]
				compID = sup.getCompIDfromName(supplierData['1'])
				
				if compID is None:
					
					sup.addSupplier(supplierData['1'], supplierData['2'], supplierData['3'], supplierData['4'], supplierData['5'], '')
					compIDNew = sup.getCompIDfromName(supplierData['1'])
					reqQ.addComToReq(quotNum, compIDNew)
				
				else:
					reqQ.addComToReq(quotNum, compID)
	
			counter = 1
			for x in itemList:
				  itemData = itemList[x]
				  reqQ.addItemToReq(quotNum, counter, itemData['description'], itemData['unit'], itemData['unitprice'], itemData['quantity'])   
				  counter = counter + 1 

		def addAbsCanv(self, quotNum, openingDate, openingTime, bidData):
					  
			reqDetails =  reqQ.getRequestDetails(quotNum)
			reqItems = reqQ.getReqItems(quotNum)
			reqComs = reqQ.getReqComp(quotNum)
		 
			abc.addAbstract(quotNum, quotNum, reqDetails[0][4], openingDate)

			for x in reqItems:

				abc. addItemToAbstract(quotNum, x[1], x[2], x[4], x[3])

			for x in reqComs:
				
				comData = bidData[x[1]]
				
				itemsBids = comData['itemBidList']

				
				warr = comData['warranty']
				deli = comData['delivery']
				vali = comData['validity']

				comprep = comData['namerep']
				reptel = comData['telrep']
				repemail = comData['emailrep']
			   
				reqQ.updateComTerms(quotNum, x[1], warr, deli, vali)
				sup.updateSupplierRepInfo(x[1], comprep, reptel, repemail)
			

				for y in itemsBids:                  
					
					bids = itemsBids[y]

					itemNum = reqQ.getItemNumFromDescription(quotNum, y)

					abc.addSupplierBid(quotNum, x[1], itemNum)

					unitprice = ''
					print('bids '+ str(bids[1]))
					
					if bids[1] == '':
						unitprice = '0'
					else:
						unitprice = bids[1]	

					abc.updateSupplierBid(quotNum, itemNum, unitprice , x[1], bids[0])

			
			preqNum = pr.getReqNumFromPR(reqDetails[0][1])       
			preqDetails = pr.getPRDetails(preqNum[0][0])
					  
			notif.adNotif(Functions.generateNotifNum(self), '', preqDetails[0][4], '1', quotNum, "ARRAY ['3','4','For PR: "+preqDetails[0][1]+"','','You have an Abstract of Canvass to Process']",'1','abstract')
			
			print("Done Creating Abstract of Canvass")

		def updateAbstractBids(self, canvnum, updateData, recomendation):

				for x in updateData:
					abc.setSelectedBid(canvnum, x, updateData[x])

				abc.updateRecomendation(canvnum, recomendation)
				abc.setAbstractAsProcessed(canvnum)
				numOfWinners = len(abc.getWinningSuppliers(canvnum))    
				
				procUsers = user.getProcUsers();
				
				for x in procUsers:

					notif.adNotif(Functions.generateNotifNum(self), '', x[0], '1', canvnum, "ARRAY ['1','1','Abstract No.: "+canvnum+"','Num. of Winner/s: "+str(numOfWinners)+" Bidder/s','Bid winners has been seleted']",'2','abstract')
		   
				print("Update Complete")    
		
		def createPO(self,  ponum, suppID, procmode, deldate, delplace, delterm, payterm, amount, conf, prref, itemList):

			po.addPO(ponum, suppID, procmode, deldate, delplace, delterm, payterm, amount, conf, prref)
			
			stocknum = 1
			for x in itemList:

				itemData = itemList[x] 
				po.addItemToPO(ponum, stocknum, itemData['4'], itemData['2'], itemData['1'], itemData['3'])
				stocknum = stocknum + 1

			
			poItems = po.getItemByPO(ponum)    

			poTotal = po.getTotalCostofPO(poItems)  
			po.updatePOAmount(ponum, poTotal)
	
			reqNum = pr.getReqNumFromPR(prref)
			reqDetails = pr.getPRDetails(reqNum[0][0])

			notif.adNotif(Functions.generateNotifNum(self), '', kp.getChancellor(), '1', ponum, "ARRAY ['3','4','Reference: PR no. "+prref+"','Total Cost: "+str(poTotal)+"','A new Purchase Order has been prepared']",'2','po')
			notif.adNotif(Functions.generateNotifNum(self), '', reqDetails[0][4], '1', reqNum[0][0], "ARRAY ['1','1','Reference: PR no. "+prref+"','Total Cost: "+str(poTotal)+"','The Purchase Order has been prepared for your request']",'2','pr')
			
			procUsers = user.getProcUsers();
			for x in procUsers:

				notif.adNotif(Functions.generateNotifNum(self), '', x[0], '1', ponum, "ARRAY ['3','4','Reference: PR no. "+prref+"','Total Cost: "+str(poTotal)+"','Please validate the approval status of the Purchase Order']",'1','po')
	   		


			print("Done Creating PO")

		def createPOFromAbs(self, absNum):
				
				rqDetails = reqQ.getRequestDetails(absNum)
				prnum = rqDetails[0][1]
				
				suppIDs = []
				items = []

				supps = abc.getWinningSuppliers(absNum)
				
				for x in supps:

					suppDetails = sup.getSupllierDetails(x[0])
					suppIDs = suppIDs + suppDetails

				poCounter = po.getMaxCounter()
				suppCount = len(suppIDs)


				for y in supps:

					genPONum = Functions.generatePONum(self)
					suppDetails = sup.getSupllierDetails(y[0])
					
					rqSuppDetails = reqQ.getComTerms(absNum, y[0])


					po.addPO(genPONum, y[0], 'procmode', '2017-02-01', 'Mindanao State University', str(rqSuppDetails[0][3]), 'on account', 1000, str(suppDetails[0][3]), prnum)


					suppWinnigItems = abc.getSupplierWinningItems(absNum, y[0])
					
					stocknum = 1
					itemAllTotal = 0
					
					for cc in suppWinnigItems:
						
						itemDescrip = abc.getDescriptionFromItemNum(absNum, cc[2])
						itemAddDetails = abc.getItemTotalCost(absNum, cc[2], y[0])

						toPODescrip = ''

						if cc[6] == '':
							toPODescrip = itemDescrip
						else:
							toPODescrip = cc[6]


						po.addItemToPO(genPONum, stocknum, itemAddDetails[1], itemAddDetails[0], toPODescrip, itemAddDetails[2])
						
						itemAllTotal = itemAllTotal + itemAddDetails[3]
						
						stocknum = stocknum + 1

					po.updatePOAmount(genPONum, itemAllTotal)
					notif.adNotif(Functions.generateNotifNum(self), '', kp.getChancellor(), '1', genPONum, "ARRAY ['3','4','Expect a new P.O. to be delivered to youre office in a couple of days','Total Cost: "+str(itemAllTotal)+"','A new Purchase Order has been prepared']",'2','po')
					
					poCounter = poCounter + 1  

				
					procUsers = user.getProcUsers();
				
					for x in procUsers:

						notif.adNotif(Functions.generateNotifNum(self), '', x[0], '1', genPONum, "ARRAY ['3','4','Reference: PR no. "+prnum+"','PO Num: "+genPONum+"','Please validate the approval status of this Purchase Order']",'1','po')
						


		
		def validateApprovePO(self, ponum, appPO, fundref, approvalDate, servingDate):
			
			 po.approvePO(ponum, appPO, fundref, approvalDate, servingDate)

			 servDateArr = servingDate.split('-')
			 servDate = date(int(servDateArr[0]),int(servDateArr[1]),int(servDateArr[2]))


			 

			 poDetails = po.getPODetails(ponum)
			 prRef = poDetails[0][13]
			 reqNum = pr.getReqNumFromPR(prRef)
			 reqDetails = pr.getPRDetails(reqNum[0][0])
			 print("///=================================================================================================")
			 print(str(servDate)+", "+str(poDetails[0][6]))

			 expDelDate = Functions.workdayadd(self, servDate, poDetails[0][6])
			 expDelDateString = expDelDate.strftime('%Y-%m-%d')

			 po.updatePODelDate(ponum, expDelDateString)

			 notif.adNotif(Functions.generateNotifNum(self), '', reqDetails[0][4], '1', reqNum[0][0], "ARRAY ['1','1','Reference: PR no. "+reqDetails[0][1]+"','Delivery Date: "+str(approvalDate)+"','Purchase Order was approved and have been served to the supplier']",'2','pr')
			 notif.adNotif(Functions.generateNotifNum(self), '', kp.getChancellor(), '1', ponum, "ARRAY ['3','4','Approved on: "+str(approvalDate)+"','Date Served: "+str(servingDate)+"','Your approved P.O. was successfully served to the supplier']",'2','po')
					
			 poItems = po.getItemByPO(ponum)    
			 poTotal = po.getTotalCostofPO(poItems)  

			 smoUser = user.getSMOUsers()
			 smoInvenUsers = user.getSMOInvenUsers()
			 
			 for x in smoUser:
			 	notif.adNotif(Functions.generateNotifNum(self), '', x[0], '1', ponum, "ARRAY ['1','1','P.O. No. "+appPO+"','Expect Del. by: "+str(expDelDate.strftime('%B %d, %Y'))+"','New purchase order was prepared, expect delivery upon up-coming days']",'2','po')
	   		

			 for x in smoInvenUsers:
			 	notif.adNotif(Functions.generateNotifNum(self), '', x[0], '1', ponum, "ARRAY ['1','1','P.O. No. "+appPO+"','Total Cost: "+str(poTotal)+"','New P.O. items needed to be profiled according to specific particular']",'1','po')
	   		
			 
			 print('Done Validating')

		def validateDeclinePO(self, ponum, reason):
				pass    

		def addReceive2(self, iarnum, ponum, expdate, asses, invnum, invdate, supplier, receivedate, recOfficer, inspectdate, insOfficer, compltstatus, itemList, rectype):
				
				totalCostOfDelivery = 0
				
				ins_2.addIAR(iarnum, ponum, expdate, asses, invnum, invdate, supplier, inspectdate, insOfficer, receivedate, recOfficer, compltstatus)
				
				saveDestination = None
				prPOTimelineDetails = None

				if rectype == False:

					prNumRef = 	pr.getPRNumforPONumForNew(ponum)
					prPOTimelineDetails = pr.getProCTimeLineDetails(prNumRef[0][0])
					
					saveDestination = Functions.checkItemSavingDestination(self, prNumRef[0][0])
					
				stocknum = 1
				
				for x in itemList:
					itemData = itemList[x] 
					
					itemID = item_Class.getItemNumfromDescription(itemData['1'])

					if itemID == []:

						itemID = item_Class.addItem(itemData['1'], '', '', itemData['2'], itemData['3'], '')

					else:
						itemID = itemID[0][0]

					ins_2.addItemToIAR(iarnum, stocknum, itemData['1'], itemData['2'], itemData['4'], itemID, itemData['3'], itemData['5'])

					if saveDestination != 'Supp-Req' and saveDestination != 'Supp-Inven': 
						ins_2.addReceiveItems(iarnum, itemData['1'], itemData['4'],itemData['3'], stocknum)

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
					
						ld_Class.addLD(ponum, iarnum, ldCost, (delDateIntervalDays * -1))
					
					else:
						ld_Class.addLD(ponum, iarnum, 0, 0)
					
				#======================================================================================================

				
				smoUser = user.getSMOUsers()
				smoInvenUsers = user.getSMOInvenUsers()

				qtyOfNewItemData = 0
				 

				if saveDestination == 'Supp-Inven':
					
					
					iarItems = ins_2.getIARItems(iarnum)

					for x in iarItems:
						
						
						print(str(iarnum)+"  "+ str(x[1])+"  "+  str(x[4]) +"  "+ str(x[3])+"  "+  str(x[2]))
						#iarnum, x[1], , x[3], x[2]
						
						itemIDNum = supply_Class.getSupplyIDFromDescription(x[3])
						

						if itemIDNum is None:
							
							genNum = Functions.generateSupplyNum(self)
							
							itemIDNumber = item_Class.getItemNumfromDescription(x[3])[0][0]

							supply_Class.addSupply(genNum, x[3], '', x[2], itemIDNumber ,x[4])
							
							qtyOfNewItemData = qtyOfNewItemData + 1
							
						else:	

							supply_Class.updateSupplyQuantity(itemIDNum, x[4])	

				if saveDestination == 'Supp-Req': 

					reqRISNum = Functions.generateRISNum(self)

					preqDetails1 = pr.getPRDetails(prReqNum[0][0])
					
					risClass.addRIS(reqRISNum, preqDetails1[0][2], '', preqDetails1[0][4])
					
					risClass.updateRISApproval(reqRISNum, 'TRUE', '')	
					
					risClass.setRISNumber(reqRISNum)
					
					iarItemsForRIS = ins_2.getIARItems(iarnum)
					
					stocknum = 1
					
					for x in iarItemsForRIS:

						risClass.addItemToRIS(reqRISNum, stocknum, x[3], x[2], x[4])
						risClass.updateRISApprovedQty(reqRISNum, stocknum, x[4])
						
						stocknum = stocknum + 1
			


		def addReceive(self, iarnum, ponum, podate, reqoff, receiptnum, receiptdate, insdate, insofficer, receivedate, receiveoff, itemList, comArray):
			
			ins.addIAR(iarnum, ponum, podate, reqoff, receiptnum, receiptdate, insdate, insofficer, receivedate, receiveoff)

			saveDestination = Functions.checkItemSavingDestination(self, prReqNum[0][0])

			totalCostOfDelivery = 0
			
			if itemList == {}:
				iarItems = po.getItemByPO(ponum)
				
				stocknum = 1

				for x in iarItems:
					
					ins.addItemToIAR(iarnum, x[1], x[4], x[3], x[2])
					ins.addReceiveItems(iarnum, x[4], x[2], x[5], stocknum)

					totalCostOfDelivery = totalCostOfDelivery + (float(x[2]) * float(x[5]))

					stocknum = stocknum + 1
					
			else:
				
				stocknum = 1
				
				for x in itemList:

					itemData = itemList[x] 
					#po.addItemToIAR(iarnum, stocknum, itemData['1'], itemData['2'], itemData['4'])
					ins.addItemToIAR(iarnum, stocknum, itemData['1'], itemData['2'], itemData['4'])
					ins.addReceiveItems(iarnum, itemData['1'], itemData['4'],itemData['3'], stocknum)

					totalCostOfDelivery = totalCostOfDelivery + (float(itemData['4']) * float(itemData['3']))

					stocknum = stocknum + 1

	
			compChecker = True
			
			print('Checking Items completion')
			
			for y in comArray:
				
				data = comArray[y]

				yy = type({})

				if type(data) != yy:
					
					ins.setItemCompStatus(iarnum, data, receivedate, y, 0)
				
				else:

					ins.setItemCompStatus(iarnum, data['status'], receivedate, y, data['quantity'])

					compChecker = False

		

			ins.updateItemComp(iarnum, compChecker, receivedate)
			

			prRef = po.getPODetails(ponum)[0][13]
			prReqNum = pr.getReqNumFromPR(prRef)
			
			#=============== The New Code =========================================================================
			
			expDateOfDel_11 = po.getPODetails(ponum)[0][4]
			expDateOfDel_1 = datetime(expDateOfDel_11.year, expDateOfDel_11.month, expDateOfDel_11.day)
			delDateInterval = (expDateOfDel_1 - datetime.now()) - 1

			
			ldCost = 0
			
			if delDateInterval.days < 0:
				ldCost = totalCostOfDelivery * 0.001 * ((delDateInterval.days * -1))
			
			ld_Class.addLD(ponum, iarnum, ldCost, (delDateInterval.days * -1)) 

			#======================================================================================================

			
			
			smoUser = user.getSMOUsers()
			smoInvenUsers = user.getSMOInvenUsers()

			qtyOfNewItemData = 0
			 
			print("checking Destination,  " + saveDestination)
			
			if saveDestination == 'Supp-Inven':
				
				
				iarItems = ins.getIARItems(iarnum)

				for x in iarItems:
					
					
					print(str(iarnum)+"  "+ str(x[1])+"  "+  str(x[4]) +"  "+ str(x[3])+"  "+  str(x[2]))
					#iarnum, x[1], , x[3], x[2]
					
					itemIDNum = supply_Class.getSupplyIDFromDescription(x[3])
					

					if itemIDNum is None:
						
						genNum = Functions.generateSupplyNum(self)
						
						itemIDNumber = item_Class.getItemNumfromDescription(x[3])[0][0]

						supply_Class.addSupply(genNum, x[3], '', x[2], itemIDNumber ,x[4])
						
						qtyOfNewItemData = qtyOfNewItemData + 1
						
					else:	

						supply_Class.updateSupplyQuantity(itemIDNum, x[4])	

			if saveDestination == 'Supp-Req': 

				reqRISNum = Functions.generateRISNum(self)

				preqDetails1 = pr.getPRDetails(prReqNum[0][0])
				
				risClass.addRIS(reqRISNum, preqDetails1[0][2], '', preqDetails1[0][4])
				
				risClass.updateRISApproval(reqRISNum, 'TRUE', '')	
				
				risClass.setRISNumber(reqRISNum)
				
				iarItemsForRIS = ins.getIARItems(iarnum)
				
				stocknum = 1
				
				for x in iarItemsForRIS:

					risClass.addItemToRIS(reqRISNum, stocknum, x[3], x[2], x[4])
					risClass.updateRISApprovedQty(reqRISNum, stocknum, x[4])
					
					stocknum = stocknum + 1
		

				notif.adNotif(Functions.generateNotifNum(self), '', reqoff, '1', reqRISNum, "ARRAY ['4','1','','Click the View Details button and follow the instructions indicated to claim the items','Your requested supplies has arrived, Proceed to the next task to claim the Items']",'1','ris')
			
			if saveDestination == 'Equi-Replace':
				
				for x in smoUser:
			 		notif.adNotif(Functions.generateNotifNum(self), '', x[0], '1', iarnum, "ARRAY ['1','1','I.A.R. No. "+iarnum+"','','Newly received Item/s is refered to a P.R. with a purpose indicated as replacement']",'2','iar')
	   	

			if saveDestination == 'Equi-New':
				
				for x in smoUser:
			 		notif.adNotif(Functions.generateNotifNum(self), '', x[0], '1', iarnum, "ARRAY ['1','1','I.A.R. No. "+iarnum+"','"+str(qtyOfNewItemData)+" item/s to update','New equipment items was receieved']",'1','iar')
	   		

			for x in smoInvenUsers:
			 	notif.adNotif(Functions.generateNotifNum(self), '', x[0], '1', iarnum, "ARRAY ['1','1','I.A.R. No. "+iarnum+"','"+str(qtyOfNewItemData)+" item/s to update','Newly received Items information is in need to be updated']",'1','supply')
	   	
			#notif.adNotif(Functions.generateNotifNum(self), '', reqoff, '1', iarnum, "ARRAY ['4','1','','','Your requested items has finally arrived']",'2','pr')
			
			print("DONE")

	
		def addPAR(self, parnum, byid, bydate, fromid, fromdate, ponum, iarnum, itemsList):
			
			propAcc.addPAR(parnum, byid, bydate, fromid, fromdate, ponum, iarnum)

			for x in itemsList:

				itemData = itemsList[x]

				#itemUnit = po.getUnitFromDescription(itemData['descrip'], ponum)
				
				invNum = '' 
				assetID = ins_2.getAssetIDFromInput(iarnum, x)

				if itemData['invnum'] == '':
					
					for y in range(0, int(itemData['quantity'])):
						
						propAcc.addItemToPARWithoutInvNum(parnum, itemData['descrip'], 'unit', itemData['price'], 1, assetID)
						
				else:	
					
					invNum = itemData['invnum']
					
					invAddNum = 0
					
					for y in range(0, int(itemData['quantity'])):
						
						propAcc.addItemToPAR(int(invNum) + invAddNum, parnum, itemData['descrip'], 'unit', itemData['price'], 1, assetID)
						invAddNum = invAddNum + 1
					
				
				ins.updateAvailableItems(iarnum, itemData['quantity'], x)
				ins.updateAvailability(iarnum, x)

			
			notif.adNotif(Functions.generateNotifNum(self), '', byid, '1', parnum, "ARRAY ['5','1','P.A.R. no. "+parnum+"','Date Added: "+str(bydate)+"','New items were added into your account']",'2','pr')            
			print("Done")    
		

		def createWMR(self,reqID, parref, insID, items, wmrnum):
			
			reqNum = wmrClass.generateWMRID()
			
			wmrClass.addWMRReportWithIns(wmrnum, reqID, parref, insID)

			for x in items:

				data = items[x]

				wmrClass.addWMRItem(wmrnum, x) #reqNum and InvNum


			return reqNum	

		def getPRStatus_Original(self, reqnum):
			
			outputData = {}

			prDetails = pr.getPRDetails(reqnum)

			if prDetails[0][1] == None and prDetails[0][8] == None:
				outputData = {'status':'approval', 'msg':"Waiting for the Chancellor's decision on the approval of the request."}   

			if prDetails[0][7] == False or prDetails[0][8] == False:
				outputData = {'status':'declinedpr', 'msg':"Request was denied due to some reasons."}

			if prDetails[0][7] and prDetails[0][8]:

				prnum = prDetails[0][1]
				
				if prnum == None:
					outputData = {'status':'quotation', 'msg':"P.R. is currently being delivered to the Procuremnt Office for numbering"}
				
				else:
					
					rqnum = reqQ.getReqNumFromRefNum(prnum)

					if rqnum == None:
						outputData = {'status':'quotation', 'msg':"A Request for Quotation is currently being prepared regarding your request."}
					
					if rqnum != None:
						
						rqDetails = reqQ.getRequestDetails(rqnum)
						absDetails = abc.getAbstractDetails(rqnum)

						if absDetails == []:
							
							outputData = {'status':'abstract', 'msg':"Items are being canvassed, Currently waiting for suppliers' reply."}  
						
						else:
							
							if absDetails[0][5] == False:
								
								outputData = {'status':'abstract_sel', 'msg':"Abstract of Canvass is waiting for your selection of your prefered items to be ordered."}  
							
							else:
								
								ponum = po.getPONumFromPRRef(prnum)

								if ponum is None:
									outputData = {'status':'po_prep', 'msg':"Purchase Order is currently prepared for your request."}   
								
								else:

									poDetails = po.getPODetails(ponum)

									if poDetails[0][16] is None:
										if poDetails[0][9] == False:
											outputData = {'status':'po_deny', 'msg':"Purchase Order was declined for some reasons."}
										else:
											outputData = {'status':'po_read', 'msg':"Purchase Order is currently waiting for approval for it to be served."}    
									else:

										iarnumRef = ins.getIARNumFromRef(ponum)
										
										if iarnumRef is None:
											outputData = {'status':'po_serve', 'msg':"Purchase Order has been approved and served. Waiting for your items to be delivered."}

										else:

											parNumRef = propAcc.getPARNumFromRef(ponum)
											iarDetails = ins.getIARDetails(iarnumRef)
											
											if parNumRef is None:
												
												if iarDetails[0][9] == True:
													outputData = {'status':'iar_delcomp', 'msg':"Requested items has finally delivered. Preparing to be tranfered into accounts."}

												else:
													outputData = {'status':'iar_delmiss', 'msg':"Requested items has finally delivered but not yet complete. Preparing to be tranfered into accounts"}   

											else:
												
												disburstStatus = ins.checkIARItemsDisburstComplete(iarnumRef)
												
												if disburstStatus:
													outputData = {'status':'par_comp', 'msg':"Requested items has been completely tranfered into accounts"}   
												
												else:
													outputData = {'status':'par_pend', 'msg':"Transfering requested items into accounts"}      


										
			return outputData 
		
		def getPRStatus(self, reqnum):
			
			outputData = {}

			prDetails = pr.getPRDetails(reqnum)
			prLocDetails = pr.getPRLocDetails(reqnum)
			prPOTimeline = pr.getProCTimeLineDetails(reqnum)
			poNum = prPOTimeline[0][12]
			iarNumList = None
			iarNumListLength = 0

			if poNum != None:
				iarNumList = ins_2.getAllIARNumFromRef(poNum)
				iarNumListLength = len(iarNumList)

			iarCompltCheck = False

			if iarNumListLength > 1:
				iarCompltCheck = ins_2.getDelStatusForMultiIAROfAPO(poNum)

			if iarNumListLength == 1:
				iarDetails = ins_2.getIARDetails(iarNumList[0][0])
				iarCompltCheck = iarDetails[0][12]
				
			if iarNumList != None:
				for x in iarNumList:
					iarDetailsOfNum = ins_2.getIARDetails(x[0])
			
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
					
					rqnum = reqQ.getReqNumFromRefNum(prnum)

					if rqnum == None:
						outputData = {'status':'quotation', 'msg':"A Request for Quotation is currently being prepared regarding your request."}
					
					if rqnum != None:
						
						rqDetails = reqQ.getRequestDetails(rqnum)
						absDetails = abc.getAbstractDetails(rqnum)

						if absDetails == []:
							
							outputData = {'status':'abstract', 'msg':"Items are being canvassed, Currently waiting for suppliers' reply."}  
						
						else:
							
							if absDetails[0][5] == False:
								
								outputData = {'status':'abstract_sel', 'msg':"Abstract of Canvass is waiting for your selection of your prefered items to be ordered."}  
							
							else:
								
								ponum = po.getPONumFromPRRef(prnum)

								if ponum is None:
									outputData = {'status':'po_prep', 'msg':"Purchase Order is currently prepared for your request."}   
								
								else:

									poDetails = po.getPODetails(ponum)

									if poDetails[0][16] is None:
										if poDetails[0][9] == False:
											outputData = {'status':'po_deny', 'msg':"Purchase Order was declined for some reasons."}
										else:
											outputData = {'status':'po_read', 'msg':"Purchase Order is currently waiting for approval for it to be served."}    
									else:

										iarnumRef = ins.getIARNumFromRef(ponum)
										
										if iarnumRef is None:
											outputData = {'status':'po_serve', 'msg':"Purchase Order has been approved and served. Waiting for your items to be delivered."}

										else:

											parNumRef = propAcc.getPARNumFromRef(ponum)
											iarDetails = ins.getIARDetails(iarnumRef)
											
											if parNumRef is None:
												
												if iarDetails[0][9] == True:
													outputData = {'status':'iar_delcomp', 'msg':"Requested items has finally delivered. Preparing to be tranfered into accounts."}

												else:
													outputData = {'status':'iar_delmiss', 'msg':"Requested items has finally delivered but not yet complete. Preparing to be tranfered into accounts"}   

											else:
												
												disburstStatus = ins.checkIARItemsDisburstComplete(iarnumRef)
												
												if disburstStatus:
													outputData = {'status':'par_comp', 'msg':"Requested items has been completely tranfered into accounts"}   
												
												else:
													outputData = {'status':'par_pend', 'msg':"Transfering requested items into accounts"}      

							'''
										
			return outputData 

		def generatedPDF(self, template, pdfName):
			
			HTML(template).write_pdf('out.pdf', stylesheets=[CSS(string='@page {size: Legal; margin:35px;}')])

		
		def createUser(self, uname, password, idnum, idExist, lname, fname, mini, rank, desig, office):
			
			acctType = 0

			if idExist == 'false':
				emp.addEmployee(idnum, fname, lname, desig, office, mini, rank, '', '')
				


			
			empDetails = emp.getEmployeeDetails(idnum)
			offDetails = offc.getOfficeDetails(empDetails[0][4])

			print(idnum)
			print(offDetails)


			if idnum == offDetails[3]:
				acctType = 4

			else:

				acctType = 5

			user.addUser(uname, password, idnum, acctType)
			user.updateUserStatus(uname, "TRUE")

			print(acctType)  

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

					rqFromRef = reqQ.getReqNumFromRefNum(docNumber)
					rqData = Functions.findRQforSearch(self,rqFromRef)

					acData = Functions.findACforSearch(self,rqFromRef)

					poRef = po.getPONumFromPRRef(docNumber)
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

			while notif.isNotifNumExist(notifNum):
				notifNum = Functions.generateIDNum(self)

			return notifNum  

		def generateSupplyNum(self):

			notifNum = Functions.generateIDNum(self)

			while supply_Class.isItemExist(notifNum):
				notifNum = Functions.generateIDNum(self)

			return notifNum  

		
		def generatePONum(self):

			notifNum = Functions.generateIDNum(self)

			while po.isPONumExist(notifNum):
				notifNum = Functions.generateIDNum(self)

			return notifNum  
		
		def generatePRNum(self):

			notifNum = Functions.generateIDNum(self)

			while pr.isPRNumExist(notifNum):
				notifNum = Functions.generateIDNum(self)

			return notifNum  

		def generateRISNum(self):

			notifNum = Functions.generateIDNum(self)

			while risClass.isRISNumExist(notifNum):
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
			inputList = loweredInput.split()

			
			docSearch = Functions.checkIfInputIsToFindDocument(self, inputList) 

			if docSearch[0]:
					
				docType = docSearch[1]
				docNumber = Functions.getDocumentNumber(self, inputList)

				if docType == 'pr':
					
					prData = Functions.findPRforSearch(self, docNumber)

					rqFromRef = reqQ.getReqNumFromRefNum(docNumber)
					rqData = Functions.findRQforSearch(self,rqFromRef)

					acData = Functions.findACforSearch(self,rqFromRef)

					poData = Functions.findPOforSearchFromRef(self,docNumber)


					outData = outData + prData + rqData + acData + poData

					for x in outData:
						print("Data ========================================")
						print(x)

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

				namesFound = Functions.findNameforSearch(self, loweredInput)
				compFound = Functions.findSupplierforSearch(self, loweredInput)

				itemsFound = Functions.findItemforSearch(self, loweredInput)
				assetsFound = Functions.findEquipmentforSearch(self, loweredInput)

				outData = prDataN + poDataN + rqDataN + acDataN + iarDataN + parDataN + namesFound + compFound + itemsFound + assetsFound

			return outData

		def getDocumentNumber(self, inputData):
				
			docNumber = ''
				
			pattern = re.compile("\d{2,3}-\d{2,3}")
			
			for x in inputData:
				if pattern.match(x) is not None and len(x) == 6:
					
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

			prResult = pr.getReqNumFromPRForSearch(inputRef)

			if prResult != []:
				
				itemList = pr.getItemByPR(prResult[0][0])
				prItemTotal = pr.getTotalItemNumofPR(itemList)
				prTotal = pr.getTotalCostofPR(itemList)
				prType = pr.getPRType(prResult[0][0])

				result = [('pr',prResult[0][0], prResult[0][1], prItemTotal, prTotal, inputRef, prType, inputRef.replace('-', '_')),]

			return result		
		
		def findPOforSearch(self, inputRef):
			
			result = []

			poRefData = po.getPONumFromAppPONum(inputRef)
			poData = po.getPODetails(poRefData)

			if poData != []:
				
				poItems = po.getItemByPO(inputRef)
				poTotal = po.getTotalCostofPO(poItems)
				suppData = sup.getSupllierDetails(poData[0][1])


				result = [('po',poData[0][13], suppData[0][1], poData[0][4], poTotal, inputRef, inputRef.replace('-', '_')),]
			
			return result	


		def findPOforSearchFromRef(self, inputRef):
			
			result = []

			poRefData = po.getPONumFromPRRefAll(inputRef)

			for x in poRefData:
				
				poData = po.getPODetails(x[0])

				if poData != []:
						
						poItems = po.getItemByPO(inputRef)
						poTotal = po.getTotalCostofPO(poItems)
						suppData = sup.getSupllierDetails(poData[0][1])


						result = result + [('po',poData[0][13], suppData[0][1], poData[0][4], poTotal, inputRef, inputRef.replace('-', '_')),]
					
			return result				

		def findRQforSearch(self, inputRef):
			
			result = []

			reqQDetails = reqQ.getRequestDetails(inputRef)

			if reqQDetails != []:
				
				suppNum = len(reqQ.getReqComp(inputRef))

				result = [('rq', reqQDetails[0][0], suppNum, reqQDetails[0][4], reqQDetails[0][1], inputRef.replace('-', '_')),]

			return result	
		
		def findRQforSearchFromRef(self, inputRef):
			
			result = []

			reqQDetails = reqQ.getRequestDetails(inputRef)

			if reqQDetails != []:
				
				suppNum = len(reqQ.getReqComp(inputRef))

				result = [('rq', reqQDetails[0][0], suppNum, reqQDetails[0][4], reqQDetails[0][1], inputRef.replace('-', '_')),]

			return result	
		
		def findACforSearch(self, inputRef):
			
			result = []

			acData = abc.getAbstractDetails(inputRef)

			if acData != []:
				result = [('ac', acData[0][2],acData[0][5], inputRef, inputRef.replace('-', '_')),]

			return result
		
		def findPARforSearch(self, inputRef):
			
			result = []

			parData = propAcc.getPARDetails(inputRef)

			if parData != []:
				result = [('par', parData[0][2], parData[0][4], parData[0][1], inputRef, inputRef.replace('-', '_')),]

			return result

		def findIARforSearch(self, inputRef):
			
			result = []

			iarData = ins.getIARDetails(inputRef)

			if iarData != []:
				
				poData = po.getPODetails(iarData[0][1])
				suppData = sup.getSupllierDetails(poData[0][1])

				result = [('iar', iarData[0][1], iarData[0][10], suppData[0][1],  iarData[0][9], iarData[0][6], inputRef, inputRef.replace('-', '_')),]


			return result

		def findNameforSearch(self, inputRef):
			
			result = []

			foundNames = emp.findEmployee(inputRef)

			if foundNames != []:
				
				for x in foundNames:
					
					empDetails = emp.getEmployeeDetails(x[0])
					parStatus = Functions.getPARStat(self, x[0])

					result = result + [('name', empDetails[0][1], empDetails[0][2], empDetails[0][3], empDetails[0][4], parStatus[1])]


			foundRepNames = sup.findCompRepName(inputRef)

			if foundRepNames != []:
				
				for x in foundRepNames:

					suppDetails = sup.getSupllierDetails(x[1])

					result = result + [('supplier', suppDetails[0][1], suppDetails[0][2], suppDetails[0][3], 0)]

			

			return result
		
		def findSupplierforSearch(self, inputRef):
			result = []

			foundSuppliers = sup.findCompName(inputRef)

			if foundSuppliers != []:

				for x in foundSuppliers:

					suppDetails = sup.getSupllierDetails(x[1])
					result = result + [('supplier', suppDetails[0][1], suppDetails[0][2], suppDetails[0][3], 0)]

			return result				
	
		def findItemforSearch(self, inputRef):
			result = []

			itemsFound = item_Class.findItem(inputRef)

			if itemsFound != []:
				
				for x in itemsFound:
					itemDetails = item_Class.getItemDetails(x[1])

					result = result + [('item', str(itemDetails[0][2]) +" - "+ str(itemDetails[0][1]), itemDetails[0][2], itemDetails[0][3]),]

			return result
		
		def findEquipmentforSearch(self, inputRef):
			result = []

			assetsFound = asset_Class.findEquipment(inputRef)

			if assetsFound != []:
				
				for x in assetsFound:
					
					assetDetails = asset_Class.getAssetDetails(x[1])
					itemDetails = item_Class.getItemDetails(assetDetails[0][1])
					
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
			prDetails = pr.getPRDetails(inputRef)
			reqIDOff = emp.getEmployeeDetails(prDetails[0][4])[0][4]
			purpose = prDetails[0][2].lower().split()

			if prDetails[0][3] == 'Equipment':
				if 'replace' in purpose or 'replacement' in purpose:
						outputData = 'Equi-Replace'
				else:
						outputData = 'Equi-New'

			else:

				if ('quarterly' in purpose or 'quarter' in purpose) and ('supply' in purpose or 'supplies' in purpose and reqIDOff  == 'SMO'):
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

if __name__ == '__main__':
	f = Functions()
	#prDetails = pr.getPRDetails('nulw-7673')
	#print(f.generateSupplyNum())
	#print('theSavingDes')
	#print(f.checkItemSavingDestination('nulw-7673'))
	#print(po.getPODetails('001-17')[0][13])
	#print(prDetails[0][2].lower().split())
	#print(sup.getCompIDfromName('1234'))
	#print("the Data " + str(f.findInfo("S")))
	#print("check"+str(f.checkIfInputIsToFindDocument(['yty','ui','op','pr','dfdf'])))
	#print(f.getDocumentNumber(['00111','2222','011-17','12345','dxgdfgdfgd']))
	#print(f.generateSupplyNum())
	print(f.workdayadd(date(2009, 12, 7),15))