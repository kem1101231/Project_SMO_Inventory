# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$10 31, 16 3:15:04 PM$"


import sys

import psycopg2
import psycopg2.extras


if __name__ == '__main__':
	
	uname = 'postgres'
	password = 'heathcliff'
	host = 'localhost'
	dbname = 'project_smo_inventory'

	DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (host, dbname, uname, password)
	dbConn = psycopg2.connect(DB_CONNECTION_STRING)
	cur = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
	qSelect = "SELECT * from users"
	cur.execute(qSelect)
	results = cur.fetchall()

	print(results)
	for row in results:
		print(row[''])
