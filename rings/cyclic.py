from .ring import Ring


# Metaclass to create classes for Cyclic(n)
class CyclicMeta(type):
  def __new__(cls, name, bases, attrs):
    # Create the class
    new_class = super().__new__(cls, name, bases, attrs)
    # Add a __init__ method dynamically
    def __init__(self, value):
        self.value = value % new_class.modulus

    new_class.__init__ = __init__
    return new_class

  def __call__(cls, value):
    # Return an instance of the class
    return super().__call__(value)


# Function to create a Cyclic class for a given modulus n
def create_cyclic_class(n):
  class_name = f"Cyclic{n}"
  attrs = {
    "modulus": n,
    "__add__": lambda self, other: cls((self.value + other.value) % n) if isinstance(other, cls) else TypeError("Can only add instances of the same class."),
    "__sub__": lambda self, other: cls((self.value - other.value) % n) if isinstance(other, cls) else TypeError("Can only subtract instances of the same class."),
    "__mul__": lambda self, other: cls((self.value * other.value) % n) if isinstance(other, cls) else TypeError("Can only multiply instances of the same class."),
    "__neg__": lambda self: cls((-self.value) % n),
    "__eq__": lambda self, other: (self.value - other.value) % n == 0,
    "__hash__": lambda self: self.value % n,
    "val": lambda self: self.value % n,
    "__repr__": lambda self: f"{self.value}"
  }
  cls = CyclicMeta(class_name, (Ring,), attrs)
  return cls

