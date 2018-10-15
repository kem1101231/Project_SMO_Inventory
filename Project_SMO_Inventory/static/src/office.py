# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$Dec 21, 2016 11:16:52 PM$"


from datetime import datetime

from connectdb import ConnectDB
from db_structure import dbTable

c = ConnectDB()
connection = c.connection()
cur = connection.cursor()

dbClass = None

class Offices:

    def __init__(self):


        dbClass = dbTable('offices')
      
        dbClass.column('id', 'varchar(25)', True)
        dbClass.column('name', 'varchar(255)', False)
        dbClass.column('type', 'varchar(25)', False)
        dbClass.column('head', 'varchar(25)', False)
        dbClass.column('authopersonel', 'varchar(25)', False)
        dbClass.column('division', 'varchar(25)', False)

        dbClass2 = dbTable('office_latest_trans')
        
        dbClass2.column('offid', 'varchar(15)', True)
        dbClass2.column('apppr', 'varchar(15)', False)
        dbClass2.column('ponum', 'varchar(15)', False)
        dbClass2.column('iarnum', 'varchar(15)', False)
        dbClass2.column('parnum', 'varchar(15)', False)
        dbClass2.column('risnum', 'varchar(15)', False)


    def addOffice(self, offid, name, offtype, head, authoPersonel, division):
        
        sql = "insert into offices values('{}', '{}', '{}', '{}', '{}', '{}')".format(offid, name, offtype.lower(), head, authoPersonel, division)
        
        cur.execute(sql)
        connection.commit()
        print("Done")

    def addOfficetoLatest(self, offid):
        
        sql = "insert into office_latest_trans values('{}')".format(offid)
        
        cur.execute(sql)
        connection.commit()
        print("Done")
   
    def updateLatestData(self, colname, coldata, offid):

        sql = "update office_latest_trans set "+colname+" = '"+coldata+"' where offid = '"+offid+"'"
        
        cur.execute(sql)
        connection.commit()
        print("Done")        


    def updateHead(self, offid, idnum):
        
        sql = "update offices set head = '{}' where id = '{}'".format(idnum, offid)
        
        cur.execute(sql)
        connection.commit()
        print("Done")        

    def updateAuthoPersonel(self, offid, idnum):
        
        sql = "update offices set authopersonel = '{}' where id = '{}'".format(idnum, offid)
        
        cur.execute(sql)
        connection.commit()
        print("Done")

    def getDepartments(self):
        
        sql = "select id from offices where type = 'department'"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        
        return result

    def getDepartmentByCollege(self, offid):
        
        sql = "select id from offices where type = 'department' and division = '"+offid+"' order by name"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        
        return result

    def getColleges(self):
        
        sql = "select id from offices where type = 'college' order by name"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        
        return result 

    def getAcademics(self):
        
        sql = "select id from offices where type = 'academics' order by name"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        
        return result

    def getOfficeHeadFromOffice(self, offid):
       
        sql = "select head from offices where id = '"+offid+"'"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        
        return result
    

    def getAdministratives(self):
        
        sql = "select id from offices where type = 'administrative' order by name"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        
        return result      

    def getAllOffices(self):
        
        sql = "select id from offices order by name"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        
        return result

    def getOfficeDetails(self, offid):
        
        sql = "select * from offices where id = '{}'".format(offid)

        cur.execute(sql)
        connection.commit()
        result = cur.fetchone()

        return result  

    def getAllOfficesSorted(self):
        
        output = []    

        colls = Offices.getColleges(self); 

        for x in colls:
            
            depts = Offices.getDepartmentByCollege(self,x[0])
            output = output + [(x[0],),] + depts

        output = output + Offices.getAcademics(self)  
        output = output + Offices.getAdministratives(self)

        return output  


if __name__ == '__main__':
        



        off = Offices()
        '''
        print("HHHHHHH")
        print(off.getAllOfficesSorted())
        print("HHHHHHH")
        print(off.getOfficeDetails('PROC'))
        
        colleges = off.getColleges()
        academics = off.getAcademics()
        administratives = off.getAdministratives()

        offices = colleges+academics+administratives

        print(colleges)
        print("  ")
        print(academics)
        print("  ")
        print(administratives)
        print("   ")
        print(offices)
        print("  ") 
        '''

        offList = off.getAllOffices()

        for x in offList:
            off.addOfficetoLatest(x[0])