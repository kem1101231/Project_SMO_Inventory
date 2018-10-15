import os.path
from Project_SMO_Inventory.static.src import connectdb
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

c = ConnectDB()
if __name__ == '__main__':
	print("Path")
	print(str(SITE_ROOT))
	print(c.connection())