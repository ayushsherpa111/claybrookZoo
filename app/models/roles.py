from app.models.user import User
class Admin(User):
  def __init__(self, *args):
    super().__init__(args[0])
    args[1].update({'role':"Admin"})
    self.__dict__.update(args[1])
  
class Visitor(User):
  def __init__(self, *args):
    super().__init__(args[0])
    args[1].update({'role':"Visitor"})
    self.__dict__.update(args[1])

class Staff(User):
  def __init__(self, *args):
    super().__init__(args[0])
    args[1].update({'role':"Staff"})
    self.__dict__.update(args[1])

class Manager(User):
  def __init__(self, *args):
    super().__init__(args[0])
    args[1].update({'role':"Manager"})
    self.__dict__.update(args[1])


class Sponsor(User):
  def __init__(self, *args):
    super().__init__(args)
    args[1].update({'role':"Sponsor"})
    self.__dict__.update(args[1])
  
  def setBand(self,band):
    self.__dict__({'band':band})
  
  def getBand(self):
    return self.band