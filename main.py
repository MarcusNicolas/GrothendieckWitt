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


  units = { cyclic_type(x) for x in range(n) if math.gcd(x, n) == 1 }
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
def cyclic_MW_diags(cyclic_type, G, pr_G):
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


# Énumère les matrices diagonales 4x4 possibles à permutation près
# et à choix près modulo un carré
def cyclic_list_diags(cyclic_type, classes, pr, choice):
  n = cyclic_type.modulus
  # on veut que choice associe à toute classe un choix de représentant

  diags = [ ]

  for i in range(len(classes)):
    for j in range(len(classes)):
      for k in  range(len(classes)):
        for l in range(len(classes)):
          diag = rings.Mat(4, 4, cyclic_type)

          diag[0][0] = choice[i]
          diag[1][1] = choice[j]
          diag[2][2] = choice[k]
          diag[3][3] = choice[l]

          diags.append(diag)

  # Prend une matrice diagonale et renvoie un élément de Z[G]
  def diag_to_vec(diag):
    v = [ 0 for _ in classes ]

    v[pr(diag[0][0])] += 1
    v[pr(diag[1][1])] += 1
    v[pr(diag[2][2])] += 1
    v[pr(diag[3][3])] += 1

    return v
  

  # On identifie les matrices qui sont obtenues l'une de l'autre par permutation
  diags, pr_diag = equiv_classes(diags, (lambda d, e: diag_to_vec(d) == diag_to_vec(e)))

  return diags, pr_diag



# Prend un dévissage d'un anneau R, et renvoie une fonction qui associe à deux
# matrices 4x4 diagonales D, D' à valeurs dans R la liste des P solutions de
# l'équation P D tP = D'.
# -----
# rings_types: une liste d'anneaux R0, R1, ..., Rn = R
# f: une liste de morphismes R1 -> R0, R2 -> R1, etc
# units_mod_sq: fonction qui renvoie pour un anneau Ri les classes d'équivalence
#   d'unités modulo carrés dans Ri, avec la projection
# fib: tableau dont la ième entrée fib[i] contient une fonction qui associe
#   à un élément de Ri l'ensemble des éléments de R(i+1) vivant au-dessus
# el_base: ensemble des éléments de l'anneau R0
# list_diags: liste de fonctions permettant de lister les diagonales
def GW_base_change(ring_types, mor, fib, el_base, units_mod_sq):#, list_diags):
  n = len(ring_types)
  zero_ring = rings.create_cyclic_class(1)

  R = [ zero_ring ] + ring_types
  mor = [ lambda _: zero_ring(0) ] + mor
  fib = [ lambda _: el_base ] + fib

  units_mod_sq = [ cyclic_units_mod_sq(zero_ring) ] + units_mod_sq
  cl_zero, pr_zero = units_mod_sq[0]

  # On commence avec le seul choix d'unité que l'on peut faire
  choice = [ [ zero_ring(1) ] ]

  diags = [ cyclic_list_diags(zero_ring, cl_zero, pr_zero, choice[0]) ]

  for k in range(1,n+1):
    # construire la fonction de choix
    cl, pr = units_mod_sq[k]
    _, pr_low = units_mod_sq[k-1]

    choice.append([])

    for i in range(len(cl)):
      # Représentant canonique de la classe un niveau en-dessous
      c_low = choice[k-1][pr_low(mor[k-1](cl[i][0]))]

      for j in range(len(cl[i])):
        if mor[k-1](cl[i][j]) == c_low:
          choice[k].append(cl[i][j])
          break


  return choice

  sol = []



  return sol[n] # TODO: bon indice ?


N = 5 # On veut Z/2^NZ

p = [ 2**(k+1) for k in range(N) ]
R = [ rings.create_cyclic_class(p[k]) for k in range(N) ]


mor = [ (lambda i: ( lambda x: R[i](x.value) ))(k) for k in range(N-1) ]
fib = [ (lambda i: lambda x: { R[i+1](x.value), R[i+1](x.value + p[i]) })(k) for k in range(N-1) ]
el_base = { R[0](0), R[0](1) }
units = [ cyclic_units_mod_sq(R[k]) for k in range(N) ]

test = GW_base_change(R, mor, fib, el_base, units)

print(test)





# Notre anneau R est ici un Z/nZ
#R = rings.create_cyclic_class(1)
#G, pr_G = cyclic_units_mod_sq(R)

#print(G)

#vecs, pr_vec = cyclic_list_diags(R, G, pr_G)



# Deux problèmes:
# 1) On veut regarder quels sont les relations (a_i) = (b_i) impliquées par
#    celles de la présentation MW (comment faire ?)
# 2) On veut regarder lesquelles de ces classes sont identifiées dans GW