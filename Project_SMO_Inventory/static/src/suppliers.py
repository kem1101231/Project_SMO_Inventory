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

class Suppliers:

    dbClass = None

    def __init__(self):
        
        self.dbClass = dbTable('suppliers')


        self.dbClass.column('compid','character varying(25)', True)
        self.dbClass.column('name','character varying(255)',False)
        self.dbClass.column('address','character varying(250)',False)
        self.dbClass.column('comprep','character varying(250)',False)
        self.dbClass.column('reptel','character varying(50)',False)
        self.dbClass.column('repemail','character varying(50)',False)
        self.dbClass.column('comptin','character varying(50)',False)
        self.dbClass.column('dateadded','date',False)
        self.dbClass.column('rating','integer',False)
        self.dbClass.column('ratingupdate','date',False)

    def addSupplier(self, name, address, comprep, reptel, repemail, comptin):
        
        compid = self.generateCompID()

        sql = "insert into suppliers values ('"+compid+"', '"+name+"', '"+address+"', '"+comprep+"', '"+reptel+"', '"+repemail+"', '"+comptin+"')"

        cur.execute(sql)
        connection.commit()
        print("Done")    

    def getSupllierDetails(self, compid):
        sql = "select * from suppliers where compid = '"+compid+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getSupllierName(self, compid):
        sql = "select name from suppliers where compid = '"+compid+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getAllSuppliers(self):
        
        sql = "select * from suppliers"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result 

    def updateSupplierBasicInfo(self, suppID, name, address):
       
        sql = "update suppliers set name = '"+name+"', address = '"+address+"' where compid = '"+suppID+"'"

        cur.execute(sql)
        connection.commit()        


    def updateSupplierRepInfo(self, suppID, comprep, reptel, repemail):
       
        sql = "update suppliers set comprep = '"+comprep+"', reptel = '"+reptel+"', repemail = '"+repemail+"' where compid = '"+suppID+"'"

        cur.execute(sql)
        connection.commit()        
    
    def updateSupplierTINInfo(self, suppID, tin):
       
        sql = "update suppliers set comptin = '"+tin+"' where compid = '"+suppID+"'"

        cur.execute(sql)
        connection.commit()        

    def getCompIDfromName(self, name):
        
        sql = "select compid from suppliers where name = '"+name+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        if result == []:
            return None
        else:
            return result[0][0]
             
    
    def findCompName(self, name):
         
        sql = "select name, compid from suppliers where lower(name) like lower('%"+name+"%')"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result        


    def findCompRepName(self, name):
         
        sql = "select comprep, compid, name from suppliers where lower(comprep) like lower('%"+name+"%')"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result        


    def generateCompID(self):
        
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

        