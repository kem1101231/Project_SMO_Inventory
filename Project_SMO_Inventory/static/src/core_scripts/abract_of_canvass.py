#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$11 12, 16 7:40:45 PM$"

from connectdb import ConnectDB

c = ConnectDB()
connection = c.connection()
cur = connection.cursor()


class AbstractOfCanvass:
    
    def addAbstract(self):
        pass

if __name__ == "__main__":
    print "Hello World";
