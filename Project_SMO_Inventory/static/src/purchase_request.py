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
from db_structure import dbTable


c = ConnectDB()
connection = c.connection()
cur = connection.cursor()

dbClass = None

class PurchaseRequest:

    def __init__(self):

        #==================================================================================

        dbClass = dbTable('purchase_request')
        
        dbClass.column('reqnum','character varying(25)',True)
        dbClass.column('prnum','character varying(50)',False)
        dbClass.column('purpose','character varying(250)',False)
        dbClass.column('prtype','character varying(30)',False)
        dbClass.column('requester_id','character varying(15)',False)
        dbClass.column('date_created','date',False)
        dbClass.column('status','boolean',False)
        dbClass.column('init_approval_status','boolean',False)
        dbClass.column('approval_status','boolean',False)
        dbClass.column('declinereason','text',False)
        dbClass.column('counter','integer',False)
        dbClass.column('approval_staus_date','date',False)
        dbClass.column('prereqstatus','boolean',False)
        dbClass.column('readstatus','boolean',False)
        dbClass.column('prereqdate','date',False)
        dbClass.column('readid','character varying(15)',False)
        dbClass.column('init_app_edit','boolean',False)
        dbClass.column('fin_app_edit','boolean',False)

        #==================================================================================

        dbClass_Pur_Req_B_Time = dbTable('purchase_request_bac_timeline')

        
        dbClass_Pur_Req_B_Time.column('reqnum','character varying(15)', True)
        dbClass_Pur_Req_B_Time.column('prnum','character varying(15)',False)
        dbClass_Pur_Req_B_Time.column('prdate','date',False)
        dbClass_Pur_Req_B_Time.column('bacstatus','boolean',False)
        dbClass_Pur_Req_B_Time.column('ponum','character varying(255)',False)

        #==================================================================================

        dbClass_Pur_Req_B_Trans = dbTable('purchase_request_bac_transactions')
     
        dbClass_Pur_Req_B_Trans.column('reqnum','character varying(15)', False)
        dbClass_Pur_Req_B_Trans.column('transnum','integer', False)
        dbClass_Pur_Req_B_Trans.column('dateconducted','date', False)


        #==================================================================================

        dbClass_Pur_Req_Item = dbTable('purchase_request_items')
        
        dbClass_Pur_Req_Item.column('reqnum','character varying(10)', False)
        dbClass_Pur_Req_Item.column('stock_num','character varying(25)', False)
        dbClass_Pur_Req_Item.column('description','text', False)
        dbClass_Pur_Req_Item.column('unit','character varying(50)', False)
        dbClass_Pur_Req_Item.column('unit_price','double precision', False)
        dbClass_Pur_Req_Item.column('quantity','double precision', False)

        #==================================================================================

        dbClass_Pur_Req_Item_Chk = dbTable('purchase_request_items_checker')


        #==================================================================================

        dbClass_Pur_Req_Loc = dbTable('purchase_request_location')
    
        dbClass_Pur_Req_Loc.column('prnum','character varying(15)', True)
        dbClass_Pur_Req_Loc.column('vcafin','boolean', False)
        dbClass_Pur_Req_Loc.column('vcafindate','date', False)
        dbClass_Pur_Req_Loc.column('vcafout','boolean', False)
        dbClass_Pur_Req_Loc.column('vcafoutdate','date', False)
        dbClass_Pur_Req_Loc.column('chanin','boolean', False)
        dbClass_Pur_Req_Loc.column('chanindate','date', False)
        dbClass_Pur_Req_Loc.column('chanout','boolean', False)
        dbClass_Pur_Req_Loc.column('chanoutdate','date', False)
        dbClass_Pur_Req_Loc.column('procin','boolean', False)
        dbClass_Pur_Req_Loc.column('procindate','date', False)


        #==================================================================================

        dbClass_Pur_Req_Mul_PO = dbTable('purchase_request_multi_po')
    
        dbClass_Pur_Req_Mul_PO.column('prnum','character varying(15)', False)
        dbClass_Pur_Req_Mul_PO.column('ponum','character varying(15)', False)
        dbClass_Pur_Req_Mul_PO.column('porelsign','boolean', False)
        dbClass_Pur_Req_Mul_PO.column('porelsigndate','date', False)
        dbClass_Pur_Req_Mul_PO.column('poappstatus','boolean', False)
        dbClass_Pur_Req_Mul_PO.column('poappstatusdate','date', False)
        dbClass_Pur_Req_Mul_PO.column('poretsigndate','date', False)
        dbClass_Pur_Req_Mul_PO.column('supplier','text', False)
        dbClass_Pur_Req_Mul_PO.column('posrstatusdate','date', False)
        dbClass_Pur_Req_Mul_PO.column('expdeldate','date', False)

        #==================================================================================

        dbClass_Pur_Req_Proc_Tim = dbTable('purchase_request_proc_timeline')

        dbClass_Pur_Req_Proc_Tim.column('reqnum','character varying(15)', True)
        dbClass_Pur_Req_Proc_Tim.column('prnum','character varying(15)', False)
        dbClass_Pur_Req_Proc_Tim.column('prnumdate','date', False)
        dbClass_Pur_Req_Proc_Tim.column('quotnum','character varying(15)', False)
        dbClass_Pur_Req_Proc_Tim.column('quotdate','date', False)
        dbClass_Pur_Req_Proc_Tim.column('quotreldate','date', False)
        dbClass_Pur_Req_Proc_Tim.column('quotcoldate','date', False)
        dbClass_Pur_Req_Proc_Tim.column('bidders','integer', False)
        dbClass_Pur_Req_Proc_Tim.column('abcnum','character varying(15)', False)
        dbClass_Pur_Req_Proc_Tim.column('abcreldate','date', False)
        dbClass_Pur_Req_Proc_Tim.column('abcselstatus','boolean', False)
        dbClass_Pur_Req_Proc_Tim.column('abcretdate','date', False)
        dbClass_Pur_Req_Proc_Tim.column('ponum','character varying(255)', False)
        dbClass_Pur_Req_Proc_Tim.column('porelsign','boolean', False)
        dbClass_Pur_Req_Proc_Tim.column('porelsigndate','date', False)
        dbClass_Pur_Req_Proc_Tim.column('poappstatus','boolean', False)
        dbClass_Pur_Req_Proc_Tim.column('poappstatusdate','date', False)
        dbClass_Pur_Req_Proc_Tim.column('poretsigndate','date', False)
        dbClass_Pur_Req_Proc_Tim.column('supplier','character varying(255)', False)
        dbClass_Pur_Req_Proc_Tim.column('posrstatusdate','date', False)
        dbClass_Pur_Req_Proc_Tim.column('expdeldate','date', False)
        dbClass_Pur_Req_Proc_Tim.column('delterm','double precision', False)
        dbClass_Pur_Req_Proc_Tim.column('amount','double precision', False)

        #==============================================================================================

        dbClassBAC = dbTable('bac_transactions')

        dbClassBAC.column('transnum','integer', True)
        dbClassBAC.column('description','character varying(255)', False)
        dbClassBAC.column('details','text', False)
        dbClassBAC.column('conductedby','character varying(255)', False)
        dbClassBAC.column('participatedby','character varying(500)', False)



    def addPR(self, reqnum, purpose, details, idnum):

        purposeString = ""
        
        if "'" in purpose:
            purposeString = purpose.replace("'", "''")
        else:
            purposeString = purpose    
        
        sql = "insert into purchase_request values('{}', null, '{}','{}','{}', '{}', TRUE)".format(reqnum, purposeString, details, idnum, strftime("%Y-%m-%d", gmtime()))             
        
        print(sql)
        cur.execute(sql)
        connection.commit()
        print ("Done")
    
    def addPRStaff(self, reqnum, purpose, details, idnum):

        purposeString = ""
        
        if "'" in purpose:
            purposeString = purpose.replace("'", "''")
        else:
            purposeString = purpose    
        
        sql = "insert into purchase_request values('{}', NULL, '{}', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,'{}','{}')".format(reqnum, purposeString, strftime("%Y-%m-%d", gmtime()), idnum)             
        
        print(sql)
        cur.execute(sql)
        connection.commit()
        print ("Done adding PR for Staff")
    
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
        
        sql = "update purchase_request set status = {} where reqnum = '{}'".format( statusValue, reqnum)             
    
        cur.execute(sql)
        connection.commit()
        print ("Done")
    
    def getAllPR(self):
        
        sql = "select reqnum from purchase_request where requester_id is not NULL and status = TRUE order by (date_created)desc;"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result
    

    def getAllPRByStatus(self, status, statustype):

        statusClause = ''

        if status == 'declined' :
            statusClause = 'init_approval_status = FALSE or approval_status = FALSE'  
        
        else:
            
            if statustype == 'init':

                if status == 'pending':
                    statusClause = 'init_approval_status is NULL'       
            else:

                if status == 'pending':
                    statusClause = 'init_approval_status = TRUE and approval_status is NULL'          
                if status == 'approved':
                    statusClause = 'init_approval_status = TRUE and approval_status is TRUE'        
            
        sql = "select reqnum from purchase_request where "+statusClause+" and requester_id is not NULL and status = TRUE order by (date_created)desc;"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result
    

    def getAllPRByStatusByID(self, status, statustype, idnum):

        statusClause = ''

        if status == 'declined' :
            statusClause = 'init_approval_status = FALSE or approval_status = FALSE'  
        
        else:
            
            if statustype == 'init':

                if status == 'pending':
                    statusClause = 'init_approval_status is NULL'       
            else:

                if status == 'pending':
                    statusClause = 'init_approval_status = TRUE and approval_status is NULL'          
                if status == 'approved':
                    statusClause = 'init_approval_status = TRUE and approval_status is TRUE'        
            
        sql = "select reqnum from purchase_request where "+statusClause+" and requester_id = '"+idnum+"' and status = TRUE  order by (date_created)asc;"
        
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
        
        sql = "select reqnum from purchase_request where requester_id = '{}' and init_approval_status is NULL and status = TRUE  order by (date_created)asc;".format(idnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def getAllInitPendingPR(self):
        
        sql = "select reqnum from purchase_request where init_approval_status is NULL and requester_id is not NULL and status = TRUE  order by (date_created)asc;"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def getAllPendingPRbyID(self, idnum):
        
        sql = "select reqnum from purchase_request where requester_id = '{}' and (init_approval_status = TRUE and approval_status is NULL) and status = TRUE  order by (date_created)desc;".format(idnum)
         
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def getAllPendingPR(self):
        
        sql = "select reqnum from purchase_request where init_approval_status = TRUE and approval_status is NULL and status = TRUE  order by (date_created)asc"
        
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
    
    def getPRTotalCost(self, reqnum):
        
        sql = "select sum(unit_price*quantity)total from purchase_request_items where reqnum = '{}'".format(reqnum)
        
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

    def getTotalCostofPRItems(self, refNum):
        
        sql = "select sum(unit_price * quantity) from purchase_request_items where reqnum = '{}'".format(refNum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result[0][0]


    def getLatestApprovedPRbyId(self, offid):
        sql = ""

        cur.execute(sql)
        connection.commit()
        result = cur.fetchone()

        return result
    

    def getLatestApprovedPRfroQuraterSupplies(self, offid):
        sql = "select reqnum from purchase_request where (purpose like '%quarter%') and (purpose like '%supply%' or purpose like '%supplies%') and requester_id ='"+offid+"' order by date_created limit 5"

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

    def updatePRTable(self, colunmname, colunmtype, datainput, wheredata):

        colunmdata = ""

        if colunmtype == 'int' or colunmtype == 'boolean':
            colunmdata = str(datainput)
        else:   
            colunmdata = "'"+str(datainput)+"'"

        sql = "update purchase_request set "+colunmname+" = "+colunmdata+" where reqnum = '"+wheredata+"'"  

        cur.execute(sql)
        connection.commit()

        print("done")  

    def updatePRItemInfo(self, description, quantity, unitprice, reqnum, stock_num):
        
        sql = "update purchase_request_items set description = '"+description+"', unit_price = "+str(unitprice)+", quantity = "+str(quantity)+" where reqnum = '"+reqnum+"' and stock_num = '"+stock_num+"' "   

        cur.execute(sql)
        connection.commit()

        print("Done")

    def removeItemsFromPR(self, reqnum):

        sql = "delete from purchase_request_items where reqnum = '"+reqnum+"'"

        cur.execute(sql)
        connection.commit()

        print("done")


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

#=============================================================================================================================================================
## PR Staff Codes
#=============================================================================================================================================================

    def getAllPRbyIDStaff(self, idnum):
        
        sql = "select reqnum from purchase_request where readid = '{}' order by (date_created)desc, (prnum)desc;".format(idnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result  

    def updateStaffPRAcceptance(self, reqnum, reqstat, editstat):
        
        sql = "update purchase_request set prereqstatus = '"+str(reqstat)+"' , readstatus = "+str(editstat)+" where reqnum = '"+reqnum+"'"

        cur.execute(sql)
        connection.commit()

        print("Done")

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
            
        toSQLDate = "abcreldate = '"+str(reldate)+"'"    

        if reldate == '':
           toSQLDate = "abcreldate = NULL"  

        sql = "update purchase_request_proc_timeline set  abcnum = '"+abcnum+"', "+toSQLDate+" where reqnum = '"+reqnum+"'"

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
  
    def getProCTimeLineDetailsFromLikeRef(self, reqnum):
        
        sql = "select * from purchase_request_proc_timeline where reqnum like '"+reqnum+"%'"

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
    
    def getMultiPONum(self, ponum):
        
        sql = "select * from purchase_request_multi_po where prnum = '"+ponum+"'"

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
    
    def getAllPRFromProcTimelineFromlikeRef(self, refData):

        sql = "select reqnum from purchase_request_proc_timeline where reqnum like '"+refData+"%' order by (prnum, reqnum) desc"

        cur.execute(sql)
        connection.commit()

        result = cur.fetchall()

        return result
    
    def getAllPRFromProcTimelineFromlikeRefWthLimit(self, refData, limitVal):

        sql = "select reqnum from purchase_request_proc_timeline where reqnum like '"+refData+"%' order by (prnum, reqnum) desc limit "+str(limitVal)+""

        cur.execute(sql)
        connection.commit()

        result = cur.fetchall()

        return result
    


##===============================================================================================================================================================        
#=============================================================================================================================================================
## PR ProcLine MultiPO
#=============================================================================================================================================================

    def addMultiPO(self, prnum, ponum):
        
        sql = "insert into purchase_request_multi_po values('"+str(prnum)+"', '"+str(ponum)+"')"
        cur.execute(sql)
        connection.commit()

        print("Done")


    def updateMulti(self, updateList, reqnum):
        
        setSQLString = ""

        for idx, x in enumerate(updateList):
            data = updateList[x]
            print(x)
            print(data)
            if data[1] == 'int' or data[1] == 'boolean':
                setSQLString = setSQLString + ""+x+" = "+str(data[0])+""
            else:
                setSQLString = setSQLString + ""+x+" = '"+str(data[0])+"'"  

            if idx != len(updateList) - 1:
                setSQLString = setSQLString + ", "    

        sql = "update purchase_request_multi_po set "+setSQLString +" where prnum = '"+str(reqnum)+"'"
        cur.execute(sql)
        connection.commit()

        print("Done")

if __name__ == "__main__":
    
    p = PurchaseRequest()
    print(p.getLatestApprovedPRfroQuraterSupplies('offid'))
    print("\============")
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
    #print(p.getMaxCounter())
    #print(p.generateReqNum())
    #print(p.getReqNumFromPR('001-17'))
    #print(p.getAllInitPendingPR())
    #print(p.getPRType(p.getReqNumFromPR('001-17')[0][0]))
    #p.updateMulti({'col1':('data1','String'), 'col2':('data1','String'), 'col3':('data1','int')}, '')
    prList = p.getAllPRByStatus('approved','final')
    for x in prList:
        print(x)

