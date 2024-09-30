import math
#import sympy as sp
import sympy
import sympy.matrices.normalforms
import rings

# Given a set with an equivalence relation, return the equivalence classes
def equiv_classes(dom, equiv):
  classes = []
  ord_dom = []

  for x in dom:
    ord_dom.append((x, True))

  for i in range(len(ord_dom)):
    x, mark_x = ord_dom[i]
    
    if mark_x:
      ord_dom[i] = (x, False)
      classe = {x}

      for j in range(len(ord_dom)):
        y, mark_y = ord_dom[j]

        if mark_y and equiv(x, y):
          ord_dom[j] = (y, False)
          classe.add(y)
        
      classes.append(classe)
    
  return classes


# Étant donné un entier n, calcule les unités, puis les classes d'équivalence
# modulo carré, et renvoie les classes d'équivalence, et une fonction qui à un
# élément associe sa classe
def cyclic_units_mod_sq(cyclic_type):
  n = cyclic_type.modulus

  units = { cyclic_type(x) for x in range(1, n) if math.gcd(x, n) == 1 }
  units_sq = { x*x for x in units }

  classes = equiv_classes(units, lambda x, y : any(a*x == y for a in units_sq))
  tab = [ -1 for i in range(n) ]

  for k in range(len(classes)):
    for x in classes[k]:
      tab[x.val()] = k

  return classes, lambda x: tab[x.val()]

# Prend un anneau Z/nZ et renvoie la matrice des relations
def cyclic_MW_matrix(cyclic_type):
  classes, p = cyclic_units_mod_sq(cyclic_type)
  mat = []
  unit = cyclic_type(1)

  # relations <a> + <-a> = <1> + <-1>
  for x in classes:
    line = [ 0 for _ in classes ]
    a = next(iter(x))

    line[p(a)] += 1
    line[p(-a)] += 1
    line[p(unit)] -= 1
    line[p(-unit)] -= 1

    mat.append(line)

  # relations <a> + <b> = <a+b> + <(a+b)ab>
  for i in range(len(classes)):
    for j in range(i, len(classes)):
      line = [ 0 for _ in classes ]
      a = next(iter(classes[i]))
      b = next(iter(classes[j]))

      # si a+b est inversible
      if p(a+b) != -1:
        line[p(a)] += 1
        line[p(b)] += 1
        line[p(a+b)] -= 1
        line[p(a*b*(a+b))] -= 1

        mat.append(line)

  # On construit une famille libre de relations
  mat = sympy.Matrix(sympy.Matrix(mat).rowspace())

  return mat.transpose() # Les relations doivent être des colonnes

# Prend une matrice mat et renvoie une fonction qui teste l'existence
# de solutions entière à l'équation Mx = v
def solution_exists(M):
  D, P, _ = sympy.matrices.normalforms.smith_normal_decomp(M, domain=sympy.ZZ)
  n, m = M.shape # P est carrée de taille n x n

  print(n, m)

  def test(v):
    w = P * sympy.Matrix(v)

    for i in range(n):
      if i < m:
        if D[i, i] == 0 and w[i, 0] != 0:
          return False
        if w[i, 0] % D[i, i] != 0:
          return False
      if i >= m and w[i, 0] != 0:
        return False

    return True

  return test

# Étant donné un type cyclique, renvoie la fonction qui teste l'équivalence de
# deux vecteurs
def cyclic_MW_equiv(cyclic_type):
  
  return []



# Create Cyclic classes for specific moduli
Cyclic2 = rings.create_cyclic_class(2)
Cyclic3 = rings.create_cyclic_class(3)
Cyclic8 = rings.create_cyclic_class(33)
Cyclic5 = rings.create_cyclic_class(5)
# Add more as needed...

print(sympy.__version__)

#Test
classes, f = cyclic_units_mod_sq(Cyclic8)
print(f"Classes: { classes }")

M = sympy.Matrix(cyclic_MW_matrix(Cyclic8))



N = sympy.Matrix([[1, 2], [0, 3]])
f = solution_exists(N)

print(f([87247, -66]))

# Deux problèmes:
# 1) On veut regarder quels sont les relations (a_i) = (b_i) impliquées par
#    celles de la présentation MW (comment faire ?)
# 2) On veut regarder lesquelles de ces classes sont identifiées dans GW