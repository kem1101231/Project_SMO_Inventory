# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$10 31, 16 3:15:50 PM$"

from datetime import datetime
import random
import string
from random import randint

from connectdb import ConnectDB

c = ConnectDB()
connection = c.connection()
cur = connection.cursor()


class Equipment:
    
    
    def addEquipment(self, itemId, description, brand, assetType, assetClass, unit, price):
        idGen = Equipment.generateEquipmentID(self)
        currentdate = datetime.now().strftime('%Y-%m-%d')

        sql = "insert into asset values('"+idGen+"','"+itemId+"','"+description+"', '"+brand+"', '"+assetType+"', '"+assetClass+"', '"+unit+"', "+str(price)+", '"+str(currentdate)+"')"

        cur.execute(sql)
        connection.commit()

        print("Done")

        return idGen

    def getAssetDetails(self, inputRef):

    		sql = "select * from asset where asset_id = '"+inputRef+"'"

    		cur.execute(sql)
    		connection.commit()
    		result = cur.fetchall()

    		return result	
	

    def updateEquipmentPrice(self, itemNum, price, dateOfUpdate):

	    	currentdate = datetime.now().strftime('%Y-%m-%d')
	    	sql = "update asset set price = "+str(price)+", date_of_update = '"+str(currentdate)+"' where asset_id = '"+itemNum+"'"

	    	cur.execute(sql)
	    	connection.commit()
	    	print("Done")


    def findEquipment(self, inputData):
    		sql = "select description, asset_id from asset where lower(description) like lower('%"+inputData+"%') or lower(brand) like lower('%"+inputData+"%')"

    		cur.execute(sql)
    		connection.commit()
    		result = cur.fetchall()

    		return result
	
    def getAssetIDFromBrandAndModel(self, brand, model):
            sql = "select asset_id from asset where description  = '"+model+"' and brand = '"+brand+"'"

            cur.execute(sql)
            connection.commit()

            result = cur.fetchall()

            return result       

    def getEquipmentByParticuar(self, partid):

            sql = "select asset_id from asset where class = '"+partid+"'"

            cur.execute(sql)
            connection.commit()
            result = cur.fetchall()

            return result            

    def getAllEquipment(self):

    		sql = "select asset_id from asset"

    		cur.execute(sql)
    		connection.commit()
    		result = cur.fetchall()

    		return result


    def getAllEquipmentQty(self):

            sql = "select sum(quantity) from inventory"

            cur.execute(sql)
            connection.commit()
            result = cur.fetchone()

            return result[0]
        
    def getAllEquipmentCost(self):

            sql = "select sum(unitprice * quantity) from inventory "

            cur.execute(sql)
            connection.commit()
            result = cur.fetchone()

            return result[0]

    def getAllEquipmentQtyonAcct(self):

            sql = "select sum(quantity) from inventory where status = TRUE"

            cur.execute(sql)
            connection.commit()
            result = cur.fetchone()

            return result[0]
      
    def getAllEquipmentQtyonWaste(self):

            sql = "select sum(quantity) from inventory where status = FALSE"

            cur.execute(sql)
            connection.commit()
            result = cur.fetchone()

            return result[0]
    

    def getAllEquipmentQtyByParticular(self, particularID):

            sql = "select sum(quantity) from inventory"

            cur.execute(sql)
            connection.commit()
            result = cur.fetchone()

            return result[0]
        
    def getAllEquipmentCostByParticular(self):

            sql = "select sum(unitprice * quantity) from inventory "

            cur.execute(sql)
            connection.commit()
            result = cur.fetchone()

            return result[0]

    def getAllEquipmentQtyonAcctByParticular(self):

            sql = "select sum(quantity) from inventory where status = TRUE"

            cur.execute(sql)
            connection.commit()
            result = cur.fetchone()

            return result[0]
      
    def getAllEquipmentQtyonWasteByParticular(self):

            sql = "select sum(quantity) from inventory where status = FALSE"

            cur.execute(sql)
            connection.commit()
            result = cur.fetchone()

            return result[0]
    
    def getAllAssetsByItem(self, itemID):

            sql = "select * from asset where itemid = '"+itemID+"'"

            cur.execute(sql)
            connection.commit()
            result = cur.fetchall()

            return result            
    

    def getAllItemIDs(self):

            sql = "select distinct(itemid) from asset"

            cur.execute(sql)
            connection.commit()
            result = cur.fetchall()

            return result             

    def getAllInvQtyByAssetID(self, assetID):

            sql = "select sum(quantity) from inventory where assetid = '"+assetID+"'"

            cur.execute(sql)
            connection.commit()
            result = cur.fetchone()

            if result[0] is None:
                return 0
            else:
                return result[0]            

    def getAllInv_WQtyByAssetID(self, assetID):

            sql = "select sum(quantity) from inventory_without_invnum where assetid = '"+assetID+"'"

            cur.execute(sql)
            connection.commit()
            result = cur.fetchone()

            if result[0] is None:
                return 0
            else:
                return result[0]    

    def getAllAcctInvQtyByAssetID(self, assetID):

            sql = "select sum(quantity) from inventory where assetid = '"+assetID+"' and status = TRUE "

            cur.execute(sql)
            connection.commit()
            result = cur.fetchone()

            if result[0] is None:
                return 0
            else:
                return result[0]              

    def getAllAcctInv_WQtyByAssetID(self, assetID):

            sql = "select sum(quantity) from inventory_without_invnum where assetid = '"+assetID+"' and status = TRUE "

            cur.execute(sql)
            connection.commit()
            result = cur.fetchone()

            if result[0] is None:
                return 0
            else:
                return result[0]    

    def getAllWasteInvQtyByAssetID(self, assetID):

            sql = "select sum(quantity) from inventory where assetid = '"+assetID+"' and status = FALSE "

            cur.execute(sql)
            connection.commit()
            result = cur.fetchone()

            if result[0] is None:
                return 0
            else:
                return result[0]    

    def getAllWasteInv_WQtyByAssetID(self, assetID):

            sql = "select sum(quantity) from inventory_without_invnum where assetid = '"+assetID+"' and status = FALSE "

            cur.execute(sql)
            connection.commit()
            result = cur.fetchone()

            if result[0] is None:
                return 0
            else:
                return result[0]               

    def generateEquipmentID(self):
	        
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


    def addEquiParticular(self):
        pass


    def getEquiParticulars(self):
        
        sql = "select idname from equip_particulars;"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result
    
    def getAllEquiParticularswithDetails(self):
        
        sql = "select * from equip_particulars except select * from equip_particulars where idname = 'ungroup' order by itemnum ;"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result
    

    def getEquiParticularDetails(self, partID):

        sql = "select * from equip_particulars where idname = '"+partID+"';"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result


        
if __name__ == "__main__":

    print("Hello World")
    print(Equipment().getAllEquipmentQty())
    print(Equipment().getAllInvQtyByAssetID(''))
