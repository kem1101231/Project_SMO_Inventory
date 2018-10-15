# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Arius_EX"
__date__ = "$Dec 21, 2016 11:16:52 PM$"


from datetime import datetime

import random
import string
from random import randint

from connectdb import ConnectDB


c = ConnectDB()
connection = c.connection()
cur = connection.cursor()

class LiquidatingDamages:
    
    def addLD(self, ponum, iarnum, damageCost, delayDays):

        ldcode = LiquidatingDamages.genLDCode(self)
        currentdate = datetime.now().strftime('%Y-%m-%d')
        
        sql = "insert into liquidating_damages values('{}', '{}', '{}', {}, {}, '{}')".format(ldcode,  ponum, iarnum, damageCost, delayDays, currentdate)
        
        cur.execute(sql)
        connection.commit()
        print("Done")

    
    def genLDCode(self):
        
        genIDNum = LiquidatingDamages.generateIDNum(self)

        while LiquidatingDamages.isLDCodeExist(self, genIDNum):
                notifNum = Functions.generateIDNum(self)

        return genIDNum


    def getLiqDamageFromPO(self, refNum):
        sql = "select sum(damage_cost) from liquidating_damages where ponum = '"+refNum+"'"   

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result
    
    def getLiqDamageListFromPO(self, refNum):
        sql = "select * from liquidating_damages where ponum = '"+refNum+"' order by datecreated"   

        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()

        return result



    def isLDCodeExist(self, ref):
        
        sql = "select ldcode from liquidating_damages where ldcode = '"+ref+"'"

        cur.execute(sql)
        connection.commit()
        r = cur.fetchall()

        if r == []:
            return False
        else:
            return True    

    def generateIDNum(self):
        
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

        

if __name__ == '__main__':
    print(LiquidatingDamages().getLiqDamageFromPO('001-18'))