
import equiv
import rings

# Prend une matrice diagonale 4x4 et renvoie un élément de Z[G]
def diag_to_vec(D, G, pr_G):
  v = [ 0 for _ in G ]

  v[pr_G(D[0,0])] += 1
  v[pr_G(D[1,1])] += 1
  v[pr_G(D[2,2])] += 1
  v[pr_G(D[3,3])] += 1

  return v

# Énumère les matrices diagonales 4x4 possibles à permutation près
# et à choix près modulo un carré
# - choice associe à toute classe un choix de représentant
def list_diags(finite_ring_type, G, pr_G, choice):
  diags = [ ]
  mat_type = rings.create_mat_class(4, finite_ring_type)

  for i in range(len(G)):
    for j in range(len(G)):
      for k in  range(len(G)):
        for l in range(len(G)):
          diags.append(mat_type.diag([ choice[i], choice[j], choice[k], choice[l] ]))
  

  # On identifie les matrices qui sont obtenues l'une de l'autre par permutation
  diags, _ = equiv.classes(diags, (lambda d, e: diag_to_vec(d, G, pr_G) == diag_to_vec(e, G, pr_G)))

  return mat_type, diags



def bil_form_eval(mat, u, v):
  R = mat.ring_type
  
  e = R.zero()

  for i in range(mat.size):
    for j in range(mat.size):
      e += u[i] * mat[i,j] * v[j]

  return e


# Prend un dévissage d'un anneau R, et renvoie une fonction qui associe à deux
# matrices 4x4 diagonales D, D' à valeurs dans R la liste des P solutions de
# l'équation P D tP = D'.
# -----
# finite_ring_types: une liste d'anneaux finis R0, R1, ..., Rn = R
# mor: une liste de morphismes R1 -> R0, R2 -> R1, etc
def GW_base_change(finite_ring_types, mor):
  N = len(finite_ring_types)
  zero_ring = rings.create_cyclic_class(1)

  R = [ zero_ring ] + finite_ring_types
  mor = [ lambda _: zero_ring(0) ] + mor
  ums = [ rings.units_mod_sq(R[k]) for k in range(N+1) ]

  G_zero, pr_zero = ums[0]

  # On commence avec le seul choix d'unité que l'on peut faire
  choice = [ [ zero_ring.unit() ] ]

  mat_zero_type, dg_zero  = list_diags(zero_ring, G_zero, pr_zero, choice[0])
  
  mat_types = [ mat_zero_type ]
  diags = [ dg_zero[0] ]

  # Contient en rang k un tableau qui associe à chaque matrice de diags[k+1]
  # l'indice de son projeté de diags[k]
  pr_diags = [ ]

  # Prend une matrice 4x4 de R[k+1] et la projette sur R[k]
  def proj_mat(k, mat):
    proj = mat_types[k].zero()

    for i in range(4):
      for j in range(4):
        proj[i,j] = mor[k](mat[i,j])
      
    return proj
  

  def pair_first(p):
    x, _ = p
    return x
  
  def pair_second(p):
    _, y = p
    return y
  
  G = [ pair_first(ums[k]) for k in range(N+1) ]
  pr_G = [ pair_second(ums[k]) for k in range(N+1) ]


  for k in range(1,N+1):
    # Construire la fonction de choix
    choice.append([ ])

    for i in range(len(G[k])):
      # Représentant canonique de la classe un niveau en-dessous
      c_low = choice[k-1][pr_G[k-1](mor[k-1](G[k][i][0]))]

      # On choisit le premier représentant qui relève c_low
      for j in range(len(G[k][i])):
        if mor[k-1](G[k][i][j]) == c_low:
          choice[k].append(G[k][i][j])
          break
    
    # Relever les diagonales avec notre fonction de choix
    mat_type, dg_cl = list_diags(R[k], G[k], pr_G[k], choice[k])

    mat_types.append(mat_type)
    diags.append([ ])
    pr_diags.append([ ])

    # Ne retenir qu'une diagonale par classe
    for d_cl in dg_cl:
      d_vec = diag_to_vec(proj_mat(k-1, d_cl[0]), G[k-1], pr_G[k-1])

      for r in range(len(diags[k-1])):
        # Teste si l'on est au-dessus de la bonne classe
        d_low_vec = diag_to_vec(diags[k-1][r], G[k-1], pr_G[k-1])
        
        if any(d_vec[i] != d_low_vec[i] for i in range(len(G[k-1]))):
          continue

        # Si c'est le cas, on cherche le premier relevé
        for d in d_cl:
          if proj_mat(k-1, d) == diags[k-1][r]:
            diags[k].append(d)
            pr_diags[k-1].append(r)
            break

        # ... et pas besoin de continuer
        break


  # Ayant calculé les diagonales, on calcule les vecteurs unitaires pour chacune
  # de ces normes
  uvec = [ [ [ zero_ring.unit() for _ in range(4)] ] ]
  pr_uvec = [  ]

  for k in range(1, N+1):
    # On relève chacun des uvec, en gardant en mémoire pr_vec
    continue


  # pour r <= s, sol[k][r][s] contient les matrices de passage de
  #   diag[k][r] vers diag[k][s]
  
  sols = [ [ [ mat_zero_type.unit() ] ] ]

  for k in range(1, N+1):
    # On a les solutions au niveau k-1

    # Pour toute diagonale, on calcule
    break


  return 0
