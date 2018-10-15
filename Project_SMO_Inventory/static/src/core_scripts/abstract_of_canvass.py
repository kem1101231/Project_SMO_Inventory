#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$11 12, 16 7:40:45 PM$"

from connectdb import ConnectDB

c = ConnectDB()
connection = c.connection()
cur = connection.cursor()


class AbstractOfCanvass:
    
    def addAbstract(self, canvassnum, bidnum, dateofquotation, dateopen):
        sql = "insert into abstract_of_canvass values('"+canvassnum+"', '"+bidnum+"', '"+str(dateofquotation)+"', '"+str(dateopen)+"' ,NULL ,FALSE);"

        cur.execute(sql)
        connection.commit()
        print("Done")

    def updateRecomendation(self, canvassnum, recomendation):
        
        sql = "update abstract_of_canvass set recomendation = '"+recomendation+"' where canvassnum = '"+canvassnum+"';"   

        cur.execute(sql)
        connection.commit()
        print("Done")
    
    def setAbstractAsProcessed(self, canvassnum):
        
        sql = "update abstract_of_canvass set sel_approval = TRUE where canvassnum = '"+canvassnum+"';"   

        cur.execute(sql)
        connection.commit()
        print("Done")

    def getAbstractDetails(self, canvassnum):
        
        sql = "select * from abstract_of_canvass where canvassnum = '"+canvassnum+"';"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def addItemToAbstract(self, canvassNum, itemNum, description, unit ,quantity):
        sql = "insert into abstract_of_canvass_items values('"+canvassNum+"', "+str(itemNum)+", '"+description+"', '"+unit+"', "+str(quantity)+")"
        print(sql)
        cur.execute(sql)
        connection.commit()
        print("Done")    

    def addSupplierBid(self, canvassnum, suppID, itemNum):
        sql = "insert into abstract_of_canvass_supplier_price values('"+canvassnum+"', '"+suppID+"', "+str(itemNum)+", 0, 'FALSE')"

        cur.execute(sql)
        connection.commit()
        print("Done")    

    def updateSupplierBid(self, canvassnum, itemNum, unitprice , suppID, bidItemDescrip):
        
        sql = "update abstract_of_canvass_supplier_price set unitprice = "+str(unitprice)+", bid_item_descrip = '"+bidItemDescrip+"' where canvassnum = '"+canvassnum+"' and itemnum = "+str(itemNum)+" and supplier = '"+suppID+"'"

        cur.execute(sql)
        connection.commit()
        print("Done")

    def getAllAbstract(self):
        sql = "select * from abstract_of_canvass order by (canvassnum)DESC"    
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getSupplierBid(self, canvassnum, itemNum, suppID):
        
        sql = "select unitprice from abstract_of_canvass_supplier_price where canvassnum = '"+canvassnum+"' and itemnum = "+str(itemNum)+" and supplier = '"+suppID+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result[0][0]

    def getSupplierSelectionStat(self, canvassnum, itemNum, suppID):
        
        sql = "select sel_approval from abstract_of_canvass_supplier_price where canvassnum = '"+canvassnum+"' and itemnum = "+str(itemNum)+" and supplier = '"+suppID+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result[0][0]


    def getSupplierBidDetails(self, canvassnum,suppID):
        
        sql = "select * from abstract_of_canvass_supplier_price where canvassnum = '"+canvassnum+"' and supplier = '"+suppID+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result      

    def getSupplierItemBid(self, canvassnum, itemNum, suppID):
        
        sql = "select bid_item_descrip from abstract_of_canvass_supplier_price where canvassnum = '"+canvassnum+"' and itemnum = "+str(itemNum)+" and supplier = '"+suppID+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result[0][0]        

        
    def setSelectedBid(self, canvassnum, itemNum, suppID):
        
        sql = "update abstract_of_canvass_supplier_price set sel_approval = 'TRUE' where canvassnum = '"+canvassnum+"' and itemnum = "+str(itemNum)+" and supplier = '"+suppID+"'"

        cur.execute(sql)
        connection.commit()
        print("Done")
    

    def setReasonForSelection(self, canvassnum, itemNum, suppID, reason):
        
        sql = "update abstract_of_canvass_supplier_price set reason = '"+reason+"' where canvassnum = '"+canvassnum+"' and itemnum = "+str(itemNum)+" and supplier = '"+suppID+"'"

        cur.execute(sql)
        connection.commit()
        print("Done")
    

    def getItemNumFromDescription(self, canvassnum, description):
    	sql = "select itemnum from abstract_of_canvass_items where description = '"+description+"' and canvassnum = '"+canvassnum+"';"

    	cur.execute(sql)
    	connection.commit()
    	result = cur.fetchall()

    	return result[0][0]	

    def getDescriptionFromItemNum(self, canvassnum, itemnum):
        
        sql = "select description from abstract_of_canvass_items where itemnum = "+str(itemnum)+" and canvassnum = '"+canvassnum+"';"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result[0][0] 

    def getItemTotalCost(self, canvassnum, itemnum,suppID):
        
        sql = "select abci.unit, abci.quantity, abcc.unitprice, abcc.unitprice * abci.quantity total from abstract_of_canvass_supplier_price abcc, abstract_of_canvass_items abci where abcc.canvassnum = '"+canvassnum+"' and abci.canvassnum = '"+canvassnum+"' and abcc.supplier = '"+suppID+"' and abcc.itemnum  = "+str(itemnum)+" and abci.itemnum = "+str(itemnum)+";"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result[0] 

    def getTotalCostofWinningItems(self, canvassnum, suppID):

        sql = "select sum(distinct(abc_supp.unitprice * abc_it.quantity)) from abstract_of_canvass_supplier_price abc_supp, abstract_of_canvass_items abc_it  where abc_supp.canvassnum ='"+canvassnum+"' and abc_supp.supplier = '"+suppID+"';"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result       

    def getSuppliers(self, canvassnum):

    	sql = "select distinct(supplier) from abstract_of_canvass_supplier_price where canvassnum ='"+canvassnum+"';"

    	cur.execute(sql)
    	connection.commit()
    	result = cur.fetchall()

    	return result

    def getWinningSuppliers(self, canvassnum):
        
        sql = "select distinct(supplier) from abstract_of_canvass_supplier_price where canvassnum ='"+canvassnum+"' and sel_approval = TRUE;"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getSupplierWinningItems(self, canvassnum, suppID):
        
        sql = "select * from abstract_of_canvass_supplier_price where canvassnum ='"+canvassnum+"' and supplier = '"+suppID+"' and sel_approval = TRUE;"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result  
        
    def getAbstractItems(self, canvassnum):

    	sql = "select * from abstract_of_canvass_items where canvassnum ='"+canvassnum+"';"

    	cur.execute(sql)
    	connection.commit()
    	result = cur.fetchall()

    	return result

    def getAbstractItem(self, canvassnum, itemnum):

        sql = "select * from abstract_of_canvass_items where canvassnum ='"+canvassnum+"' and itemnum = "+str(itemnum)+";"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result
    


if __name__ == '__main__':
    abc = AbstractOfCanvass()
    print(abc.getAbstractDetails('001-17'))
    print(abc.getSuppliers('001-17'))	

    print(abc.getTotalCostofWinningItems('010-17', 'DuYh-5412'))