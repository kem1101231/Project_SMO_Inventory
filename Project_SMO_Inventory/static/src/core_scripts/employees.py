from connectdb import ConnectDB

c = ConnectDB()
connection = c.connection()
cur = connection.cursor()

class Employees:
    
    
    def addEmployee(self, idnum, fname, sname, designation, dept, mini, rank, title, suffix):
        
       sql = "insert into employees values('{}', '{}', '{}','{}','{}','{}','{}','{}','{}')".format(idnum, fname, sname, designation, dept, rank, title, mini, suffix)             
    
       cur.execute(sql)
       print (sql)
       connection.commit()
       print ("Done")
  
    def isUserRegistered(self, idnum):
        
        sql = "select idnum from employees where idnum = '{}'".format(idnum)
    
        cur.execute(sql)
        connection.commit()
        r = cur.fetchall()
        
        if r == []:
            return False
        else:
            return True
    
    def getAllEmployeeID(self):
       
       sql = "select idnum from employees"
       cur.execute(sql)
       connection.commit()
       result = cur.fetchall()
       
       return result          
    
    def getEmployeeDetails(self, referenceString):
       
       sql = "select * from employees where idnum = '{}'".format(referenceString)
       cur.execute(sql)
       connection.commit()
       result = cur.fetchall()
       
       return result
    
    def getIDnumFromName(self, fname, sname):
        
        sql = "select idnum from employees where fname = '"+fname+"' and sname = '"+sname+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result[0][0]

    def findEmployee(self, inputData):
        
        sql = "select distinct(idnum), sname, fname from employees where idnum like '"+inputData+"%' or lower(fname) like lower('%"+inputData+"%') or lower(sname) like lower('%"+inputData+"%');" 

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result  

    def getEmployeeByOff(self, offid):
          sql = "select idnum from employees where dept = '"+offid+"'"

          cur.execute(sql)
          connection.commit()
          result = cur.fetchall()

          return result