from typing import Optional

import math
import sympy
import sympy.matrices.normalforms
import rings

# On prends un ensemble muni d'une rel d'équivalence, et on renvoie les classes
# d'équivalence sous forme de liste
def equiv_classes(dom, equiv):
  classes = []
  mark = [ True for _ in dom ]
  ref = [ None for _ in dom ]


  for i in range(len(dom)):
    if mark[i]:
      classe = [ ]
      m = len(classes)

      for j in range(len(dom)):
        if mark[j] and equiv(dom[i], dom[j]):
          mark[j] = False
          ref[j] = m
          classe.append(dom[j])
        
      classes.append(classe)
    
  return classes, lambda i: classes[ref[i]]


# Étant donné un entier n, calcule les unités, puis les classes d'équivalence
# modulo carré, et renvoie les classes d'équivalence, et une fonction qui à un
# élément associe sa classe
def cyclic_units_mod_sq(cyclic_type):
  n = cyclic_type.modulus

  units = { cyclic_type(x) for x in range(1, n) if math.gcd(x, n) == 1 }
  units_sq = { x*x for x in units }

  G, _ = equiv_classes(list(units), lambda x, y : any(a*x == y for a in units_sq))
  tab = [ None for i in range(n) ]

  for k in range(len(G)):
    for x in G[k]:
      tab[x.val()] = k

  return G, lambda x: tab[x.val()]

# Prend un anneau Z/nZ et renvoie la matrice des relations
def cyclic_MW_matrix(cyclic_type, G, pr_G):
  mat = []
  unit = cyclic_type(1)
  n = cyclic_type.modulus

  # relations <a> + <-a> = <1> + <-1>
  for x in G:
    line = [ 0 for _ in G ]
    a = next(iter(x))

    line[pr_G(a)] += 1
    line[pr_G(-a)] += 1
    line[pr_G(unit)] -= 1
    line[pr_G(-unit)] -= 1

    mat.append(line)

  # relations <a> + <b> = <a+b> + <(a+b)ab>
  for i in range(n):
    a = cyclic_type(i)

    if pr_G(a) == None:
      break

    for j in range(a, n):
      b = cyclic_type(j)

      if pr_G(b) != None and pr_G(a+b) != None:
        line = [ 0 for _ in G ]

        line[pr_G(a)] += 1
        line[pr_G(b)] += 1
        line[pr_G(a+b)] -= 1
        line[pr_G(a*b*(a+b))] -= 1

        mat.append(line)

  # On construit une famille libre de relations
  mat = sympy.Matrix(sympy.Matrix(mat).rowspace())

  return mat.transpose() # Les relations doivent être des colonnes

# Prend une matrice mat et renvoie une fonction qui teste l'existence
# de solutions entière à l'équation Mx = v
def solution_exists(M):
  D, P, _ = sympy.matrices.normalforms.smith_normal_decomp(M, domain=sympy.ZZ)
  n, m = M.shape # P est carrée de taille n x n

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

# Étant donné un anneau Z/nZ, renvoie une fonction permettant de tester
# l'équivalence de deux vecteurs de Z[G(R)] modulo les relations de MW
def cyclic_MW_equiv(cyclic_type, G, pr_G):
  mat = cyclic_MW_matrix(cyclic_type, G, pr_G)
  is_zero = solution_exists(mat)

  return (lambda u, v: is_zero([u[i] - v[i] for i in range(len(u))]))


# Étant donné un anneau Z/nZ, calculer les classes d'équivalence de vecteurs de
# la forme <a> + <b> + <c> + <d> où a, b, c, d sont des unités, modulo MW
# Ensuite on peut tester l'équivalence avec la présentation de Knebuch par force
# brute (modulo réduction avec symétries)
def cyclic_MW_four_diag(cyclic_type, G, pr_G):
  n = cyclic_type.modulus

  vecs = [ ]

  for i in range(len(G)):
    for j in range(i, len(G)):
      for k in range(j, len(G)):
        for l in range(k, len(G)):
          v = [ 0 for _ in G ]

          v[i] += 1
          v[j] += 1
          v[k] += 1
          v[l] += 1

          vecs.append(v)

  vecs, pr_vec = equiv_classes(vecs, cyclic_MW_equiv(cyclic_type, G, pr_G))

  return vecs, pr_vec


def cyclic_GW_four_diag(cyclic_type, classes, pr):
  n = cyclic_type.modulus
  choice = [ next(iter(classes[i])) for i in range(len(classes)) ]

  diags = [ ]

  for i in range(len(classes)):
    for j in range(len(classes)):
      for k in  range(len(classes)):
        for l in range(len(classes)):
          diag = rings.Mat(4, 4)

          diag[0,0] = cyclic_type(choice(i))
          diag[1,1] = cyclic_type(choice(j))
          diag[2,2] = cyclic_type(choice(k))
          diag[3,3] = cyclic_type(choice(l))

          diags.append(diag)


  # Prend une matrice diagonale et renvoie un élément de Z[G]
  def pr_diag(diag):
    v = [ 0 for _ in classes ]

    v[pr(diag(0,0))] += 1
    v[pr(diag(1,1))] += 1
    v[pr(diag(2,2))] += 1
    v[pr(diag(3,3))] += 1

    return v

  return 0



# Notre anneau R est ici un Z/nZ
R = rings.create_cyclic_class(256)

G, pr_G = cyclic_units_mod_sq(R)

vecs, pr_vec = cyclic_MW_four_diag(R, G, pr_G)
print(len(vecs))


# Deux problèmes:
# 1) On veut regarder quels sont les relations (a_i) = (b_i) impliquées par
#    celles de la présentation MW (comment faire ?)
# 2) On veut regarder lesquelles de ces classes sont identifiées dans GW