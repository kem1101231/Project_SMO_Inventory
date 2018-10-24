# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$10 31, 16 3:15:04 PM$"


import sys

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 


class ConnectDB:
	
	# ===================================
	# Update the following Data to set the Database

	uname = 'odoo'
	password = 'odoo'
	host = 'localhost'
	dbname = 'project_smo_inventory'

	# ===================================


	conn = None	

	def __init__(self):
		
		try:
			self.conn = psycopg2.connect(dbname = self.dbname,
									user = self.uname, 
									host = self.host, 
									password = self.password)

		except Exception as e:

			ConnectDB.createDB(self)
			
			self.conn = psycopg2.connect(dbname = self.dbname,
									user = self.uname, 
									host = self.host, 
									password = self.password)


	def createDB(self):
		
		con = psycopg2.connect(dbname = 'postgres', user = self.uname, host = self.host, password = self.password)
		con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

		cur = con.cursor()
		cur.execute("CREATE DATABASE {} ;".format(self.dbname))

	def connection(self):
		return self.conn


'''
 Final update: 
	Date: May 26, 2018
	Time: 3:02 AM 	
'''