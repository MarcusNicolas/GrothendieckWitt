import rings

# import MW_presentation
from GW_presentation import GW_base_change, fibs_fun
from MW_presentation import MW_matrix

A = rings.create_cyclic_class(128)
G, pr_G = rings.units_mod_sq(A)

print(G)

relations = MW_matrix(A, G, pr_G)

print(relations)





N = 1 # On veut Z/2^NZ

p = [ 2**(k+1) for k in range(N) ]
R = [ rings.create_cyclic_class(p[k]) for k in range(N) ]


mor = [ (lambda i: ( lambda x: R[i](x.value) ))(k) for k in range(N-1) ]


sols, diags, build_mat = GW_base_change(R, mor)
for k in range(1, N+1):
  print("--------------\n")
  print(f"Dans Z/{2**k}Z\n")

  for r in range(len(diags[k])):
    for s in range(len(diags[k])):
      continue
      #print(len(sols[k][r][s]))

'''
mor, choice, pr_G, diags, pr_diags, uvec, fibs_uvec = GW_base_change(R, mor)


for k in range(1, len(uvec)):
  print("--------------\n")
  print(f"Dans Z/{2**k}Z\n")

  for i in range(len(fibs_uvec[k-1])):
    proj_i = pr_G[k-1](mor[k-1](choice[k][i]))

    for r in range(len(fibs_uvec[k-1][i])):
      proj_r = pr_diags[k-1][r]

      for s in range(len(fibs_uvec[k-1][i][r])):
        for t in fibs_uvec[k-1][i][r][s]:
          print("Le vecteur: ")
          print(uvec[k][i][r][t])
          print("est unitaire au-dessus de ")
          print(uvec[k-1][proj_i][proj_r][s])
          print("pour la forme")
          print(diags[k][r])
          print("\n")
'''


'''
for k in range(len(diags)):
  print("Dans Z /", 2**k, "Z\n")

  for r in range(len(diags[k])):
    print(diags[k][r])
    if k > 0:
      print("(au-dessus de")
      print(diags[k-1][pr_diags[k-1][r]])
      print(")")
    print("\n")

  print("-------------\n")
'''


'''
# Notre anneau R est ici un Z/nZ
R = rings.create_cyclic_class(32)
Mat = rings.create_mat_class(2, R)

G, pr = rings.finite_ring.units_mod_sq(R)

print(pr(R(11)))
print(pr(R(0)))'''

#G, pr_G = cyclic_units_mod_sq(R)

#print(G)

#vecs, pr_vec = cyclic_list_diags(R, G, pr_G)



# Deux problèmes:
# 1) On veut regarder quels sont les relations (a_i) = (b_i) impliquées par
#    celles de la présentation MW (comment faire ?)
# 2) On veut regarder lesquelles de ces classes sont identifiées dans GW