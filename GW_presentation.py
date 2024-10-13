import sympy

import equiv
import rings

from MW_presentation import remove_doubles

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


# Étant donné une fonction ensembliste fun: dom --> cod, on renvoie
# une fonction qui associe à un élément de cod l'ensemble des éléments
# de dom au-dessus
def fibs_fun(dom, cod, fun):
  fibs = dict()
  
  for y in cod:
    fibs[y] = []

  for x in dom:
    fibs[fun(x)].append(x)

  for y in cod:
    fibs[y] = set(fibs[y])

  return lambda y: fibs[y]



# Prend un dévissage d'un anneau R, et renvoie une fonction qui associe à deux
# matrices 4x4 diagonales D, D' à valeurs dans R la liste des P solutions de
# l'équation P D tP = D'.
# -----
# finite_ring_types: une liste d'anneaux finis R0, R1, ..., Rn = R
# mor: une liste de morphismes R1 -> R0, R2 -> R1, etc
def GW_matrices(finite_ring_types, mor):
  N = len(finite_ring_types)
  zero_ring = rings.create_cyclic_class(1)

  R = [ zero_ring ] + finite_ring_types
  mor = [ lambda _: zero_ring(0) ] + mor
  el = [ R[k].elements() for k in range(N+1) ]
  fibs_el = [ fibs_fun(el[k+1], el[k], mor[k]) for k in range(N) ]

  ums = [ rings.units_mod_sq(R[k]) for k in range(N+1) ]

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


  # On commence avec le seul choix d'unité que l'on peut faire
  choice = [ [ zero_ring.unit() ] ]
  mat_zero_type, dg_zero  = list_diags(zero_ring, G[0], pr_G[0], choice[0])
  
  mat_types = [ mat_zero_type ]
  diags = [ dg_zero[0] ]

  # Contient en rang k un tableau qui associe à chaque matrice de diags[k+1]
  # l'indice de son projeté de diags[k]
  pr_diags = [ ]

  # On construit des choix cohérents de matrices diagonales:
  # - diags[k] contient la liste des matrices diagonales choisies dans R[k]
  # - pr_diags[k-1][r] est l'indice tel que l'on ait l'identité
  #   mor[k-1]( diags[k][r] ) == diags[k-1][ pr_diags[k-1][r] ]
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
  # - uvec[k][i][r] donne la liste des vecteurs de norme choice[k][i]
  #   pour la forme donnée par la matrice diag[k][r]
  # - fibs_uvec[k-1][i][r][s] liste les indices de uvec[k][i][r] dans lesquels
  #   vivent les vecteurs au-dessus de uvec[k-1][proj_i][proj_r][s]
  uvec = [ [ [ [ [ zero_ring.unit() for _ in range(4) ] ] ] ] ]
  fibs_uvec = [ ]

  for k in range(1, N+1):
    uvec.append([ ])
    fibs_uvec.append([ ])

    for i in range(len(G[k])):
      proj_i = pr_G[k-1](mor[k-1](choice[k][i]))

      uvec[k].append([ ])
      fibs_uvec[k-1].append([ ])

      for r in range(len(diags[k])):
        proj_r = pr_diags[k-1][r]
        uvec_low = uvec[k-1][proj_i][proj_r]

        uvec[k][i].append([ ])
        fibs_uvec[k-1][i].append([ [ ] for _ in range(len(uvec_low)) ])

        t = 0

        # pour chaque vecteur "unitaire" selon la matrice projetée...
        for s in range(len(uvec_low)):
          u_low = uvec_low[s]

          for x1 in fibs_el[k-1](u_low[0]):
            for x2 in fibs_el[k-1](u_low[1]):
              for x3 in fibs_el[k-1](u_low[2]):
                for x4 in fibs_el[k-1](u_low[3]):
                  u = [ x1, x2, x3, x4 ]

                  # on le rajoute s'il est un relevé "unitaire"
                  if bil_form_eval(diags[k][r], u, u) == choice[k][i]:
                    uvec[k][i][r].append(u)
                    fibs_uvec[k-1][i][r][s].append(t)
                    t += 1


  # pour r et s < len(diags[k]), la liste sol[k][r][s] contient les matrices
  # de passage de diags[k][s] = (d_i) vers diags[k][r] = (e_i) 
  # Rq: on représente une telle matrice de passage P par la donnée
  # de 4 entiers (p_i), et alors P est la matrice dont la ligne i est
  # uvec[k][<e_i>][s][p_i]
  sols = [ [ [ [ [0, 0, 0, 0] ] ] ] ]


  for k in range(1, N+1):
    sols.append([ ])
    
    tot_mat = 0
    compt = 1

    # Si k == N, on n'a peut s'arrêter dès qu'on sait qu'il existe une solution
    last_ring = (k == N)

    for r in range(len(diags[k])):
      proj_r = pr_diags[k-1][r]

      for s in range(len(diags[k])):
        proj_s = pr_diags[k-1][s]
        tot_mat += len(sols[k-1][proj_r][proj_s])
        

    # TODO: implémenter inverse matriciel pour diviser par deux le temps
    # TODO: implémenter avec plusieurs coeurs
    for r in range(len(diags[k])):

      proj_r = pr_diags[k-1][r]
      sols[k].append([ ])

      # e[i] est l'indice dans choice[k-1] de diags[k][r][i,i]
      e = [ pr_G[k](diags[k][r][i,i]) for i in range(4)]

      # puis on calcule les matrices de passage par force brute
      for s in range(len(diags[k])):
        if last_ring and s >= r:
          break

        proj_s = pr_diags[k-1][s]
        sols[k][r].append([ ])
        
        soL_exists = False

        otn = lambda u, v: bil_form_eval(diags[k][s], u, v) == R[k].zero()

        for p_low in sols[k-1][proj_r][proj_s]:

          if last_ring and soL_exists:
            break

          print(f"[{k}] matrice {compt}/{tot_mat}\n")
          compt += 1

          fib_u = [ fibs_uvec[k-1][e[i]][s][p_low[i]] for i in range(4) ]

          if len(fib_u[0]) == 0 or len(fib_u[1]) == 0 or len(fib_u[2]) == 0 or len(fib_u[3]) == 0:
            continue

          for t1 in fib_u[0]:
            u1 = uvec[k][e[0]][s][t1]

            if last_ring and soL_exists:
              break
            
            for t2 in fib_u[1]:
              u2 = uvec[k][e[1]][s][t2]

              if last_ring and soL_exists:
                break
              if not otn(u1, u2):
                continue

              for t3 in fib_u[2]:
                u3 = uvec[k][e[2]][s][t3]

                if last_ring and soL_exists:
                  break
                if not (otn(u1, u3) and otn(u2, u3)):
                  continue

                for t4 in fib_u[3]:
                  u4 = uvec[k][e[3]][s][t4]

                  if last_ring and soL_exists:
                    break
                  if not (otn(u1, u4) and otn(u2, u4) and otn(u3, u4)):
                    continue

                  p = mat_types[k]([u1, u2, u3, u4])

                  assert p * diags[k][s] * p.transpose() == diags[k][r], "ERREUR"

                  sols[k][r][s].append([t1, t2, t3, t4])
                  soL_exists = True



  # On construit maintenant les matrices de relations pour chaque k
  rel_mats = [ ]
  vec_rel = [ ]
  subs = lambda u, v: [ u[i] - v[i] for i in range(len(u)) ]

  for k in range(1,N+1):
    rel = [ ]
    vec = lambda r: diag_to_vec(diags[k][r], G[k], pr_G[k])

    vec_rel.append([ ])

    for r in range(len(diags[k])):
      u = vec(r)

      for s in range(r):
        v = vec(s)
        
        # S'il existe une solution...
        if len(sols[k][r][s]) != 0:
          vec_rel[k-1].append([u, v])
          rel.append(subs(vec(r), vec(s)))


    rel_mats.append(sympy.Matrix(remove_doubles(rel)).transpose())

  return rel_mats, vec_rel, choice
