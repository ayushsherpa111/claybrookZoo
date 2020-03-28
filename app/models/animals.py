class Animal:
  
  def __init__(self,*args,**kwargs):
    animalArgs = args[0]
    animalArgs.update(kwargs)
    self.__dict__.update(animalArgs)

  def get(self):
    print(self)
    return vars(self)

  @classmethod
  def fromDict(cls,inst,animDict):
    if "_id" in animDict:
      _id = animDict['_id']
      del animDict["_id"]
    anim = inst(*animDict.values())
    anim._id = _id
    return anim


