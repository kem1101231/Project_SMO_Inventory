# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$10 31, 16 3:15:37 PM$"

from connectdb import ConnectDB
from time import gmtime, strftime
from datetime import datetime
from db_structure import dbTable


c = ConnectDB()
connection = c.connection()
cur = connection.cursor()

dbClass = None

class RequisitionAndIssuanceSlip:

    def __init__(self):
        
        dbClass = dbTable('req_iss_slip')
       
        dbClass.column('slipnum','character varying(10)',True)
        dbClass.column('risnum','character varying(10)',False)
        dbClass.column('purpose','text',False)
        dbClass.column('datecreated','date',False)
        dbClass.column('requestid','character varying(10)',False)
        dbClass.column('status','boolean',False)
        dbClass.column('statusreason','character varying(255)',False)
        dbClass.column('statusdate','date',False)
        dbClass.column('counter','integer',False)
        dbClass.column('releasestatus','boolean',False)
        dbClass.column('releasedate','date',False)
        dbClass.column('receivedby','character varying(10)',False)

        #=========================================================================

        dbClassItems = dbTable('ris_items')

        dbClassItems.column('slipnum','character varying(10)', True)
        dbClassItems.column('stocknum','integer', False)
        dbClassItems.column('description','character varying(250)', False)
        dbClassItems.column('unit','character varying(50)', False)
        dbClassItems.column('quantity','double precision', False)
        dbClassItems.column('quantityapproved','double precision', False)

        #==========================================================================

        dbClassSuppInv = dbTable('supply_inventory')

        dbClassSuppInv.column('id','character varying(10)', True)
        dbClassSuppInv.column('description','character varying(250)', False)
        dbClassSuppInv.column('type','character varying(50)', False)
        dbClassSuppInv.column('unit','character varying(50)', False)
        dbClassSuppInv.column('itemid','character varying(10)', False)
        dbClassSuppInv.column('quantity','double precision', False)
        dbClassSuppInv.column('initquantity','double precision', False)
        dbClassSuppInv.column('latestup','date', False)





    def addRIS(self, reqnum, purpose, details, idnum):
        
        sql = "insert into req_iss_slip values('{}', null, '{}','{}', '{}', NULL, NULL, NULL)".format(reqnum, purpose, strftime("%Y-%m-%d", gmtime()),idnum)             
        
        print(sql)
        cur.execute(sql)
        connection.commit()
        print ("Done")
    
    def updateRISApproval(self, reqnum, decision, reason):
        
        if decision == 'TRUE':
            sql = "update req_iss_slip set status = TRUE where slipnum = '"+reqnum+"'"

        else:
            sql = "update req_iss_slip set status = FALSE , statusreason = '"+reason+"' where slipnum = '"+reqnum+"'"
             
        
        cur.execute(sql)
        connection.commit()
        print ("Approval Update Done, Decission was " + decision)
    
    def setRISNumber(self, reqnum):
        
        prnum = RequisitionAndIssuanceSlip.generateReqNum(self)
        counter = RequisitionAndIssuanceSlip.getMaxCounter(self) + 1
        currentdate = datetime.now().strftime('%Y-%m-%d')



        sql = "update req_iss_slip set risnum = '"+prnum+"', counter = "+str(counter)+", statusdate = '"+str(currentdate)+"' where slipnum = '"+reqnum+"'"
        
        cur.execute(sql)
        connection.commit()
        print ("Done Numbering RIS")
    
    
    def updateRISApprovedQty(self, slipnum, itemnum, qty):
        
        sql = "update ris_items set quantityapproved  = '{}' where slipnum = '{}' and stocknum = '{}'".format( qty, slipnum, itemnum)             
    
        cur.execute(sql)
        connection.commit()
        print ("Done")

    def releaseRIS(self, reqnum, recOfficer):
        
        counter = RequisitionAndIssuanceSlip.getMaxCounter(self) + 1
        currentdate = datetime.now().strftime('%Y-%m-%d')

        sql = "update req_iss_slip set releasestatus = TRUE, receivedby = '"+recOfficer+"', releasedate = '"+str(currentdate)+"' where slipnum = '"+reqnum+"'"
        
        cur.execute(sql)
        connection.commit()
        print ("Done")
    
    
    def updatePRStatus(self, reqnum, statusValue):
        
        sql = "update purchase_request set status = '{}' where reqnum = '{}'".format( statusValue, reqnum)             
    
        cur.execute(sql)
        connection.commit()
        print ("Done")
    
    def getAllRIS(self):
        
        sql = "select slipnum from req_iss_slip order by (datecreated)desc, (risnum)desc;"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result
    
    def getAllRISbyID(self, idnum):
    
        sql = "select slipnum from req_iss_slip where requestid = '{}' order by (datecreated)desc, (risnum)desc;".format(idnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result
    
    def getAllRISbyIDTimeFrame(self, idnum, fromdate, todate):
    
        sql = "select slipnum from req_iss_slip where requestid = '{}' and releasedate between '{}' and '{}' order by (datecreated)desc, (risnum)desc;".format(idnum, fromdate, todate)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def getAllRISTimeFrame(self, fromdate, todate):
    
        sql = "select slipnum from req_iss_slip where releasedate between '{}' and '{}' order by (datecreated)desc, (risnum)desc;".format(fromdate, todate)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result        

    def getRISByItemConsumtion(self, slipnum, description):
    
        sql = "select sum(quantityapproved)approved, sum(quantity)requested from ris_items where slipnum = '{}' and description = '{}';".format(slipnum, description)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result
    
    def getAllRISByItemConsumtion(self, description):
    
        sql = "select sum(quantityapproved)approved, sum(quantity)requested from ris_items where description = '{}';".format(description)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def getQuarRISByItemConsumtion(self, fromdate, todate, description):

        risList = RequisitionAndIssuanceSlip.getAllRISTimeFrame(self, fromdate, todate)
        qtyapp = 0
        qtyreq = 0

        print(":::::::::::::")
        print("RIS List")
        print(risList)

        for x in risList:
            print(x[0])
            print(description)
        
            sql = "select sum(quantityapproved)approved, sum(quantity)requested from ris_items where  slipnum = '{}' and description = '{}';".format(x[0],description)
            
            cur.execute(sql)
            connection.commit()
            result = cur.fetchall()

            if result[0][0] == None:
                return [0, 0]
            else:
                qtyapp = qtyapp + result[0][0]
                qtyreq = qtyreq + result[0][1] 

                return [qtyapp, qtyreq]


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

    def getAllPendingRIS(self):
        
        sql = "select slipnum from req_iss_slip where status is NULL order by (datecreated)desc"
        
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

    def addItemToRIS(self, reqnum, stockNum, description, unit, quantity):
        
        sql = "insert into ris_items values('{}', {}, '{}','{}',{}, 0)".format(reqnum, stockNum, description, unit, quantity)             
        cur.execute(sql)
        connection.commit()
        print ("Done")
    
    def getItemByRIS(self, reqnum):
        
        sql = "select * from ris_items where slipnum = '{}' order by description;".format(reqnum)
        
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

    def getRISDetails(self, reqnum):
        
        sql = "select * from req_iss_slip where slipnum = '{}'".format(reqnum)
        
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
        
        sql = "select max(counter) from req_iss_slip where date_part('year', datecreated) = date_part('year', CURRENT_DATE)" 

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall() 
        
        if result[0][0] is None:
            return 0
        else:
            return result[0][0]


    def generateReqNum(self):
        
        counter = RequisitionAndIssuanceSlip.getMaxCounter(self) + 1

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

    def isRISNumExist(self, ref):
        
        sql = "select slipnum from req_iss_slip where slipnum = '"+ref+"'"

        cur.execute(sql)
        connection.commit()
        r = cur.fetchall()

        if r == []:
            return False
        else:
            return True    
    
    def getRISDetailsByRISNum(self, ref):
        
        sql = "select * from req_iss_slip where risnum = '"+ref+"'"

        cur.execute(sql)
        connection.commit()
        r = cur.fetchall()
        
        return r             

# =================================================================================================
#   Claim Function
    
    def getAllClaimedQty(self, suppid, fromdate, todate):
        pass
    
    def getAllClaimedQtyByID(self, suppid, fromdate, todate, offID):
        pass        
# -------------------------------------------------------------------------------------------------
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
    
    p = RequisitionAndIssuanceSlip()
    #print(p.getMaxCounter())
    #print(p.generateReqNum())
    #print(p.getReqNumFromPR('001-17'))
    #print(p.getAllInitPendingPR())
    print(p.getQuarRISByItemConsumtion('2018-04-01', '2018-06-30', 'Folder Brown Long'))