
import random
import string
from random import randint
from datetime import datetime

from connectdb import ConnectDB
from db_structure import dbTable

c = ConnectDB()
connection = c.connection()
cur = connection.cursor()

dbClass = None

class Items:

	def __init__(self):
		
		dbClass = dbTable('items')
		
		dbClass.column('itemid','character varying(10)', True)
		dbClass.column('description','character varying(255)', False)
		dbClass.column('type','character varying(15)', False)
		dbClass.column('class','character varying(15)', False)
		dbClass.column('unit','character varying(10)', False)
		dbClass.column('price','double precision', False)
		dbClass.column('prcounter','integer', False)
		dbClass.column('riscounter','integer', False)
		dbClass.column('quantityonrequest','double precision', False)
		dbClass.column('category','character varying(10)', False)

	
	def addItem(self, description, itemType, itemClass, unit, price, catergory):
		
		idGen = Items.generateItemID(self)

		sql = "insert into items values('"+idGen+"','"+description+"', '"+itemType+"', '"+itemClass+"', '"+unit+"', "+str(price)+",0 ,0, 0, '"+catergory+"')"

		cur.execute(sql)
		connection.commit()
		print("Done")

		return idGen

	def updateItemInfo(self, itemid, description, itemType, itemClass, unit, price, category):
		
		sql = "update items set  description = '"+description+"', type = '"+itemType+"', class = '"+itemClass+"', unit ='"+unit+"', price = "+str(price)+", category = '"+category+"' where itemid = '"+itemid+"';"

		cur.execute(sql)
		connection.commit()
		print("Done")

	def updatePrice(self, itemNum, price):
		
		sql = "update items set price = "+str(price)+" where itemid = '"+itemNum+"'"

		cur.execute(sql)
		connection.commit()
		print("Done")


	def updateItemCounter(self, description, counterType):
		
		
		sql = "update items set "+counterType+" = (select "+counterType+" from items where description = '"+description+"') + 1 where description = '"+description+"'"

		cur.execute(sql)
		connection.commit()
		
		print("Done")

	def updateItemQuantityOnRequest(self, description, qtytoadd):
		
		
		sql = "update items set quantityonrequest = (select quantityonrequest from items where description = '"+description+"') + "+str(qtytoadd)+" where description = '"+description+"'"

		cur.execute(sql)
		connection.commit()
		
		print("Done")
	
	def updateSubtractItemQuantityOnRequest(self, description, qtytoadd):
		
		
		sql = "update items set quantityonrequest = (select quantityonrequest from items where description = '"+description+"') - "+str(qtytoadd)+" where description = '"+description+"'"

		cur.execute(sql)
		connection.commit()
		
		print("Done")
	

	def getItemDetails(self, itemID):
		
		sql = "select * from items where itemid = '"+itemID+"'"

		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		return result

	def getItemNumfromDescription(self, inputData):
		
		sql = "select itemid from items where description = '"+inputData+"'"

		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		return result	

	def findItem(self, inputData):
		
		sql = "select description, itemid from items where lower(description) like lower('%"+inputData+"%')"

		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		return result

	def findSupplyItem(self, inputData):
		
		sql = "select description, itemid from items where lower(description) like lower('%"+inputData+"%') and class = 'Supply'"

		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		return result


	def getAllItems(self):
		
		sql = "select itemid from items order by class, description;"

		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		return result

	def getAllSupplyItems(self):
		
		sql = "select itemid from items where class = 'Supply'"

		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		return result	
	


	def getAllSupplyItemsSorted(self):
		
		sql = "select itemid from items where class = 'Supply' order by (prcounter + riscounter)desc"

		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		return result	
	
	def getAllSupplyItemsSortedwithDetails(self):
		
		sql = "select * from items where class = 'Supply' order by (prcounter + riscounter)desc"

		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		return result				

	def getAllItemsWithDetails(self):
		
		sql = "select * from items order by class, description"

		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		return result	

	def getAllItemsWithDetailsByClass(self, classRef):
		
		sql = "select * from items where category = '"+classRef+"' order by description"

		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		return result		

	def getAllEquipmentItemsWithDetails(self):
		
		sql = "select * from items where class = 'Equipment' or class = ''"

		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		return result		


	def isIDExist(self, idref):
		
		sql = "select itemid from items where itemid = '"+idref+"'"
		
		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()

		if result == []:
			return False
		else:
			return True

	def generateItemID(self):
		output = ''

		check = True

		while check:
			
			output = Items.generateItemIDString(self)
			check = Items.isIDExist(self, output)
	
		return output			


	def generateItemIDString(self):
        
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

if __name__ == '__main__':
	
	Items()