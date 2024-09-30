from .ring import Ring

class Mat(Ring):
  def __init__(self, rows, cols, ring_type):
    if not isinstance(ring_type, type) or not issubclass(ring_type, Ring):
      raise TypeError("ring_type must be a subclass of Ring.")
    self.rows = rows
    self.cols = cols
    self.ring_type = ring_type
    self.data = [[ring_type(0) for _ in range(cols)] for _ in range(rows)]

  def __getitem__(self, idx):
      return self.data[idx]

  def __setitem__(self, idx, value):
    if len(value) != self.cols:
      raise ValueError("Row must have the same number of columns.")
    self.data[idx] = value

  def __add__(self, other):
    if self.rows != other.rows or self.cols != other.cols:
      raise ValueError("Matrices must have the same dimensions for addition.")
    result = Mat(self.rows, self.cols, self.ring_type)
    for i in range(self.rows):
      for j in range(self.cols):
        result[i][j] = self[i][j] + other[i][j]
    return result

  def __sub__(self, other):
    if self.rows != other.rows or self.cols != other.cols:
      raise ValueError("Matrices must have the same dimensions for substraction.")
    result = Mat(self.rows, self.cols, self.ring_type)
    for i in range(self.rows):
      for j in range(self.cols):
        result[i][j] = self[i][j] - other[i][j]
    return result

  def __mul__(self, other):
    if self.cols != other.rows:
      raise ValueError("Incompatible matrix dimensions for multiplication.")
    result = Mat(self.rows, other.cols, self.ring_type)
    for i in range(self.rows):
      for j in range(other.cols):
        for k in range(self.cols):
          result[i][j] += self[i][k] * other[k][j]
    return result

  def __repr__(self):
    return "\n".join(["[" + ", ".join(map(str, row)) + "]" for row in self.data])