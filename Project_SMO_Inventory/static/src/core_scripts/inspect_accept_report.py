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

class InsepectionAndAcceptanceReceipt:

    def addIAR(self, iarnum, ponum, podate, reqoff, receiptnum, receiptdate, insdate, insofficer, receivedate, receiveoff):
        
        counter = InsepectionAndAcceptanceReceipt.getMaxCounter(self) + 1
        
        sql = "insert into insp_and_accept_report values('{}', '{}', '{}','{}','{}', '{}', FALSE, '{}', '{}', FALSE, '{}','{}', {})".format(iarnum, ponum, reqoff, podate, receiptnum, receiptdate, insdate, insofficer, receivedate, receiveoff, counter)             
        
        cur.execute(sql)
        connection.commit()
        print ("Done")
    
    def updateInsStatus(self, iarnum, status, insDate):
        
        sql = "update insp_and_accept_report set insstatus = {}, insdate = '{}'  where iarnum = '{}'".format(status, insDate, iarnum)
         
        cur.execute(sql)
        connection.commit()
        print ("Done")
    
    def updateItemComp(self, iarnum, status, receivedate):
        
        if status == True:
            sql = "update insp_and_accept_report set isitemcomplete = TRUE, receivedate = '{}' where iarnum = '{}'".format(receivedate, iarnum)

        else:
            sql = "update insp_and_accept_report set isitemcomplete = FALSE, receivedate = '{}' where iarnum = '{}'".format(receivedate ,iarnum)
                     
        cur.execute(sql)
        connection.commit()
        print ("Done")

    def addItemToIAR(self, iarnum, stockNum, description, unit, quantity):
        
        sql = "insert into iar_items values('{}', {}, '{}', '{}', {})".format(iarnum, stockNum, unit, description, quantity)             
        
        cur.execute(sql)
        connection.commit()
        print ("Done")


    def getIARItems(self, iarnum):
        
        sql = "select *,(quantity-compstatmiss)miss from iar_items where iarnum = '"+iarnum+"'"         
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result  

    def getAllIARItems(self, iarnum):
        
        sql = "select *,(quantity-compstatmiss)miss from iar_items"         
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result            

    def setItemCompStatus(self, iarnum, status, statdate, stockNum, quantity):
    
        if status == 'TRUE':
            sql = "update iar_items set compstat = TRUE, compdate = '"+str(statdate)+"',  compstatmiss = "+str(quantity)+" where iarnum = '"+iarnum+"' and stocknum = "+str(stockNum)+""
        else:
            sql = "update iar_items set compstat = FALSE, compdate = '"+str(statdate)+"', compstatmiss = "+str(quantity)+" where iarnum = '"+iarnum+"' and stocknum = "+str(stockNum)+""    

        cur.execute(sql)
        connection.commit()
        print("Done")

    def setItemWorkStatus(self, iarnum, status, statdate, stockNum, quantity):
        
        if status == 'TRUE':
            sql = "update iar_items set workstat = TRUE, workdate = '"+str(statdate)+"' where iarnum = '"+iarnum+"' and stocknum = "+str(stockNum)+""
        else:
            sql = "update iar_items set workstat = FALSE, workdate = '"+str(statdate)+"', workstatmiss = "+quantity+" where iarnum = '"+iarnum+"' and stocknum = "+str(stockNum)+""
                
        cur.execute(sql)
        connection.commit()
        print("Done")

    def getIARDetails(self, iarnum):
        
        sql = "select * from insp_and_accept_report where iarnum = '{}'".format(iarnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result
    
    def getAllIARNums(self):
        
        sql = "select iarnum from insp_and_accept_report order by (receivedate)DESC" 

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall() 
        
        return result

    def getMaxCounter(self):
        
        sql = "select max(counter) from insp_and_accept_report where date_part('year', receivedate) = date_part('year', CURRENT_DATE)" 

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall() 
        
        if result[0][0] is None:
            return 0
        else:
            return result[0][0]


    def generateReqNum(self):
        
        counter = InsepectionAndAcceptanceReceipt.getMaxCounter(self) + 1

        maxCounter = str(counter).zfill(3)
        year = datetime.now().year
        suffix = float(str(year)[-3:]) if '.' in str(year)[-2:] else int(str(year)[-2:])
        
        return maxCounter+"-"+str(suffix)

    def getIARNumFromRef(self, refNum):
        
        sql = "select iarnum from insp_and_accept_report where ponum = '"+refNum+"'" 

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall() 
        
        if result == []:
            return None
        else:
            return result[0][0]   

    def getAllIARNumFromRef(self, refNum):
        
        sql = "select iarnum from insp_and_accept_report where ponum = '"+refNum+"' order by iarnum" 

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall() 
        
        if result == []:
            return None
        else:
            return result

    def getLatestDelDate(self, refNum):
        
        sql = "select max(receivedate) from insp_and_accept_report where ponum = '"+refNum+"'" 

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall() 
        
        if result == []:
            return None
        else:
            return result[0][0]   


#========= Receive Item Table Functions ================================================================================================

    def addReceiveItems(self, iarnum, description, quantity, unitprice, stockNum):
          
          sql = "insert into received_items values('"+iarnum+"',TRUE, '"+description+"',"+str(quantity)+", "+str(unitprice)+", "+str(stockNum)+")" 

          cur.execute(sql)
          connection.commit()
          print("Done adding items to Recieved Items")

    def getAvailableItems(self, iarnum):
        
        sql = "select * from received_items where iarnum = '"+iarnum+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result
    
    def getItemDetails(self, iarnum, itemnum):
        sql = "select * from received_items where iarnum = '"+iarnum+"' and itemnum = "+str(itemnum)+""

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result[0]
     

    def updateAvailableItems(self, iarnum, quantity, itemnum):
        sql = "update received_items set quantity = ((select quantity from received_items where iarnum = '"+iarnum+"' and itemnum = "+str(itemnum)+") - "+str(quantity)+") where iarnum = '"+iarnum+"' and itemnum = "+str(itemnum)+" "

        cur.execute(sql)
        connection.commit()
        print("Done")    

        
    def updateAvailability(self, iarnum, itemnum):
        
        itemDetails = InsepectionAndAcceptanceReceipt.getItemDetails(self, iarnum, itemnum)

        if itemDetails[3] == 0:
            
            sql = "update received_items set availability = FALSE where iarnum = '"+iarnum+"' and itemnum = "+str(itemnum)+""

            cur.execute(sql)
            connection.commit()

        print("Done")   

    def checkIARItemsDisburstComplete(self, iarnum):
         
        itemList =  InsepectionAndAcceptanceReceipt().getAvailableItems(iarnum)  

        disburstCompleteStatus = True
        print("list "+str(itemList))

        for x in itemList:
            if x[1] == True:
                disburstCompleteStatus = False
        

        return disburstCompleteStatus

if __name__ == "__main__":
    
    p = InsepectionAndAcceptanceReceipt()
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
    #print(p.getAllIARNumFromRef('004-17'))
    print(p.getLatestDelDate('Aujp-4090'))