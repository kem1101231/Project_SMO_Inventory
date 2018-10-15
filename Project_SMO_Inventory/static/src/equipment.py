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
from db_structure import dbTable

c = ConnectDB()
connection = c.connection()
cur = connection.cursor()

dbClass = None

class Equipment:

    def __init__(self):
        
        dbClass = dbTable('asset')
        
        dbClass.column('asset_id','character varying(10)',True)
        dbClass.column('itemid','character varying(15)',False)
        dbClass.column('description','character varying(250)',False)
        dbClass.column('brand','character varying(150)',False)
        dbClass.column('type','character varying(80)',False)
        dbClass.column('class','character varying(80)',False)
        dbClass.column('unit','character varying(50)',False)
        dbClass.column('unit_price','double precision',False)
        dbClass.column('date_of_update','date',False)

        #==========================================================

        dbClassInv = dbTable('inventory')

        dbClassInv.column('invnum','integer', True)
        dbClassInv.column('parnum','character varying(25)', False)
        dbClassInv.column('description','character varying(255)', False)
        dbClassInv.column('unit','character varying(50)', False)
        dbClassInv.column('unitprice','double precision', False)
        dbClassInv.column('quantity','double precision', False)
        dbClassInv.column('status','boolean', False)
        dbClassInv.column('assetid','character varying(10)', False)
        dbClassInv.column('serialnum','character varying(50)', False)
        dbClassInv.column('iarnum','character varying(15)', False)


        #==========================================================

        dbClassInvW = dbTable('inventory_without_invnum')

        dbClassInvW.column('invnum','integer', True)
        dbClassInvW.column('parnum','character varying(25)', False)
        dbClassInvW.column('description','character varying(255)', False)
        dbClassInvW.column('unit','character varying(50)', False)
        dbClassInvW.column('unitprice','double precision', False)
        dbClassInvW.column('quantity','double precision', False)
        dbClassInvW.column('status','boolean', False)
        dbClassInvW.column('assetid','character varying(10)', False)
        dbClassInvW.column('serialnum','character varying(50)', False)
        dbClassInvW.column('iarnum','character varying(15)', False)

        #==========================================================

        dbClassEquiP = dbTable('equip_particulars')

        dbClassEquiP.column('idname','character varying(15)', True)
        dbClassEquiP.column('name','character varying(255)', False)
        dbClassEquiP.column('subhead','character varying(15)', False)
        dbClassEquiP.column('itemnum','character varying(10)', False)
    
    
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
   
    def findEquipmentFromInventory(self, inputData):
            sql = "select invnum, assetid from inventory where lower(description) like lower('%"+inputData+"%')"

            cur.execute(sql)
            connection.commit()
            result = cur.fetchall()

            return result
    
    def findEquipmentFromInventoryWithoutNum(self, inputData):
            sql = "select invnum, assetid from inventory_without_invnum where lower(description) like lower('%"+inputData+"%') "

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


    def addEquiParticular(self, idname, name, subhead, itemnum):
        sql = "insert into equip_particulars values('"+idname+"','"+name+"','"+subhead+"',"+itemnum+")"

        cur.execute(sql)
        connection.commit()        


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

#===========================================================================
#New Inventory Table Codes



    def getAllEquiList(self):
        sql = "select distinct(description),unit, unitprice, assetid, (select count(description) from inventory)quantity from inventory"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getAllEquiListbyPARNum(self, parNum):
        
        sql = "select distinct(description), unit, unitprice, assetid,  (select count(description)  from inventory where description = i.description and parnum = '"+parNum+"' group by description)quantity,(select count(description)  from inventory where description = i.description and parnum = '"+parNum+"' group by description)*unitprice  from inventory i  where parnum = '"+parNum+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getAllEquiNoNumListbyPARNum(self, parNum):
        
        sql = "select distinct(description), unit, unitprice, assetid,  (select count(description)  from inventory_without_invnum where description = i.description and parnum = '"+parNum+"' group by description)quantity,(select count(description)  from inventory_without_invnum where description = i.description and parnum = '"+parNum+"' group by description)*unitprice  from inventory_without_invnum i  where parnum = '"+parNum+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result


    def getEquiIndiDetailsby(self, description):
        
        sql = "select invnum, status, serialnum from inventory where description = '"+description+"'"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getEquiIndiDetailsbyPARNum(self, description, parNum):
        
        sql = "select invnum, status, serialnum, unitprice  from inventory where description = '"+description+"' and parnum = '"+parNum+"'"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result
    
    def getEquiIndiDetailsNoNumbyPARNum(self, description, parNum):
        
        sql = "select invnum, status, serialnum, unitprice ,'no' from inventory_without_invnum where description = '"+description+"' and parnum = '"+parNum+"'"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getMaxPriceOfItemFromInv(self, assetid):
        sql = "select unitprice from inventory  where assetid = '"+assetid+"'  order by unitprice limit 1"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getMaxPriceOfItemFromInvWithoutNum(self, assetid):
        sql = "select unitprice from inventory_without_invnum  where assetid = '"+assetid+"'  order by unitprice limit 1"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result    

if __name__ == "__main__":

    #print("Hello World")
    #print(Equipment().getAllEquipmentQty())
    #print(Equipment().getAllInvQtyByAssetID(''))
    print(Equipment().getAllEquiList())
    print(Equipment().getAllEquiListbyPARNum('001-18'))
