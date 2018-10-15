
from connectdb import ConnectDB

cdb = ConnectDB()

connection = cdb.connection()
cur = connection.cursor()

class dbTable:

    dbname = None

    def __init__(self, dbname):
        
        self.dbname = dbname
        sql = "create table if not exists " + dbname + "()" 
        dbTable.executeUpdate(self, sql)    
    

    def column(self, columnname, datatype, pkey):
        
        try:

            sqlwhilesy = "alter table " + self.dbname + "  add column " + columnname + " " + datatype +";"
            
            if pkey == True:
              sqlwhilesy = sqlwhilesy + "alter table " + self.dbname + " alter column " + columnname + " set not null; alter table " + self.dbname + " ADD PRIMARY KEY (" + columnname + ");"

            sql = "DO $$ BEGIN BEGIN " + sqlwhilesy + " EXCEPTION WHEN duplicate_column THEN RAISE NOTICE ''; END; END;$$"

            dbTable.executeUpdate(self, sql)
            
        except Exception as e:
            raise e


    def executeUpdate(self, sql):
         
          try:
            cur.execute(sql)
            connection.commit()

          except Exception as e:
            raise e

    def executeQuery(self, sql):
         
          try:
            cur.execute(sql)
            connection.commit()
            result = cur.fetchall()
            
            return result

          except Exception as e:
            raise e
      

