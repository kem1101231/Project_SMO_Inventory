from notifications import Notification
import datetime

n = Notification()
def setNotifDetails(idnum):
    
    outputList = []

    notifList = n.getNotifOfPersonnel(idnum)

    for x in notifList:
      print(type(x))
      
      kk = n.getNotifDisplayDetails(x[0])
      print(type(kk[0]))
      print(kk[0])

      ll = ()

      print(x[0])
        
      ll = (x[0],)

      if kk[0][0] == '1':
        ll = ll + ('icon-ok',)
      if kk[0][0] == '2':
          ll = ll + ('icon-legal',)
      if kk[0][0] == '3':
          ll = ll + ('icon-info',)
      if kk[0][0] == '4':
          ll = ll + ('icon-truck',)
      if kk[0][0] == '5':
          ll = ll + ('icon-exclamation',)
      
      if kk[0][1] == '1':
        ll = ll + ('success',)
      if kk[0][1] == '2':
          ll = ll + ('info',)
      if kk[0][1] == '3':
          ll = ll + ('danger',)
      if kk[0][1] == '4':
          ll = ll + ('warning',)
      
      ll = ll + (kk[0][2],kk[0][3],kk[0][4],) 
      
      #details = tuple(kk)
      print('/---------------------')
      print(ll)

      print('=============================')
      outputList = outputList + [ll]

    return outputList

class Test():
      def test1(self, input):
          return input

if __name__ == '__main__':

      print(Test().test1('uuu'))

      print(setNotifDetails('2013-0211'))  
      