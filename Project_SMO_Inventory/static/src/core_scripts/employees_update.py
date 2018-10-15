from connectdb import ConnectDB
from connectmydb import ConnectMyDB

c = ConnectDB()
myc = ConnectMyDB()

connection = c.connection()
cur = connection.cursor()

myconnection = myc.connection()
mycur = myconnection.cursor()

class Employees:
    
    
    def addEmployee(self, idnum, fname, sname, designation, dept, mname):
        
       sql = "insert into employees values('{}', '{}', '{}','{}', NULL, NULL, '', '{}','')".format(idnum, fname, sname,  dept, mname)             
    
       cur.execute(sql)
       print (sql)
       connection.commit()
       print ("Done")
    
    
    def getEmployeesFromMyDB(self):
        
        sql = "select DISTINCT(ee.employee_id), ee.emp_firstname, ee.emp_lastname, ee.emp_middle_name, (select job_description from ohrm_job_title where id = ee.job_title_code) job, emp_number from hs_hr_employee ee"  

        mycur.execute(sql)
        myconnection.commit()
        result = mycur.fetchall()

        return result

if __name__ == '__main__':
  emp = Employees()
  empList = emp.getEmployeesFromMyDB()

  empListCheck = ()

  for x in empList:
    print("/=================================================")
    print(x)
    print("/=================================================")
    print(x['employee_id'])
    
    toSQLId = str(x['employee_id'])

    if x['employee_id'] in empListCheck:
      print("Duplicate Found")
      toSQLId = str(x['employee_id'])+"-"+str(x['emp_number'])
    
    empListCheck = empListCheck + (x['employee_id'],)  

    if x['employee_id'] == None or x['employee_id'] == '' or x['employee_id'] == '-':
      print(str(x['emp_number']))
      toSQLId = str(x['emp_number'])
    
    print(x['emp_middle_name'])
    
    toSQLMName = x['emp_middle_name']
    
    if x['emp_middle_name'] != '':
        toSQLMName = x['emp_middle_name'][0]+"."  
    
    print("toSQLId: "+str(toSQLId))
    emp.addEmployee(toSQLId, x['emp_firstname'], x['emp_lastname'], x['job'], None, toSQLMName)

  
  print(empListCheck)
  print()  

  print(len(empList))  
  print("Done")  