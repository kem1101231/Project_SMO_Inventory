from os.path import dirname, abspath
import sys


dirreq = dirname(dirname(abspath(__file__)))

class PathConfig:
        def __init__(self):
            #config python file path for Ubuntu machines
            sys.path.append('{}/Project_SMO_Inventory/static/src'.format(dirreq))

            #configure python file path for Windows machines
            sys.path.append('{}\Project_SMO_Inventory\static\src'.format(dirreq))
