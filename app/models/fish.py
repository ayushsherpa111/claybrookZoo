from app.models.animals import Animal

class Fish(Animal):
  def __init__(self, *args,**kwargs):
    super().__init__(args[0])
    self.location = "Aquarium"
    self.__dict__.update(args[1])

