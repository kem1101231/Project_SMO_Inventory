# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$10 31, 16 3:15:04 PM$"


import pymysql
import pymysql.cursors
 
class ConnectMyDB:
   
    def connection(self):
    	
    	conn= pymysql.connect(host='localhost',user='root',password='',db='hrdb',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    	cursor =  conn.cursor()

    	return conn


if __name__ == '__main__':
	c = ConnectDB()
	c.connection()