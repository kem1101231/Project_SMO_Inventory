from connectdb import ConnectDB
from db_structure import dbTable

c = ConnectDB()
connection = c.connection()
cur = connection.cursor()

dbClass = None

class KeyPositions:

	def __init__(self):
		
		dbClass = dbTable('keypositions')
		
		dbClass.column('id','varchar(10)',True)
		dbClass.column('empid','varchar(15)',False)


	
	def getChancellor(self):

		sql = "select empid from keypositions where id = 'chancellor'"
		cur.execute(sql)
		connection.commit()
		r = cur.fetchone()

		if r != None:
			return r[0]
		else:
			return r

	
	def getChancellorRep(self):

		sql = "select empid from keypositions where id = 'chancerep'"
		cur.execute(sql)
		connection.commit()
		r = cur.fetchone()
		
		if r != None:
			return r[0]
		else:
			return r

	def setChancellor(self, idnum):
		sql = ""

		if KeyPositions.getChancellor(self) == None:
			sql = "insert into keypositions values('chancellor','{}')".format(idnum)
		else:
			sql = "update keypositions set empid = '{}' where id = 'chancellor'".format(idnum)             
    
		cur.execute(sql)
		print (sql)
		connection.commit()
		print ("Done")

	def getVCAF(self):

		sql = "select empid from keypositions where id = 'vcaf'"
        
		cur.execute(sql)
		connection.commit()
		r = cur.fetchone()
		
		if r != None:
			return r[0]
		else:
			return r

	
	def getVCAFRep(self):

		sql = "select empid from keypositions where id = 'vcafrep'"
        
		cur.execute(sql)
		connection.commit()
		r = cur.fetchone()

		if r != None:
			return r[0]
		else:
			return r

	def setVCAF(self, idnum):
		sql = ""
		if KeyPositions.getVCAF(self) == None:
			sql = "insert into keypositions values('vcaf', '{}')".format(idnum)
		else:
			sql = "update keypositions set empid = '{}' where id = 'vcaf'".format(idnum)             
    
		cur.execute(sql)
		print (sql)
		connection.commit()
		print ("Done")

	def getVCAA(self):

		sql = "select empid from keypositions where id = 'vcaa'"
		
		cur.execute(sql)
		connection.commit()
		r = cur.fetchone()

		return r[0]

	def setVCAA(self, idnum):
       	
		sql = "update keypositions set empid = '{}' where id = 'vcaa'".format(idnum)             
    
		cur.execute(sql)
		print (sql)
		connection.commit()
		print ("Done")	

if __name__ == '__main__':
	 k = KeyPositions()
	 print(k.getVCAFRep())		