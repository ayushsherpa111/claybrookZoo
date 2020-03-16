from animals import Animal

class Mammals(Animal):
  def __init__(self, spcs, name, dob, gender, lifeSpan, clas, diet, habitat, popn, joinD, dimension,gestPeriod,cat,bodyTemp):
    super().__init__(spcs, name, dob, gender, lifeSpan, clas, diet, habitat, popn, joinD, dimension)
    self.gest = gestPeriod
    self.category = cat
    self.bodyTemp = bodyTemp

  def getDiet(self):
    return f"This fuckin animal eats {' and'.join(self.diet)}"
  