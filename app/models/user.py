from copy import deepcopy
class User:

  def __init__(self,*args):
    self.__dict__.update(args[0])
  
  def stringify(self):
    userDct = self.__dict__
    userDct.pop('password')
    for i in userDct:
      userDct.update({i : str(userDct[i])})
    return userDct

  def dictParse(self):
    tempDct =  deepcopy(self.__dict__)
    tempDct.pop('password')
    tempDct.pop('email')
    return tempDct
 
  def update(self,data):
    self.__dict__.update(data)
    