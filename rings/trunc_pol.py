from .finite_ring import FiniteRing, ring_sum


# Métaclasse pour créer TruncPol(n)
class TruncPolMeta(type):
  def __new__(cls, name, bases, attrs):
    # Create the class
    new_class = super().__new__(cls, name, bases, attrs)
    # Add a __init__ method dynamically
    def __init__(self, coeffs):
      self.coeffs = [ coeffs[i] if i < len(coeffs) else new_class.ring_type.zero() for i in range(new_class.max_deg) ]
          
    def __getitem__(self, idx):
      return self.coeffs[idx]
    
    def __setitem__(self, idx, val):
      if not isinstance(val, new_class.ring_type):
        raise TypeError("Valeur du mauvais type.")
      
      self.coeffs[idx] = val
    
    @staticmethod
    def elements():


    new_class.__init__ = __init__
    new_class.__getitem__ = __getitem__
    new_class.__setitem__ = __setitem__
    new_class.elements = elements

    return new_class

  def __call__(cls, value):
    # Return an instance of the class
    return super().__call__(value)
  

# TODO: lister éléments
def create_trunc_pol_class(n, rg):
  class_name = f"{rg.__name__}[X]/(X^{n})"
  attrs = {
    "max_deg": n,
    "ring_type": rg,

    "zero": staticmethod(lambda: cls([ rg.zero() for _ in range(n) ])),

    "unit": staticmethod(lambda: cls([ rg.unit() if i == 0 else rg.zero() for i in range(n) ])),

    #"elements": staticmethod(lambda: { cls(i) for i in range(n) } ),

    "__add__": lambda self, other: cls([ self[i] + other[i] for i in range(n) ]) if isinstance(other, cls) else TypeError("On ne peut additionner que des instances de la même classe."),

    "__mul__": lambda self, other: cls([ ring_sum([ self[j]*other[i-j] for j in range(i+1) ]) for i in range(n) ]) if isinstance(other, cls) else TypeError("On ne peut multiplier que des instances de la même classe."),

    "__neg__": lambda self: cls([ -self[i] for i in range(n)]),

    "__eq__": lambda self, other: not any([ self[i] != other[i] for i in range(n) ]),

    "__repr__": lambda self: "TODO"
  }
  cls = TruncPolMeta(class_name, (FiniteRing,), attrs)
  return cls
