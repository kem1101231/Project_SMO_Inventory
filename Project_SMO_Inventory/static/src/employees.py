from connectdb import ConnectDB
from db_structure import dbTable

c = ConnectDB()
connection = c.connection()
cur = connection.cursor()



class Employees:

    dbClass = None

    def __init__(self):

      self.dbClass = dbTable('employees')
      
      self.dbClass.column('idnum', 'varchar(15)', True)
      self.dbClass.column('fname', 'varchar(100)', False)
      self.dbClass.column('sname', 'varchar(100)', False)
      self.dbClass.column('designation', 'varchar(100)', False)
      self.dbClass.column('dept', 'varchar(50)', False)
      self.dbClass.column('rank', 'varchar(25)', False)
      self.dbClass.column('title', 'varchar(25)', False)
      self.dbClass.column('mname', 'varchar(100)', False)
      self.dbClass.column('suffix', 'varchar(10)', False)
      self.dbClass.column('picfile', 'varchar(255)', False)

    def addNewEmployee(self, inputList):
        sqlCols = ""
        sqlVals = ""

        for x in inputList:
            
            listData = inputList[x]
            
            if sqlCols != "":
              sqlCols = sqlCols + ", "
            
            sqlCols = sqlCols + x  

            if sqlVals != "":
              sqlVals = sqlVals + ", "
            
            valData = ""
            
            if listData[1] == "int":
              valData = str(listData[0])
            else:
               valData = "'"+str(listData[0])+"'"   

            sqlVals = sqlVals + valData

        sql = "insert into employees (" + sqlCols + ") values (" + sqlVals + ")"
        self.dbClass.executeUpdate(sql)   
               

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


    def updateEmpPic(self, empPic, empid):
        sql = "update employees set picfile = '"+empPic+"' where idnum = '"+empid+"'"
        cur.execute(sql)
        connection.commit()

        print("Done")

    def transferEmployeeToOffice(self, idnum, offid):
        sql = "update employees set dept = '"+offid+"' where idnum = '"+idnum+"'"
        self.dbClass.executeUpdate(sql)
        print("Done")

if __name__ == '__main__':
  Employees()