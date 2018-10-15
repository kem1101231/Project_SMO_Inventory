# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$10 31, 16 3:15:37 PM$"

from connectdb import ConnectDB
from time import gmtime, strftime
from datetime import datetime

c = ConnectDB()
connection = c.connection()
cur = connection.cursor()

class RequisitionAndIssuanceSlip:

    def addRIS(self, reqnum, purpose, details, idnum):
        
        sql = "insert into req_issuance_slip values('{}', null, '{}','{}', NULL, NULL, NULL, '{}')".format(reqnum, purpose, strftime("%Y-%m-%d", gmtime()),idnum)             
        
        print(sql)
        cur.execute(sql)
        connection.commit()
        print ("Done")
    
    def updateRISApproval(self, reqnum, decision, reason):
        
        if decision == 'TRUE':
            sql = "update req_issuance_slip set status = TRUE where slipnum = '"+reqnum+"'"

        else:
            sql = "update req_issuance_slip set status = FALSE , statusreason = '"+reason+"' where slipnum = '"+reqnum+"'"
                     
    
        
        cur.execute(sql)
        connection.commit()
        print ("Done")
    
    def setRISNumber(self, reqnum):
        
        prnum = PurchaseRequest.generateReqNum(self)
        counter = PurchaseRequest.getMaxCounter(self) + 1
        currentdate = datetime.now().strftime('%Y-%m-%d')



        sql = "update req_issuance_slip set risnum = '"+prnum+"', counter = "+str(counter)+", stausdate = '"+str(currentdate)+"' where slipnum = '"+reqnum+"'"
        
        cur.execute(sql)
        connection.commit()
        print ("Done")
    

    def updatePRStatus(self, reqnum, statusValue):
        
        sql = "update purchase_request set status = '{}' where reqnum = '{}'".format( statusValue, reqnum)             
    
        cur.execute(sql)
        connection.commit()
        print ("Done")
    
    def getAllPR(self):
        
        sql = "select reqnum from purchase_request;"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result
    
    def getAllPRbyID(self, idnum):
        
        sql = "select reqnum from purchase_request where requester_id = '{}' order by (date_created)desc, (prnum)desc;".format(idnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result
    
    def getAllInitPendingPRbyID(self, idnum):
        
        sql = "select reqnum from purchase_request where requester_id = '{}' and init_approval_status is NULL order by (date_created)desc;".format(idnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def getAllInitPendingPR(self):
        
        sql = "select reqnum from purchase_request where init_approval_status is NULL order by (date_created)desc;"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def getAllPendingPRbyID(self, idnum):
        
        sql = "select reqnum from purchase_request where requester_id = '{}' and (init_approval_status = TRUE and approval_status is NULL) order by (date_created)desc;".format(idnum)
         
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def getAllPendingPR(self):
        
        sql = "select reqnum from purchase_request where init_approval_status = TRUE and approval_status is NULL; order by (date_created)desc"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def getAllApprovedPRbyID(self, idnum):
        
        sql = "select reqnum from purchase_request where requester_id = '{}' and (init_approval_status = TRUE and approval_status = TRUE) order by (date_created)desc;".format(idnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result
    
    def getAllApprovedPR(self):
        
        sql = "select reqnum from purchase_request where init_approval_status = TRUE and approval_status = TRUE order by (date_created)desc;"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def getAllDeclinedPRbyID(self, idnum):
        
        sql = "select reqnum from purchase_request where requester_id = '{}' and (init_approval_status = FALSE or approval_status = FALSE) order by (date_created)desc;".format(idnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def getAllDeclinedPR(self):
        
        sql = "select reqnum from purchase_request where init_approval_status = FALSE or approval_status = FALSE order by (date_created)desc;"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def addItemToRIS(self, reqnum, stockNum, description, unit, price, quantity):
        
        sql = "insert into ris_items values('{}', {}, '{}','{}',{}, 0)".format(reqnum, stockNum, description, unit, quantity)             
        cur.execute(sql)
        connection.commit()
        print ("Done")
    
    def getItemByPR(self, reqnum):
        
        sql = "select *, (unit_price * quantity)total from purchase_request_items where reqnum = '{}' order by description;".format(reqnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def getReqNumFromPR(self, prnum):
         
        sql = "select reqnum from purchase_request where prnum = '{}';".format(prnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        
        return result  

    def getReqNumFromPRForSearch(self, prnum):
        
        sql = "select reqnum, purpose from purchase_request where prnum = '{}';".format(prnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        
        return result  

    def getReqNumFromPRwithID(self, prnum, idnum):
        
        sql = "select reqnum, purpose from purchase_request where prnum = '{}' and requester_id = '{}';".format(prnum, idnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        
        return result  

    def getPRDetails(self, reqnum):
        
        sql = "select * from purchase_request where reqnum = '{}'".format(reqnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def getTotalItemNumofPR(self, theItemList):
        
        totalCost = 0
        
        for itemDetails in theItemList:

            totalCost = totalCost + itemDetails[5]


        return totalCost


    def getTotalCostofPR(self, theItemList):
        
        totalCost = 0
        
        for itemDetails in theItemList:
            
            totalCost = totalCost + itemDetails[6]


        return totalCost

    def getLatestApprovedPRbyOffice(self, offid):
        sql = ""

        cur.execute(sql)
        connection.commit()
        result = cur.fetchone()

        return result

    def getMaxCounter(self):
        
        sql = "select max(counter) from purchase_request where date_part('year', date_created) = date_part('year', CURRENT_DATE)" 

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall() 
        
        if result[0][0] is None:
            return 0
        else:
            return result[0][0]


    def generateReqNum(self):
        
        counter = PurchaseRequest.getMaxCounter(self) + 1

        maxCounter = str(counter).zfill(3)
        year = datetime.now().year
        suffix = float(str(year)[-3:]) if '.' in str(year)[-2:] else int(str(year)[-2:])
        return maxCounter+"-"+str(suffix)

    def isPRApproved(self, prnum):
        

        reqnum = self.getReqNumFromPR(prnum)  

        if reqnum == []:
            return False
        else:
            return True      
        


if __name__ == "__main__":
    
    p = PurchaseRequest()
    #pp = p.getPRDetails('EqoA-6375')
    #pp = pp[0] + (p.getTotalCostofPR(p.getItemByPR('EqoA-6375')),)
    #print(pp)
    #p.addItemToPR('2011-533', '25', 'Asus EEE PC', 'unit', 23000, 2)
    #p.addItemToPR('2011-533', '25', 'Fan', 'unit',6955, 5)
    #p.addItemToPR('2011-533', '25', 'AirCon', 'unit', 25536, 6)
    #p.addItemToPR('2011-533', '25', 'HP Pavalion', 'unit', 56000, 3)
    #p.addItemToPR('2011-533', '25', 'Samsung Galaxy', 'unit', 25615, 1)
    #print(p.getTotalCostofPR(p.getItemByPR('2011-533')))
    #p.addPR("20366-66", 'GGWP', 'Noob Troll', '2011-0623')
    print(p.getMaxCounter())
    print(p.generateReqNum())
    print(p.getReqNumFromPR('001-17'))
    print(p.getAllInitPendingPR())