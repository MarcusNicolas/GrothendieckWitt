import sympy
import sympy.polys.matrices
import sympy.matrices.normalforms

import equiv
from rings import finite_ring



# Prend une matrice mat (à coeffs dans Z) et renvoie une fonction qui teste
# l'existence de solutions à l'équation Mx = v
def solution_exists(M):
  D, P, _ = sympy.matrices.normalforms.smith_normal_decomp(M, domain=sympy.ZZ)
  n, m = M.shape # P est carrée de taille n x n

  def test(v):
    w = P * sympy.Matrix(v)

    for i in range(n):
      if i < m:
        if D[i, i] == 0 and w[i, 0] != 0:
          return False
        if D[i, i] != 0 and w[i, 0] % D[i, i] != 0:
          return False
      if i >= m and w[i, 0] != 0:
        return False

    return True

  return test


def remove_doubles(vec):
  sol = dict()

  for v in vec:
    sol[tuple(v)] = v

  return list(sol.values())


# Prend un anneau fini et renvoie la matrice des relations pour MW
def MW_matrix(finite_ring_type, G, pr_G):
  one = finite_ring_type.unit()
  u = list(finite_ring.units(finite_ring_type))

  mat = []

  # relations <a> + <-a> = <1> + <-1>
  for x in G:
    rel = [ 0 for _ in G ]
    a = next(iter(x))

    rel[pr_G(a)] += 1
    rel[pr_G(-a)] += 1
    rel[pr_G(one)] -= 1
    rel[pr_G(-one)] -= 1

    mat.append(rel)

  # relations <a> + <b> = <a+b> + <(a+b)ab>
  for i in range(len(u)):
    a = u[i]

    for j in range(i, len(u)):
      b = u[j]
      c = u[i] + u[j]

      if pr_G(c) == None:
        break

      rel = [ 0 for _ in G ]
      rel[pr_G(a)] += 1
      rel[pr_G(b)] += 1
      rel[pr_G(c)] -= 1
      rel[pr_G(a*b*c)] -= 1

      mat.append(rel)
        

  mat = sympy.Matrix(remove_doubles(mat))

  return mat.transpose() # Les relations doivent être des colonnes


# Étant donné un anneau fini R, renvoie une fonction permettant de tester
# l'équivalence de deux vecteurs de Z[G(R)] modulo les relations de MW
def MW_equiv(finite_ring_type, G, pr_G):
  mat = MW_matrix(finite_ring_type, G, pr_G)
  is_zero = solution_exists(mat)

  return (lambda u, v: is_zero([u[i] - v[i] for i in range(len(u))]))


# Étant donné un anneau fini R, calculer les classes d'équivalence de vecteurs
# de la forme <a> + <b> + <c> + <d> où a, b, c, d sont des unités, modulo MW.
def cyclic_MW_diags(finite_ring_type, G, pr_G):
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


  vecs, pr_vec = equiv.classes(vecs, MW_equiv(finite_ring_type, G, pr_G))

  return vecs, pr_vec

