from connectdb import ConnectDB

c = ConnectDB()
connection = c.connection()
cur = connection.cursor()

class KeyPositions:
	
	def getChancellor(self):

		sql = "select empid from keypositions where id = 'chancellor'"
		cur.execute(sql)
		connection.commit()
		r = cur.fetchone()

		return r[0]
	
	def getChancellorRep(self):

		sql = "select empid from keypositions where id = 'chancerep'"
		cur.execute(sql)
		connection.commit()
		r = cur.fetchone()

		return r[0]

	def setChancellor(self, idnum):
       	
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

		return r[0]
	
	def getVCAFRep(self):

		sql = "select empid from keypositions where id = 'vcafrep'"
        
		cur.execute(sql)
		connection.commit()
		r = cur.fetchone()

		return r[0]

	def setVCAF(self, idnum):
       	
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