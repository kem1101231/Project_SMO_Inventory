# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$Dec 21, 2016 11:16:52 PM$"

import random
import string
from random import randint

from time import gmtime, strftime
from datetime import datetime

from connectdb import ConnectDB
from db_structure import dbTable

c = ConnectDB()
connection = c.connection()
cur = connection.cursor()
currentdate = datetime.now().strftime('%Y-%m-%d')

dbClass = None

class PropertyAcceptanceReceipt:

    def __init__(self):
       
        dbClass = dbTable('property_acc_receipt')

        dbClass.column('parnum','character varying(15)', True)
        dbClass.column('dateofpar','date',False)
        dbClass.column('receiveby','character varying(25)',False)
        dbClass.column('datereceiveby','date',False)
        dbClass.column('receivefrom','character varying(25)',False)
        dbClass.column('datereceivefrom','date',False)
        dbClass.column('ponum','character varying(15)',False)
        dbClass.column('counter','integer',False)
        dbClass.column('partype','character varying(15)',False)
        dbClass.column('iarnumref','character varying(15)',False)





    def addPAR(self, parnum, byid, bydate, fromid, fromdate, ponum, iarnum):
        
        counter = PropertyAcceptanceReceipt.getMaxCounter(self) + 1

        sql = "insert into property_acc_receipt values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}')".format(parnum, bydate, byid, fromdate, fromid, currentdate, ponum, counter, iarnum)

        cur.execute(sql)
        connection.commit()
        print("Done")   

    def updatePARType(self, parnum, typeInput):
        sql = "update property_acc_receipt set partype = '"+typeInput+"' where parnum = '"+parnum+"'"

        cur.execute(sql)
        connection.commit()
        print("Done") 

    def updateSerialID(self, invnum, inputdata):
        sql = "update inventory set serialnum = '"+inputdata+"' where invnum = '"+invnum+"'" 

        cur.execute(sql)
        connection.commit()
        
    def tranferPAR(self, invnum, inputdata):
        
        sql = "update property_acc_receipt set receiveby = '"+inputdata+"', datereceiveby = '"+str(currentdate)+"' where parnum = '"+invnum+"'" 

        cur.execute(sql)
        connection.commit()
        

    def addItemToPAR(self, invnum, parnum, descrip, unit, price, quan, assetid):

        toSQL = str(0)
        
        if invnum != '':
            toSQL = str(invnum)

        sql = "insert into inventory values ("+toSQL+", '"+parnum+"', '"+descrip+"', '"+unit+"', "+str(price)+", "+str(quan)+", TRUE, '"+assetid+"')"

        cur.execute(sql)
        connection.commit()
        print("Done")    

    def addItemToPARWithoutInvNum(self, parnum, descrip, unit, price, quan, assetid):

        counter = PropertyAcceptanceReceipt.getMaxCounterOnInvWithoutInvNum(self) + 1

        sql = "insert into inventory_without_invnum values ("+str(counter)+", '"+parnum+"', '"+descrip+"', '"+unit+"', "+str(price)+", "+str(quan)+", TRUE, '"+assetid+"')"

        cur.execute(sql)
        connection.commit()
        print("Done")    
    

    def getPARDetails(self, parnum):
        
        sql = "select * from property_acc_receipt where parnum = '"+parnum+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getPARItems(self, parnum):
        
        sql = "select *, (unitprice*quantity)total from inventory where parnum = '"+parnum+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result
    
    def getPARItemsOnAcct(self, parnum):
        
        sql = "select distinct* from inventory where parnum = '"+parnum+"' and status = TRUE"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result
    
    def getPARItemsOnAcctfromInvNoNum(self, parnum):
        
        sql = "select *, (unitprice*quantity)total from inventory_without_invnum where parnum = '"+parnum+"' and status = TRUE"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result    
    def getPARItemsNotOnAcct(self, parnum):
        
        sql = "select *, (unitprice*quantity)total from inventory where parnum = '"+parnum+"' and status = FALSE"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getAllPAR(self):
        
        sql = "select * from property_acc_receipt order by (parnum)desc"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getPARItemsFromNoInvNum(self, parnum):
        
        sql = "select *, (unitprice*quantity)total from inventory_without_invnum where parnum = '"+parnum+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result    

    def getPAROFID(self, byid):
        
        sql = "select parnum from property_acc_receipt where receiveby = '"+byid+"' order by (parnum)DESC"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getInvenItemByAssetID(self, assetid, parnum):
        
        sql = "select i.*, p.dateofpar ,p.receiveby, p.datereceiveby, 'with' from inventory i,property_acc_receipt p where i.assetid = '"+assetid+"' and p.parnum = '"+parnum+"' and i.parnum = '"+parnum+"'"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getInvenWithOutNumItemByAssetID(self, assetid, parnum):
        
        sql =  "select i.*, p.dateofpar ,p.receiveby, p.datereceiveby,'no'  from inventory_without_invnum i,property_acc_receipt p where i.assetid = '"+assetid+"' and p.parnum = '"+parnum+"' and i.parnum = '"+parnum+"'"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result
    
    def getTotalQuantityOfPAR(self, itemList):
        
        total = 0
        
        if itemList != []:
            for x in itemList:
                total = total + x[5]

        return total    

    def getPARTotal(self, itemList):
        
        total = 0
        for x in itemList:
            total = total + x[10]

        return total    
    
    def getPARItemAmountTotal(self, parnum):
        
        sql = "select sum(unitprice * quantity) from inventory where parnum = '"+parnum+"' and status = TRUE"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result 

    def getMaxCounter(self):
        
        sql = "select max(counter) from property_acc_receipt where date_part('year', dateofpar) = date_part('year', CURRENT_DATE)" 

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall() 
        
        if result[0][0] is None:
            return 0
            
        else:
            return result[0][0]
            



    def getMaxCounterOnInvWithoutInvNum(self):
        
        sql = "select max(invnum) from inventory_without_invnum" 

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall() 
        
        if result[0][0] is None:
            return 0
        else:
            return result[0][0]


    def getPARNumFromRef(self, refNum):
        
        sql = "select parnum from property_acc_receipt where ponum = '"+refNum+"'" 

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall() 
        
        if result == []:
            return None
        else:
            return result[0][0]


    def getInventoryItemByInvNum(self, invNum):
        
        sql = "select * from inventory where invnum = "+str(invNum)+"" 

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall() 
        
        if result == []:
            return None
        else:
            return result[0]

    def generateRecNum(self):
        
        counter = PropertyAcceptanceReceipt.getMaxCounter(self) + 1

        maxCounter = str(counter).zfill(3)
        year = datetime.now().year
        suffix = float(str(year)[-3:]) if '.' in str(year)[-2:] else int(str(year)[-2:])
        
        return maxCounter+"-"+str(suffix)



if __name__ == '__main__':
        
        prop = PropertyAcceptanceReceipt()

        print(prop.getPAROFID('byid'))
        #supp = Suppliers()
        #supp.addSupplier('Star Bright Office Depot','Quirino Ave, General Santos City','Katsura Kotarou','123-1234-567','zura@joishishi.com','123-4567')
        #print(supp.getCompIDfromName('Star Bright Office Depot'))

        