# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$10 31, 16 3:14:51 PM$"


from connectdb import ConnectDB
from db_structure import dbTable


c = ConnectDB()
connection = c.connection()
cur = connection.cursor()



class User:
    
    dbClass = None
    
    def __init__(self):

      self.dbClass = dbTable('users')
      
      self.dbClass.column('uname', 'varchar(50)', True)
      self.dbClass.column('pass', 'varchar(50)', False)
      self.dbClass.column('idnum', 'varchar(15)', False)
      self.dbClass.column('access_type', 'integer[]', False)
      self.dbClass.column('profile_pic', 'bytea', False)
      self.dbClass.column('status', 'boolean', False)

      #===================================================================

      dbClassDev = dbTable('devusers')
      
      dbClassDev.column('uname','character varying(25)', True)
      dbClassDev.column('password','character varying(50)', False)
      dbClassDev.column('acctype','integer',False)
      dbClassDev.column('name','character varying(255)',False)
    
    def addUser(self, uname, password, idnum, acctype):
        
       sql = "insert into users values('"+uname+"', '"+password+"', '"+idnum+"','{"+str(acctype)+"}')"             
    
       cur.execute(sql)
       print (sql)
       connection.commit()
       print ("Done")
       
 
    def removeUser(self):
        sql = "insert into users values('{}', '{}', '{}','{"+' '.join(map(str, acctype))+"}')".format(uname, password, id, acctype)             
    
        cur.execute(sql)
        print (sql)
        connection.commit()
        print ("Done")
    
    def updateUserPass(self, uname, newPass):
    
       sql = "update users set pass = '{}' where uname = '{}'".format(newPass, uname)             
    
       cur.execute(sql)
       print (sql)
       connection.commit()
       print ("Done")
    


    def updateUserPic(self, picture):
        pass

    def isUserRegistered(self, uname):
        
        sql = "select uname from users where uname = '{}'".format(uname)
    
        cur.execute(sql)
        connection.commit()
        r = cur.fetchall()
        
        if r == []:
            return False
        else:
            return True
    
    def isIDRegistered(self, idnum):
       
        sql = "select uname from users where idnum = '{}'".format(idnum)
    
        cur.execute(sql)
        connection.commit()
        r = cur.fetchall()
        
        if r == []:
            return False
        else:
            return True       
        
    def updateUserStatus(self, uname, status):
        sql = "update users set status = "+status+" where uname = '"+uname+"'"

        cur.execute(sql)
        connection.commit()

        print("Done")

    def checkUserPass(self, uname, password):
         
         sql = "select pass from users where uname = '{}'".format(uname)
         
         cur.execute(sql);
         connection.commit()
         result = cur.fetchone()
        
         if result[0] == password:
             return True
         else:
             return False

    def getUserDetails(self, referenceString):
       
       sql = "select * from users where uname = '{}'".format(referenceString)
       cur.execute(sql)
       connection.commit()
       result = cur.fetchall()
       
       return result

    def getUserDetailsFromID(self, referenceString):
       
       sql = "select * from users where idnum = '{}'".format(referenceString)
       cur.execute(sql)
       connection.commit()
       result = cur.fetchall()
       
       return result       
    
    def getUnameFromID(self, idnum):
        
        sql = "select uname from users where idnum = '{}'".format(idnum)
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
       
        return result

    def getProcUsers(self):
        
        sql = "select idnum from users where access_type[0] = 2 or access_type[1] = 2 or access_type[2] = 2 or access_type[3] = 2"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getSMOUsers(self):
        
        sql = "select idnum from users where access_type[0] = 3 or access_type[1] = 3 or access_type[2] = 3 or access_type[3] = 3 or access_type[0] = 31 or access_type[1] = 31 or access_type[2] = 31 or access_type[3] = 31 or access_type[0] = 32 or access_type[1] = 32 or access_type[2] = 32 or access_type[3] = 32 or access_type[0] = 33 or access_type[1] = 33 or access_type[2] = 33 or access_type[3] = 33 or access_type[0] = 34 or access_type[1] = 34 or access_type[2] = 34 or access_type[3] = 34 or access_type[0] = 35 or access_type[1] = 35 or access_type[2] = 35 or access_type[3] = 35"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result 

    def getSMOInvenUsers(self):
        
        sql = "select idnum from users where access_type[0] = 31 or access_type[1] = 31 or access_type[2] = 31 or access_type[3] = 31"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result
    
    def getSMOAdminUser(self):
        
        sql = "select idnum from users where access_type[0] = 3 or access_type[1] = 3 or access_type[2] = 3 or access_type[3] = 3"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result
      

    def getUserbyAccesType(self, accessTypeNum):
        
        sql = "select idnum from users where access_type[0] = "+accessTypeNum+" or access_type[1] = "+accessTypeNum+" or access_type[2] = "+accessTypeNum+" or access_type[3] = "+accessTypeNum+" or access_type[4] = "+accessTypeNum+" or access_type[5] = "+accessTypeNum+" or access_type[6] = "+accessTypeNum+" or access_type[7] = "+accessTypeNum+" or access_type[8] = "+accessTypeNum+" or access_type[9] = "+accessTypeNum+";"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result

    def getNumOfAccessType(self, uname):
        
        sql = "SELECT array_length(access_type, 1) FROM users where uname = '"+uname+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result   

    def getAccessType(self, uname):
        
        sql = "SELECT access_type FROM users where idnum = '"+uname+"'"

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result         

    def addUserAccessType(self, uname, acctype):
        
        index = User.getNumOfAccessType(self, uname)

        sql = "update users set access_type["+str(index+1)+"] = "+str(acctype)+" where uname = '"+uname+"'"

        cur.execute(sql)
        connection.commit()
        print("Done")

    def removeUserAccessType(self,uname, acctype):
        
        sql = "UPDATE users SET access_type = array_remove(access_type, "+str(acctype)+") where uname = '"+uname+"';"

        cur.execute(sql)
        connection.commit()
        print("Done")         

    def updateUserAccessType(self, idnum, oldAcctype, newAcctype):
        
        sql = "UPDATE users SET access_type = array_replace(access_type, (select access_type[1] from users where idnum = '"+idnum+"'), "+str(newAcctype)+") where idnum = '"+idnum+"';"

        cur.execute(sql)
        connection.commit()
        print("Done")     

    def getAllUsers(self):
          sql = "select * from users order by uname"

          cur.execute(sql)
          connection.commit()
          result = cur.fetchall()

          return result 

    def checkAdminUser(self):
        sql = "select uname from users where access_type = '{0}'"
        result = self.dbClass.executeQuery(sql)

        if result == []:
            return False
        else:
            return True


if __name__ == "__main__":
    
    u = User()
    #d = u.isUserRegistered("kem1101231")
    #print (d)
    #ee = u.checkUserPass("kem1101", "condiminaheathcliff" )
    #u.updateUserPass("kem1101","condigago")
    #print (u.getUserDetails("kem1101"))
    #print (ee)
    #print ("Hello World")
    #print(u.getAccessType('2011-0813'))
    #u.updateUserAccessType('2011-0813', 0, 5)
    print(u.checkAdminUser())