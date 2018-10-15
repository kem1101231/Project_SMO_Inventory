#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$11 12, 16 7:40:45 PM$"


import random
import string
from random import randint

from datetime import datetime

from connectdb import ConnectDB

c = ConnectDB()
connection = c.connection()
cur = connection.cursor()


class PurchaseOrder:

	def addPO(self, ponum, suppID, procmode, deldate, delplace, delterm, payterm, amount, conf, prref):

		currentdate = datetime.now().strftime('%Y-%m-%d')
		
		sql = "insert into purchase_order values('"+ponum+"','"+suppID+"','"+str(currentdate)+"', '"+procmode+"', '"+str(deldate)+"', '"+delplace+"', "+delterm+", '"+payterm+"', "+str(amount)+", TRUE, FALSE, FALSE, '"+conf+"', '"+prref+"', NULL)"

		cur.execute(sql)
		connection.commit()
		print("Done")

	def addItemToPO(self, ponum, itemnum, quantity, unit, description, unitcost):

		sql = "insert into purchase_order_items values ('"+ponum+"', "+str(itemnum)+", "+str(quantity)+", '"+unit+"', '"+description+"', "+str(unitcost)+")"

		cur.execute(sql)
		connection.commit()
		print("Done")

	def updatePOAmount(self, ponum, amount):
		
		sql = "update purchase_order set amount = "+str(amount)+" where ponum = '"+ponum+"'"

		cur.execute(sql)
		connection.commit()
		print("Done")
	
	def updatePODelDate(self, ponum, delDate):
		
		sql = "update purchase_order set dateofdelivery = '"+str(delDate)+"' where ponum = '"+ponum+"'"

		cur.execute(sql)
		connection.commit()
		print("Done")
	
	def approvePO(self, ponum, appPO, fundref, approvalDate, serveDate):
		
		counter = PurchaseOrder.getMaxCounter(self) + 1;

		sql = "update purchase_order set poappnum = '"+appPO+"', fundref = '"+fundref+"', approval_date = '"+str(approvalDate)+"', serve_date = '"+str(serveDate)+"', counter = "+str(counter)+" where ponum = '"+ponum+"'"

		cur.execute(sql)
		connection.commit()
		print("Done")
	

	def getAllPO(self):

		sql = "select * from purchase_order order by (ponum)DESC"

		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		return result	



	def getAllApprovedPO(self):

		sql = "select * from purchase_order where poappnum is not NULL order by (poappnum)DESC, (datecreated)DESC"

		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		return result	



	def getPODetails(self, refnum):
		
		sql = "select * from purchase_order where ponum = '"+refnum+"'"

		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		return result

	def getItemByPO(self, reqnum):

		sql = "select *, (unitcost  * quantity)total from purchase_order_items where ponum = '{}';".format(reqnum)
		
		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		return result

	def getPOItemsQuantity(self, reqnum):
		
		sql = "select count(*) from purchase_order_items where ponum = '{}';".format(reqnum)

		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		return result

	def getMaxCounter(self):

		sql = "select max(counter) from purchase_order where date_part('year', datecreated) = date_part('year', CURRENT_DATE)"

		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		if result[0][0] is None:
			return 0
		else:
			return result[0][0]	

	def generatePONum(self):

		counter = PurchaseOrder.getMaxCounter(self) + 1

		maxCounter = str(counter).zfill(3)
		year = datetime.now().year
		suffix = float(str(year)[-3:]) if '.' in str(year)[-2:] else int(str(year)[-2:])

		return maxCounter+"-"+str(suffix)

	def getPONumFromPRRef(self, refNum):
		
		sql = "select ponum from purchase_order where prref = '"+refNum+"'"

		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		if result == []:
			return None
		else:
			return result[0][0]
	
	def getPONumFromPRRefAll(self, refNum):
		
		sql = "select ponum from purchase_order where prref = '"+refNum+"'"

		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		return result

	def getTotalNumOfItemsofPO(self, theItemList):

		totalCost = 0

		for itemDetails in theItemList:

			#itemCost = itemDetails[4]  * itemDetails[5]
			totalCost = totalCost + itemDetails[2]

		return totalCost
	def getTotalCostofPO(self, theItemList):

		totalCost = 0

		for itemDetails in theItemList:

			#itemCost = itemDetails[4]  * itemDetails[5]
			totalCost = totalCost + itemDetails[6]

		return totalCost

	def getUnitFromDescription(self, description, ponum):
		
		sql = "select unit from purchase_order_items where description = '"+description+"' and ponum = '"+ponum+"'"	

		cur.execute(sql)
		connection.commit()

		result = cur.fetchall()

		return result[0][0]

	def getTotalCostofPR(self, theItemList):

		totalCost = 0
		
		for itemDetails in theItemList:

			#itemCost = itemDetails[4]  * itemDetails[5]
			totalCost = totalCost + itemDetails[6]

		return totalCost

	def isPONumExist(self, ref):

		sql = "select ponum from purchase_order where ponum = '"+ref+"'"

		cur.execute(sql)
		connection.commit()
		r = cur.fetchall()

		if r == []:
			return False
		else:
			return True	

	def getPONumFromAppPONum(self, refNum):
		
		sql = "select ponum from purchase_order where poappnum = '"+refNum+"';"	

		cur.execute(sql)
		connection.commit()

		result = cur.fetchall()

		return result[0][0]
	

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



if __name__ == "__main__":
    print (PurchaseOrder().getMaxCounter());
    poDetails = PurchaseOrder().getPODetails('001-17')
    #print(poDetails[0][16])
    print(PurchaseOrder().getPONumFromAppPONum('001-17'))
