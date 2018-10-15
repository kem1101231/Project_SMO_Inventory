# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$Dec 21, 2016 11:16:52 PM$"


from datetime import datetime

from connectdb import ConnectDB

c = ConnectDB()
connection = c.connection()
cur = connection.cursor()

class Offices:
    
    def addOffice(self, offid, name, offtype, head, authoPersonel, division):
        
        sql = "insert into offices values('{}', '{}', '{}', '{}', '{}', '{}')".format(offid, name, offtype, head, authoPersonel, division)
        
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
        
        sql = "select id from offices where type = 'department' and division = '"+offid+"'"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        
        return result

    def getColleges(self):
        
        sql = "select id from offices where type = 'college'"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        
        return result 

    def getAcademics(self):
        
        sql = "select id from offices where type = 'academics'"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        
        return result

    def getAdministratives(self):
        
        sql = "select id from offices where type = 'administrative'"
        
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        
        return result      

    def getAllOffices(self):
        
        sql = "select id from offices "
        
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

if __name__ == '__main__':
        



        off = Offices()
        

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
