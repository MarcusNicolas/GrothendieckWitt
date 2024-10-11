from .ring import Ring, ring_sum



# Métaclasse pour créer Mat(n, R)
class MatMeta(type):
  def __new__(cls, name, bases, attrs):
    # Create the class
    new_class = super().__new__(cls, name, bases, attrs)
    # Add a __init__ method dynamically
    def __init__(self, mat):
      self.mat = [ [ new_class.ring_type(0) for _ in range(new_class.size) ] for _ in range(new_class.size) ]

      if len(mat) != new_class.size:
        raise ValueError("Pas le bon nombre de lignes.")

      for i in range(new_class.size):
        if len(mat[i]) != new_class.size:
          raise ValueError("Pas le bon nombre de colonnes.")

        for j in range(new_class.size):
          if not isinstance(mat[i][j], new_class.ring_type):
            raise TypeError("Valeurs du mauvais type.")

          self[i,j] = mat[i][j]

    @staticmethod
    def diag(coeffs):
      if len(coeffs) != new_class.size:
        raise ValueError("Pas le bon nombre de coefficients.")
      
      mat = new_class.zero()

      for i in range(new_class.size):
        if not isinstance(coeffs[i], new_class.ring_type):
          raise TypeError("Valeurs du mauvais type.")

        mat[i,i] = coeffs[i]

      return mat
    
    def transpose(self):
      n = new_class.size
      return new_class([ [ self[j,i] for j in range(n) ] for i in range(n)])
          
    def __getitem__(self, idx):
      i, j = idx
      return self.mat[i][j]
    
    def __setitem__(self, idx, val):
      if not isinstance(val, new_class.ring_type):
        raise TypeError("Valeur du mauvais type.")
      
      i, j = idx
      self.mat[i][j] = val

    new_class.__init__ = __init__
    new_class.diag = diag
    new_class.transpose = transpose
    new_class.__getitem__ = __getitem__
    new_class.__setitem__ = __setitem__
    return new_class

  def __call__(cls, mat):
    # Return an instance of the class
    return super().__call__(mat)





def create_mat_class(n, rg):
  class_name = f"Mat{n}({rg.__name__})"
  attrs = {
    "size": n,
    "ring_type": rg,

    "zero": staticmethod(lambda: cls([ [ rg.zero() for _ in range(n) ] for _ in range(n)])),

    "unit": staticmethod(lambda: cls([ [ rg.unit() if i == j else rg.zero() for j in range(n) ] for i in range(n)])),

    "__add__": lambda self, other: cls([ [ self[i,j] + other[i,j] for j in range(n) ] for i in range(n) ]) if isinstance(other, cls) else TypeError("On ne peut additionner que des instances de la même classe."),

    "__mul__": lambda self, other: cls([ [ ring_sum(rg, [ self[i,k] * other[k,j] for k in range(n) ]) for j in range(n) ] for i in range(n) ]) if isinstance(other, cls) else TypeError("On ne peut multiplier que des instances de la même classe."),

    "__neg__": lambda self: cls([ [ -self[i,j] for j in range(n) ] for i in range(n)]),

    "__eq__": lambda self, other: not any([ any([ self[i,j] != other[i,j] for j in range(n) ]) for i in range(n) ]),

    "__repr__": lambda self: "\n".join(["[" + ", ".join(map(str, row)) + "]" for row in self.mat])
  }
  cls = MatMeta(class_name, (Ring,), attrs)
  return cls
