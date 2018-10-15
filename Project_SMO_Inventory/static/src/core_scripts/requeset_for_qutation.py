#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$11 12, 16 7:26:30 PM$"

from datetime import datetime

from connectdb import ConnectDB
from purchase_request import PurchaseRequest

c = ConnectDB()
connection = c.connection()
cur = connection.cursor()

preq = PurchaseRequest()

class RequestForQuotation:
    
    def addRequest(self, quotationNum, refnum, projName, projLoc, canvasser):

    	currentdate = datetime.now().strftime('%Y-%m-%d')
    	print("insert into req_for_quotation values('"+quotationNum+"', '"+refnum+"', '"+projName+"', '"+projLoc+"', '"+currentdate+"', '"+canvasser+"');")
    	sql = "insert into req_for_quotation values('"+quotationNum+"', '"+refnum+"', '"+projName+"', '"+projLoc+"', '"+currentdate+"', '"+canvasser+"');"
    	cur.execute(sql)
    	connection.commit()
    	print("Done")

    def addComToReq(self, quotNum, compid):
    	
    	sql = "insert into req_for_quotation_suppliers values('"+quotNum+"', '"+compid+"');"
    	
    	cur.execute(sql)
    	connection.commit()
    	print("Done")

    def updateComTerms(self, qoutNum, compid, warrantyper, delperiod, pricevalidity):
    	
    	sql = "update req_for_quotation_suppliers set warrantyper = "+warrantyper+", delperiod = "+delperiod+", pricevalidity = "+pricevalidity+" where quotationnum = '"+quotNum+"' and compid = '"+compid+"'" 

    	cur.execute(sql)
    	connection.commit()
    	print("Done")

    def getComTerms(self, quotnum, compid):
        
        sql = "select * req_for_quotation_suppliers where quotationnum = '"+quotNum+"' and compid = '"+compid+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getAllReqQuo(self):
            
        sql = "select * req_for_quotation order by (quotationnum)DESC"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getReqItems(self, quotNum):
    	
    	reqDetails= self.getRequestDetails(quotNum)
    	refnum = preq.getReqNumFromPR(reqDetails[0][1]) 
    	itemList = preq.getItemByPR(refnum[0][0])

    	return itemList

    def getRequestDetails(self, quotNum):
    	
    	sql = "select * from req_for_quotation where quotationnum = '"+quotNum+"'"

    	cur.execute(sql)
    	connection.commit()
    	result = cur.fetchall()

    	return result

if __name__ == "__main__":
    r = RequestForQuotation()
    #r.addRequest('1234-1582', '12544','','','')
    #r.addComToReq('1234-1582', 'smi')
    print(r.getReqItems('1234-1582'))
