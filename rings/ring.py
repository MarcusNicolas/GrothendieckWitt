# Classe qui encode des anneaux finis
class Ring:
  @staticmethod
  def zero():
    raise NotImplementedError("'zero' non implémenté.")
  
  @staticmethod
  def unit():
    raise NotImplementedError("'unit' non implémentée.")
  
  def __add__(self, other):
    raise NotImplementedError("Addition non implémentée.")

  def __sub__(self, other):
    return self + (-other)

  def __mul__(self, other):
    raise NotImplementedError("Multiplication non implémentée.")

  def __neg__(self):
    raise NotImplementedError("Négation non implémentée.")
  
  def __eq__(self, other):
    raise NotImplementedError("Égalité non implémentée.")

  def __repr__(self):
    raise NotImplementedError("Représentation non implémentée.")



def ring_sum(ring_type, list):
  s = ring_type.zero()

  for x in list:
    s += x

  return s
