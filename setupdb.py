# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$10 31, 16 3:15:04 PM$"


import sys

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 
import getpass

if __name__ == '__main__':
	
	print("\n••••••••••••••••••••••••••••••••\n")
	print("Were setting up your application. Please provide the following infomation asked to set up the server.\n")

	host_address = input("Database server's address: ")
	port_number = int(input("Port number: "))
	dbname = input('Database Name: ')	
	
	print("\n••••••••••••••••••••••••••••••••\n")
	print('Now, please provide your access account to the database.\n')
	
	uname = input('Username: ')
	password = getpass.getpass('Password: ')	
	
	try:
		con = psycopg2.connect(dbname = dbname, user = uname, host = host_address, port=port_number, password = password)
		print("It seems that you already finished setting up the server for this application.\n")

	except Exception as e:

		ans = input("The database you wish to access doesn't exist.\nDo you want to create the database? [y-yes/n-no]")

		if ans in ['y','yes','YES']:
			print("Preraring database ................")

			con = psycopg2.connect(dbname = 'postgres', user = uname, host = host_address, port=port_number, password = password)
			con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

			cur = con.cursor()
			cur.execute("CREATE DATABASE {} ;".format(dbname))

			file = open("Project_Govnt_Inventory/db_access.txt","w+")
			file.write(host_address+"\n")
			file.write(str(port_number)+"\n")
			file.write(dbname+"\n")
			file.write(uname+"\n")
			file.write(password+"\n")

			print("Database created.")

		else:
			print("\n••••••••••••••••••••••••••••••••\n")
			print("Seriourly!?\n..............\nWe can't proceed any futher than here.\nYou may come back setting up your server once you had make up your mind.\nGood day.\n")


	
