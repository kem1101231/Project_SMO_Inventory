 # To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$Dec 21, 2016 11:16:52 PM$"

import random
import string
from random import randint

from datetime import datetime

from connectdb import ConnectDB

c = ConnectDB()
connection = c.connection()
cur = connection.cursor()

class Supply:

    def addSupply(self, compid, description, itemtype, unit, itemid, quantity):
        
        sql = "insert into supply_inventory values ('"+compid+"', '"+description+"', '"+itemtype+"', '"+unit+"', '"+itemid+"', "+str(quantity)+")"
        print(sql)
        cur.execute(sql)
        connection.commit()
        print("Done")    

    def updateSupplyQuantity(self, suppid, quantity):
      
        sql = "update supply_inventory set quantity = (select quantity from supply_inventory where id = '"+suppid+"')- "+str(quantity)+" where  id = '"+suppid+"'"

        cur.execute(sql)
        connection.commit()
        print("Done")    

    def updateSupplyAddQuantity(self, suppid, quantity):
      
        sql = "update supply_inventory set quantity = (select quantity from supply_inventory where id = '"+suppid+"') + "+str(quantity)+" where  id = '"+suppid+"'"

        cur.execute(sql)
        connection.commit()
        print("Done")    
    
    
    def getSupplyIDFromDescription(self, description):
        
        sql = "select id from supply_inventory where description = '"+description+"'"  

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        outData = ''

        if result == []:
            outData = None
        else:
            outData = result[0][0]

        return outData    
        
    def getSupplyDetails(self, compid):
        sql = "select * from supply_inventory where id = '"+compid+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getSupplyInventory(self):
        
        sql = "select * from supply_inventory order by description"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getSupplyQuantityFromItemID(self, itemid):
        
        sql = "select sum(quantity)-(select quantityonrequest from items where itemid = '"+itemid+"')total from supply_inventory where itemid = '"+itemid+"' "

        cur.execute(sql)
        connection.commit()
        result = cur.fetchone()

        print(result)

        if result[0] == None:
            return '0'   
       
        else:
             return result[0]
    

    def isItemExist(self, refData):
        
        sql = "select id from supply_inventory where id = '"+refData+"'"
        print(sql)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        
        print(result)
        
        if result == []:
            return False
        else:
            return True

    def generateSupplyID(self):
        
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
        
        supp = Suppliers()
        #supp.addSupplier('Star Bright Office Depot','Quirino Ave, General Santos City','Katsura Kotarou','123-1234-567','zura@joishishi.com','123-4567')
        print(supp.getCompIDfromName('Star Bright Office Depot'))

        