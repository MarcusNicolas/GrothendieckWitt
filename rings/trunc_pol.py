from .ring import ring_sum
from .finite_ring import FiniteRing


# Métaclasse pour créer TruncPol(n)
# TODO: précalculer produits et sommes....
class TruncPolMeta(type):
  def __new__(cls, name, bases, attrs):
    new_class = super().__new__(cls, name, bases, attrs)

    def __init__(self, coeffs):
      self.coeffs = [ coeffs[i] if i < len(coeffs) else new_class.ring_type.zero() for i in range(new_class.max_deg) ]
    
    @staticmethod
    def elements():
      n = new_class.max_deg

      rg_el = list(new_class.ring_type.elements())
      s = len(rg_el)

      p = [ s**(i+1) for i in range(n) ]

      el = [ new_class.zero() for _ in range(p[n-1]) ]

      for t in range(len(el)):
        for i in range(n):
          el[t][i] = rg_el[t % p[i] // (p[i-1] if i > 0 else 1)]

      return set(el)
          
    def __getitem__(self, idx):
      return self.coeffs[idx]
    
    def __setitem__(self, idx, val):
      if not isinstance(val, new_class.ring_type):
        raise TypeError("Valeur du mauvais type.")
      
      self.coeffs[idx] = val
    
    def __hash__(self):
      # Pas très propre mais ça fonctionne
      b = 6
      return sum([ self[i].__hash__() * (b**i) for i in range(new_class.max_deg) ])


    new_class.__init__ = __init__
    new_class.elements = elements
    new_class.__getitem__ = __getitem__
    new_class.__setitem__ = __setitem__
    new_class.__hash__ = __hash__

    return new_class

  def __call__(cls, value):
    return super().__call__(value)
  

def create_trunc_pol_class(n, rg):
  class_name = f"Pol({n}, {rg.__name__})"
  attrs = {
    "max_deg": n,
    "ring_type": rg,

    "zero": staticmethod(lambda: cls([ rg.zero() for _ in range(n) ])),

    "unit": staticmethod(lambda: cls([ rg.unit() if i == 0 else rg.zero() for i in range(n) ])),

    #"elements": staticmethod(lambda: { cls(i) for i in range(n) } ),

    "__add__": lambda self, other: cls([ self[i] + other[i] for i in range(n) ]) if isinstance(other, cls) else TypeError("On ne peut additionner que des instances de la même classe."),

    "__mul__": lambda self, other: cls([ ring_sum(rg, [ self[j]*other[i-j] if j < n and (i-j) < n else rg.zero() for j in range(i+1) ]) for i in range(n) ]) if isinstance(other, cls) else TypeError("On ne peut multiplier que des instances de la même classe."),

    "__neg__": lambda self: cls([ -self[i] for i in range(n)]),

    "__eq__": lambda self, other: not any([ self[i] != other[i] for i in range(n) ]),

    "__repr__": lambda self: "0" if self == cls.zero() else " + ".join([f"{'' if c == rg.unit() else c}X^{i}" if i > 0 else str(c) for i, c in enumerate(self.coeffs) if c != rg.zero()]).replace("X^1", "X")
  }
  cls = TruncPolMeta(class_name, (FiniteRing,), attrs)
  return cls
