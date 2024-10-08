import rings

# import MW_presentation
from GW_presentation import GW_base_change



N = 3 # On veut Z/2^NZ

p = [ 2**(k+1) for k in range(N) ]
R = [ rings.create_cyclic_class(p[k]) for k in range(N) ]


mor = [ (lambda i: ( lambda x: R[i](x.value) ))(k) for k in range(N-1) ]

test = GW_base_change(R, mor)


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