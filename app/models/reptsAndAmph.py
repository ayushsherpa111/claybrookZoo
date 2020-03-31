from app.models.animals import Animal

class ReptileAndAmphForm(Animal):
  def __init__(self, *args,**kwargs):
    super().__init__(args[0])
    self.location = "Hothouse"
    self.__dict__.update(args[1])

