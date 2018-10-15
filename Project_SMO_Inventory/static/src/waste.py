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
from db_structure import dbTable

c = ConnectDB()
connection = c.connection()
cur = connection.cursor()

dbClass = None

class Waste:

    def __init__(self):

        dbClass = dbTable('waste_mat_report')
      
        dbClass.column('reqnum','character varying(10)', True)
        dbClass.column('wmrnum','character varying(10)', False)
        dbClass.column('datecreated','date', False)
        dbClass.column('requestid','character varying(10)', False)
        dbClass.column('parref','character varying(10)', False)
        dbClass.column('status','boolean', False)
        dbClass.column('status_date','date', False)
        dbClass.column('inspetor','character varying(10)', False)
        dbClass.column('counter','integer', False)

        #=============================================================================

        dbClassItems = dbTable('wmr_items')

        dbClassItems.column('reqnum','character varying(10)', False)
        dbClassItems.column('invnum','integer', False)


    def addWMRReport(self, reqNum, reqID, parref):
        
        currentdate = datetime.now().strftime('%Y-%m-%d')

        sql = "insert into waste_mat_report values ('"+reqNum+"', NULL, '"+str(currentdate)+"', '"+reqID+"', '"+parref+"', NuLL, NULL, NULL, 0)"

        cur.execute(sql)
        connection.commit()
        print("Done")    

    def addWMRReportWithIns(self, reqNum, reqID, parref, insID):
        
        currentdate = datetime.now().strftime('%Y-%m-%d')

        sql = "insert into waste_mat_report values ('"+reqNum+"', NULL, '"+str(currentdate)+"', '"+reqID+"', '"+parref+"', NuLL, NULL, '"+insID+"', 0)"

        cur.execute(sql)
        connection.commit()
        print("Done")    


    def updateStatus(self, reqID, statusData, insID):

        currentdate = datetime.now().strftime('%Y-%m-%d')
        sql = "update waste_mat_report set status = '"+statusData+"', status_date = '"+currentdate+"', inspetor = '"+insID+"'   where  reqnum = '"+reqID+"'"

        cur.execute(sql)
        connection.commit()
        print("Done")    

    def getWMRIDFromWMRNum(self, wmrref):
        
        sql = "select id from waste_mat_report where wmrnum= '"+wmrref+"'"  

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        outData = ''

        if result == []:
            outData = None
        else:
            return result[0][0]
        
    def getWMRDetails(self, reqnum):
        sql = "select * from waste_mat_report where reqnum = '"+reqnum+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getAllWMRwithDetails(self):
        sql = "select * from waste_mat_report"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result
    
    def getAllWMR(self):
        sql = "select reqnum from waste_mat_report"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result
    

    def addWMRItem(self, reqnum, invnum):
        
        sql = "insert into wmr_items values('"+reqnum+"','"+str(invnum)+"')"

        cur.execute(sql)
        connection.commit()
        print("Done")

    def getWMRItems(self, reqnum):
        
        sql = "select * from wmr_items where reqnum = '"+reqnum+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def generateWMRID(self):
        
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

        