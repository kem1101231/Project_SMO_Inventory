#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$11 12, 16 7:26:30 PM$"

from datetime import datetime

from connectdb import ConnectDB
from purchase_request import PurchaseRequest
from db_structure import dbTable


c = ConnectDB()
connection = c.connection()
cur = connection.cursor()

preq = PurchaseRequest()
dbClass = None


class RequestForQuotation:

    def __init__(self):
        
        dbClass = dbTable('req_for_quotation')
   
        dbClass.column('quotationnum','character varying(15)', True)
        dbClass.column('refnum','character varying(50)', False)
        dbClass.column('projname','character varying(255)', False)
        dbClass.column('projlocation','character varying(255)', False)
        dbClass.column('datecreated','date', False)
        dbClass.column('canvasser','character varying(150)', False)
        dbClass.column('counter','integer', False)

        #=============================================================

        dbClassItems = dbTable('req_for_quotation_items')

        dbClassItems.column('quotationnum','character varying(25)', False)
        dbClassItems.column('itemnum','integer', False)
        dbClassItems.column('description','character varying(250)', False)
        dbClassItems.column('quantity','double precision', False)
        dbClassItems.column('unit','character varying(50)', False)
        dbClassItems.column('unitprice','double precision', False)

        #=============================================================

        dbClassSupp = dbTable('req_for_quotation_suppliers')

        dbClassSupp.column('quotationnum','character varying(15)', False)
        dbClassSupp.column('compid','character varying(15)', False)
        dbClassSupp.column('warrantyper','double precision', False)
        dbClassSupp.column('delperiod','double precision', False)
        dbClassSupp.column('pricevalidity','double precision', False)

    
    def addRequest(self, quotationNum, refnum, projName, projLoc, canvasser):

        
        counter = RequestForQuotation.getMaxCounter(self) + 1
        currentdate = datetime.now().strftime('%Y-%m-%d')
    	
        sql = "insert into req_for_quotation values('"+quotationNum+"', '"+refnum+"', '"+projName+"', '"+projLoc+"', '"+currentdate+"', '"+canvasser+"', "+str(counter)+");"
        cur.execute(sql)
        connection.commit()
        print("Done")

    def addComToReq(self, quotNum, compid):
    	
    	sql = "insert into req_for_quotation_suppliers values('"+quotNum+"', '"+compid+"');"
    	
    	cur.execute(sql)
    	connection.commit()
    	print("Done")

    def addItemToReq(self, quotNum, itemNum, description, unit, unitprice, quantity):
        
        sql = "insert into req_for_quotation_items values('"+quotNum+"', "+str(itemNum)+", '"+description+"', "+str(quantity)+", '"+unit+"', "+str(unitprice)+");"
        print(sql)
        
        cur.execute(sql)
        connection.commit()
        print("Done")   

    def updateComTerms(self, quotNum, compid, warrantyper, delperiod, pricevalidity):
    	
    	sql = "update req_for_quotation_suppliers set warrantyper = "+warrantyper+", delperiod = "+delperiod+", pricevalidity = "+pricevalidity+" where quotationnum = '"+quotNum+"' and compid = '"+compid+"'" 

    	cur.execute(sql)
    	connection.commit()
    	print("Done")

    
    def getComTerms(self, quotnum, compid):
        
        sql = "select * from req_for_quotation_suppliers where quotationnum = '"+quotnum+"' and compid = '"+compid+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result
    

    def getReqItems(self, quotNum):
    	
        sql = "select * from req_for_quotation_items where quotationnum = '"+ quotNum + "';"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
    	
        return result

    def getReqComp(self, quotNum):
        
        sql = "select * from req_for_quotation_suppliers where quotationnum = '"+ quotNum + "';"  

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        
        return result
         
    def getRequestDetails(self, quotNum):
    	
    	sql = "select * from req_for_quotation where quotationnum = '"+quotNum+"'"

    	cur.execute(sql)
    	connection.commit()
    	result = cur.fetchall()

    	return result
    
    def getMaxCounter(self):
        
        sql = "select max(counter) from req_for_quotation where date_part('year', datecreated) = date_part('year', CURRENT_DATE)" 

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall() 
        
        if result[0][0] is None:
            return 0
        else:
            return result[0][0]

    def getAllReqQuo(self):
            
        sql = "select * from req_for_quotation order by (quotationnum)DESC"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result


    def generateReqNum(self):
        
        counter = RequestForQuotation.getMaxCounter(self) + 1

        maxCounter = str(counter).zfill(3)
        year = datetime.now().year
        suffix = float(str(year)[-3:]) if '.' in str(year)[-2:] else int(str(year)[-2:])
        return maxCounter+"-"+str(suffix)

    def getItemNumFromDescription(self, quotNum, description):
        sql = "select itemnum from req_for_quotation_items where description = '"+description+"' and quotationnum = '"+quotNum+"';"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result[0][0]         

    def getReqNumFromRefNum(self, refnum):
        sql = "select quotationnum from req_for_quotation where refnum = '"+refnum+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        
        if result == []:
            return None
        else:
            return result[0][0]    
    
    def getReqNumFromRefNumAll(self, refnum):
        sql = "select quotationnum from req_for_quotation where refnum = '"+refnum+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        
        return result         

if __name__ == "__main__":
    r = RequestForQuotation()
    #r.addRequest('1234-1582', '12544','','','')
    #r.addComToReq('1234-1582', 'smi')
    #print(r.getReqItems('1234-1582'))
    #print(r.getMaxCounter())
    print(r.generateReqNum())

