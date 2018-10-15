# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$10 31, 16 3:15:37 PM$"

import random
import string
from random import randint


from connectdb import ConnectDB
from time import gmtime, strftime
from datetime import datetime

c = ConnectDB()
connection = c.connection()
cur = connection.cursor()

class PurchaseRequest:

    def addPR(self, reqnum, purpose, details, idnum):

        purposeString = ""
        
        if "'" in purpose:
            purposeString = purpose.replace("'", "''")
        else:
            purposeString = purpose    
        
        sql = "insert into purchase_request values('{}', null, '{}','{}','{}', '{}')".format(reqnum, purposeString, details, idnum, strftime("%Y-%m-%d", gmtime()))             
        
        print(sql)
        cur.execute(sql)
        connection.commit()
        print ("Done")
    

    def addPRToProc(self, reqnum):
        
        sql = "insert into purchase_request_proc_timeline values('{}')".format(reqnum)             
        
        print(sql)
        cur.execute(sql)
        connection.commit()
        print ("Done")  

    def addPRToProcNewLine(self, reqnum, prnum, prnumdate):
        
        sql = "insert into purchase_request_proc_timeline values('{}', '{}', '{}')".format(reqnum, prnum, prnumdate)             
        
        print(sql)
        cur.execute(sql)
        connection.commit()
        print ("Done")       
    
    def updatePRApproval(self, reqnum, statustype, decision, reason):

        
        if decision == 'TRUE':
            sql = "update purchase_request set {} = '{}' where reqnum = '{}'".format(statustype, decision, reqnum)

        else:
            sql = "update purchase_request set {} = '{}', declinereason = '{}' where reqnum = '{}'".format(statustype, decision, reason, reqnum)
                     
    
        
        cur.execute(sql)
        connection.commit()
        print ("Done")
    
    def updatePRApprovalDate(self, reqnum):

        currentdate = datetime.now().strftime('%Y-%m-%d')

        sql = "update purchase_request set approval_staus_date = '"+str(currentdate)+"' where reqnum = '"+reqnum+"'"
        
        cur.execute(sql)
        connection.commit()
        print ("Done")
    
    

    def setPRNumber(self, reqnum):
        
        prnum = PurchaseRequest.generateReqNum(self)
        counter = PurchaseRequest.getMaxCounter(self) + 1
        currentdate = datetime.now().strftime('%Y-%m-%d')



        sql = "update purchase_request set prnum = '"+prnum+"', counter = "+str(counter)+", approval_staus_date = '"+str(currentdate)+"' where reqnum = '"+reqnum+"'"
        
        cur.execute(sql)
        connection.commit()
        print ("Done")
    
    def setPRNumberFromInput(self, reqnum, inputprnum):
        
        counter = PurchaseRequest.getMaxCounter(self) + 1
        currentdate = datetime.now().strftime('%Y-%m-%d')



        sql = "update purchase_request set prnum = '"+inputprnum+"', counter = "+str(counter)+" where reqnum = '"+reqnum+"'"
        
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
        
        sql = "select reqnum from purchase_request where requester_id = '{}' and init_approval_status is NULL order by (date_created)asc;".format(idnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def getAllInitPendingPR(self):
        
        sql = "select reqnum from purchase_request where init_approval_status is NULL order by (date_created)asc;"
        
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
        
        sql = "select reqnum from purchase_request where init_approval_status = TRUE and approval_status is NULL order by (date_created)asc"
        
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
    
    def getAllNonPendingPR(self):
        
        sql = "select reqnum from purchase_request where init_approval_status is not NULL and approval_status is not NULL order by (date_created)desc;"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def getAllNonInitPendingPR(self):
        
        sql = "select reqnum from purchase_request where init_approval_status is not NULL order by (date_created)desc;"
        
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

    def addItemToPR(self, reqnum, stockNum, description, unit, price, quantity):
        
        sql = "insert into purchase_request_items values('{}', '{}', '{}','{}',{}, {})".format(reqnum, stockNum, description, unit, price, quantity)             
        cur.execute(sql)
        connection.commit()
        print ("Done")
    
    def getItemByPR(self, reqnum):
        
        sql = "select *, (unit_price * quantity)total from purchase_request_items where reqnum = '{}' order by cast (stock_num as integer); ".format(reqnum)
        
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



    def getUnclassifiedPRByDescription(self, description):
        
        sql = "select * from purchase_request where reqnum in (select reqnum from purchase_request_items where description = '"+description+"') and prtype = ''"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        
        return result 

    def updatePRType(self, reqnum, inputType):
        
        sql = "update purchase_request set prtype = '"+inputType+"' where reqnum = '"+reqnum+"'"

        cur.execute(sql)
        connection.commit()
        print("Done")

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
    
    def getPRType(self, reqnum):
        
        sql = "select prtype from purchase_request where reqnum = '"+reqnum+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

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

    def isPRNumExist(self, ref):
        
        sql = "select reqnum from purchase_request where reqnum = '"+ref+"'"

        cur.execute(sql)
        connection.commit()
        r = cur.fetchall()

        if r == []:
            return False
        else:
            return True    

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

#==============================================================================================================================================================
## PR Location Codes
#==============================================================================================================================================================
    
    def addPRLoc(self, reqnum):
        
        sql = "insert into purchase_request_location values('{}')".format(reqnum)             
        
        print(sql)
        cur.execute(sql)
        connection.commit()
        print ("Done")
    
    def getPRLocDetails(self, prnum):
        
        sql = "select * from purchase_request_location where prnum = '{}'".format(prnum)
         
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def updatePRLoc(self, prnum, uptype, update, upoff):

        updateCol = ''
        updateColDate = ''

        if uptype == 'in' and  upoff == 'vcaf':
            updateCol = 'vcafin'
            updateColDate = 'vcafindate'

        if uptype == 'out' and  upoff == 'vcaf':  
            updateCol = 'vcafout'
            updateColDate = 'vcafoutdate' 

        if uptype == 'in' and  upoff == 'oc':
            updateCol = 'chanin'
            updateColDate = 'chanindate' 

        if uptype == 'out' and  upoff == 'oc':
            updateCol = 'chanout'
            updateColDate = 'chanoutdate'     

        if uptype == 'in' and  upoff == 'proc': 
            updateCol = 'procin'
            updateColDate = 'procindate' 

        sql = "update purchase_request_location set "+updateCol+" = TRUE, "+updateColDate+" = '"+update+"' where prnum = '"+prnum+"'"

        cur.execute(sql)
        connection.commit()

    def getPRLocDetails(self, reqnum):
        
        sql = "select * from purchase_request_location where prnum = '"+reqnum+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result


##=============================================================================================================================================================
## Special Codes for the New UI 
##=============================================================================================================================================================
    
    def updatePrNum(self, reqnum, prnum, prdate):

        currentdate = datetime.now().strftime('%Y-%m-%d')

        sql = "update purchase_request_proc_timeline set prnum = '"+prnum+"', prnumdate = '"+str(currentdate)+"' where reqnum = '"+reqnum+"'"

        cur.execute(sql)
        connection.commit()

        print("Done Adding New PR Num")

    def updateQuotNum(self, reqnum, quotnum, quotdate):
        
        sql = "update purchase_request_proc_timeline set quotnum = '"+quotnum+"', quotdate = '"+str(quotdate)+"' where reqnum = '"+reqnum+"'"

        cur.execute(sql)
        connection.commit()

        print("Done Adding New Quotation Num")
    

    def updateCanvassStartEnd(self, reqnum, startDate, endDate, bidders):
        
        sql = "update purchase_request_proc_timeline set quotreldate= '"+str(startDate)+"', quotcoldate = '"+str(endDate)+"', bidders = "+str(bidders)+" where reqnum = '"+reqnum+"'"

        cur.execute(sql)
        connection.commit()

        print("Done Update Quotation Info")    

    def addACData(self, reqnum, abcnum, reldate):
        
        sql = "update purchase_request_proc_timeline set  abcnum = '"+abcnum+"', abcreldate = '"+str(reldate)+"' where reqnum = '"+reqnum+"'"

        cur.execute(sql)
        connection.commit()

        print("Done Adding New Abstract Num")

    def updateACData(self, reqnum, retdate):
        
        sql = "update purchase_request_proc_timeline set  abcretdate = '"+str(retdate)+"', abcselstatus = TRUE where reqnum = '"+reqnum+"'"

        cur.execute(sql)
        connection.commit()

        print("Done Adding New Abstract Num")              

    def addPOData(self, reqnum, ponum, poreldate):
        
        sql = "update purchase_request_proc_timeline set  ponum = '"+ponum+"', porelsigndate = '"+str(poreldate)+"', porelsign = TRUE where reqnum = '"+reqnum+"'"

        cur.execute(sql)
        connection.commit()

        print("Done Adding New PO Num")              


    def getPRCountForNewTimeline(self, idnum):
        sql = "select count(reqnum) from purchase_request_proc_timeline where reqnum like '"+idnum+"%'"

        cur.execute(sql)
        connection.commit()

        result = cur.fetchall()

        return result[0][0]

    def updatePOAppData(self, reqnum, appstatus, poretdate):
        
        sql = "update purchase_request_proc_timeline set  poappstatus = "+appstatus+", poretsigndate = '"+str(poretdate)+"' where reqnum = '"+reqnum+"'"

        cur.execute(sql)
        connection.commit()

        print("Done Updating PO Information")              

    def updatePOSerData(self, reqnum, poserdate, expdeldate, supplier):
        
        sql = "update purchase_request_proc_timeline set  posrstatusdate = '"+str(poserdate)+"', expdeldate = '"+str(expdeldate)+"',supplier = '"+supplier+"' where reqnum = '"+reqnum+"'"

        cur.execute(sql)
        connection.commit()

        print("Done Updating PO Information")    

    def updateQuotReleaseandCollect(self, reqnum, dateInput, uptype):

        updateCol = ''
        if uptype == 'rel':
            updateCol = 'quotreldate'
        else:
            updateCol = 'quotcoldate'

        sql = "update purchase_request_proc_timeline set "+updateCol+" = '"+str(dateInput)+"' where reqnum = '"+reqnum+"'"

        cur.execute(sql)
        connection.commit()

        print("Done update on Quotation Date")

    def setNumberOfBidders(self, reqnum, bidsnum):
        
        sql = "update purchase_request_proc_timeline set bidders = "+bidsnum+" where reqnum = '"+reqnum+"'"

        cur.execute(sql)
        connection.commit()

        print("Done Update on number of Bidders")

    def getProCTimeLineDetails(self, reqnum):
        
        sql = "select * from purchase_request_proc_timeline where reqnum = '"+reqnum+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result
  

    def getPRNumforPONum(self, ponum):
        
        sql = "select reqnum from purchase_request_proc_timeline where ponum = '"+ponum+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getPRNumforPONumForNew(self, ponum):
        
        sql = "select reqnum from purchase_request_proc_timeline where prnum = '"+ponum+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result        


    def getAllPRFromProcTimeline(self):

        sql = "select ponum from purchase_request_proc_timeline where ponum != '' order by (ponum) desc"

        cur.execute(sql)
        connection.commit()

        result = cur.fetchall()

        return result
    
##===============================================================================================================================================================        


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
    print(p.getPRType(p.getReqNumFromPR('001-17')[0][0]))