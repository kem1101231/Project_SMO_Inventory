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

class Tasks:

    def __init__(self):

        dbClass = dbTable('transactions')

        dbClass.column('id','character varying(15)', True)
        dbClass.column('transtype','character varying(25)', False)
        dbClass.column('by','character varying(15)', False)
        dbClass.column('transdate','date', False)
        dbClass.column('transtime','time without time zone', False)
        dbClass.column('title','character varying(255)', False)
        dbClass.column('msg1','character varying(255)', False)
        dbClass.column('msg2','character varying(255)', False)
        dbClass.column('reftransnum','character varying(15)', False)


    
    def addTrans(self, idnum, transtype, byid):
        
        currentdate = datetime.now().strftime('%Y-%m-%d')
        currenttime = datetime.now().strftime('%H:%M')

        sql = "insert into transactions values('{}','{}','{}','{}','{}')".format(idnum, transtype, byid, currentdate, currenttime)             
        
        print (sql)
        cur.execute(sql)
        connection.commit()
        print ("Done") 
    
    def getTaskDetails(self, notifnum): 
        sql = "select * from transactions where id = '{}'".format(notifnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result
    
    def getTransOfPersonnel(self,idnum):
        
        sql = "select * from transactions where by = '{}' order by (transdate)DESC".format(idnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def getAllNotifsOfPersonel(self, idnum):
       
        sql = "select notifnum from notifications where toid = '{}' and type = 2 order by (dateofnotif)DESC ".format(idnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def getNotifNum(self, idnum):
        sql = "select COUNT(notifnum) from notifications where toid = '{}' and type = 2 and status = FALSE".format(idnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result
    
    def getTaskOfPersonel(self, idnum):
        
        sql = "select notifnum from notifications where toid = '{}' and type = 1 and status = FALSE order by (dateofnotif)DESC".format(idnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result
    
    def getTaskNum(self, idnum):
        
        sql = "select COUNT(notifnum) from notifications where toid = '{}' and type = 1 and status = FALSE".format(idnum)
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result
    
    def updateNotif(self, notifnum):
        
        sql = "update notifications set status = 'TRUE' where notifnum = '{}'".format(notifnum)             
    
        cur.execute(sql)
        connection.commit()
        print ("Done")

    def createNotifRef(self, trans, transnum):
        pass
        
    
    def getTransFromNotifRef(self,notifref):
        pass
    

    def getNotifDisplayDetails(self, notifnum):
        
        sql = "select details from notifications where notifnum = '{}';".format(notifnum)

        cur.execute(sql)
        connection.commit()
        result = cur.fetchone()
        
        return result

    def getTaskDisplayDetails(self, notifnum):
        
        sql = "select details from notifications where notifnum = '{}';".format(notifnum)

        cur.execute(sql)
        connection.commit()
        result = cur.fetchone()
        
        return result    

    def isNotifNumExist(self, ref):
        
        sql = "select notifnum from notifications where notifnum = '"+ref+"'"

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

    def getNotifFromData(self, ref, toid):
        
        sql = "select notifnum from notifications where notifref = '"+ref+"' and toid = '"+toid+"';"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getNotifFromDataWithRef(self, ref, toid, reftype):
        
        sql = "select notifnum from notifications where notifref = '"+ref+"' and toid = '"+toid+"' and reftype = '"+reftype+"';"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getHotifTimeAndDate(self, notifnum):
    
        sql = "select dateofnotif, timeofnotif from notifications where notifnum = '"+notifnum+"';"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result


if __name__ == '__main__':
    
        n = Notification()
        
        numID = n.generateIDNum()
        print("boolean "+str(n.isNotifNumExist(numID)))
        while n.isNotifNumExist(numID):
            numID = n.generateIDNum()  
            print("new gennum"+numID) 
        
        print(numID)
        n.adNotif(numID, '','2013-0211', '1', 'XGkk-6170', "ARRAY ['1','1','Date of Req.: "+datetime.strptime('2017-02-02',"%Y-%m-%d").strftime("%B %d, %Y")+"','PR no.: XGkk-6170','Your Purchase Request was Approved']",'2','pr')      

        print('//======'+str(n.getNotifOfPersonnel('2017-0823')))
        print('//======'+str(n.getTaskOfPersonel('2017-0823')))

