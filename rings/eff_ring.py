from .finite_ring import FiniteRing


# Prends un ensemble et une fonction fun: X x X -> X, et renvoie
# la même fonction précalculée
def precompute(X, fun):
  f = dict()

  for x in X:
    f[x] = fun(x)

  return lambda x: f[x]

def precompute_pair(X, fun):
  f = dict()

  for x in X:
    f[x] = dict()

    for y in X:
      f[x][y] = fun(x, y)

  return lambda x, y: f[x][y]


def find_idx(lst, x):
  for i in range(len(lst)):
    if lst[i] == x:
      return i
    
  return None

class EffMeta(type):
  def __new__(cls, name, bases, attrs):
    new_class = super().__new__(cls, name, bases, attrs)

    def __init__(self, idx):
      self.idx = idx

    @staticmethod
    def encapsulate(x):
      return new_class(find_idx(new_class.data_el, x))
    
    def value(self):
      return new_class.data_el[self.idx]
    

    new_class.__init__ = __init__
    new_class.encapsulate = encapsulate
    new_class.value = value
    return new_class

  def __call__(cls, value):
    return super().__call__(value)



def create_eff_ring(rg, el):
  class_name = f"Eff_{rg.__name__}"
  attrs = {
    "ring_type": rg,
    "data_el": list(el),
    "data_add": precompute_pair(list(range(len(el))), lambda i, j: find_idx(el, el[i] + el[j])),
    "data_mul": precompute_pair(list(range(len(el))), lambda i, j: find_idx(el, el[i] * el[j])),
    "data_neg": precompute(list(range(len(el))), lambda i: find_idx(el, -el[i])),
    "data_zero": find_idx(el, rg.zero()),
    "data_unit": find_idx(el, rg.unit()),

    "zero": staticmethod(lambda: cls(cls.data_zero)),
    "unit": staticmethod(lambda: cls(cls.data_unit)),

    "elements": staticmethod(lambda: { cls(i) for i in range(len(el)) } ),

    "__add__": lambda self, other: cls(cls.data_add(self.idx, other.idx)) if isinstance(other, cls) else TypeError("On ne peut additionner que des instances de la même classe."),

    "__mul__": lambda self, other: cls(cls.data_mul(self.idx, other.idx)) if isinstance(other, cls) else TypeError("On ne peut multiplier que des instances de la même classe."),

    "__neg__": lambda self: cls(cls.data_neg(self.idx)),

    "__eq__": lambda self, other: self.idx == other.idx,

    "__hash__": lambda self: self.idx,

    "__repr__": lambda self: str(self.value())
  }
  cls = EffMeta(class_name, (FiniteRing,), attrs)
  return cls
