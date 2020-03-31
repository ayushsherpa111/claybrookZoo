from app.models.animals import Animal

class Mammals(Animal):
  def __init__(self, *args,**kwargs):
    super().__init__(args[0])
    self.location = "Compound"
    self.__dict__.update(args[1])

  def getDiet(self):
    return f"This animal eats {' and'.join(self.diet)}"


  def __repr__(self):
    return super().__repr__(
      [str(key)+str(val) for key,val in [*zip([*self.__dict__.keys()],[*self.__dict__.values()])] ]
    )