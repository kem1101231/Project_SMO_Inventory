from os.path import dirname, abspath
import sys

print(dirname(dirname(abspath(__file__))))
sys.path.append(dirname(dirname(abspath(__file__))))

from SuperUser.testInheritance import Test



if __name__ == '__main__':
	Test().printThis()