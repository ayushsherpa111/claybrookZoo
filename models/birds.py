from animals import Animal
class Birds(Animal):
  def __init__(self, spcs, name, dob, gender, lifeSpan, clas, diet, habitat, popn, joinD, dimension,nest,clutch,wingspan,fly,color):
    super().__init__(spcs, name, dob, gender, lifeSpan, clas, diet, habitat, popn, joinD, dimension)
    self.nest = nest
    self.clutch = clutch
    self.wingspan = wingspan
    self.fly = fly
    self.color = color
  
  def updateNest(self,nest):
    self.nest = nest
    return self.nest
  
