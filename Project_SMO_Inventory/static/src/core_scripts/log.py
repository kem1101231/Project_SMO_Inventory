import random
import string
from random import randint

from connectdb import ConnectDB

c = ConnectDB()
connection = c.connection()
cur = connection.cursor()

class Log:
    
	def generateLogID(self):
        
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

	def addLog(self, idnum):
        
		logid = Log.generateLogID(self)
		print(logid)

		if Log.checkIdExist(self,logid):
			logid = generateLogID()

		sql = "insert into log values('{}', '{}', null, null)".format(logid, idnum)             
    
		cur.execute(sql)
		connection.commit()

		return logid
		print ("Done") 
    
	def getLogDetails(self, logid): 
        
		sql = "select * from log where logid = '{}'".format(logid)
        
		cur.execute(sql)
		connection.commit()
		result = cur.fetchall()
       
		return result
    
	def checkIdExist(self, logid):
		
		sql = "select logid from log where logid = '{}'".format(logid)
    
		cur.execute(sql)
		connection.commit()
		r = cur.fetchall()
        
		if r == []:
			return False
		else:
			return True


if __name__ == '__main__':
	
	l = Log()
	idgen = l.generateLogID()
	pp = l.addLog('2011-0813', 4)
	print(idgen)
	print(pp)
	