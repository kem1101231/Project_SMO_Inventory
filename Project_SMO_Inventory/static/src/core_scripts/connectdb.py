# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$10 31, 16 3:15:04 PM$"


import psycopg2
import sys
 
class ConnectDB:
    
    def connection(self):
        
        conn_string = "host='localhost' dbname='Project_SMO_Inventory' user='postgres' password='heathcliff'"
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
	
        return conn


if __name__ == '__main__':
	c = ConnectDB()
	print(c.connection())