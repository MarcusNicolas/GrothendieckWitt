import rings

# import MW_presentation
from GW_presentation import GW_matrices, fibs_fun
from MW_presentation import MW_matrix


N = 3 # On veut Z/2^NZ

p = [ 2**(k+1) for k in range(N) ]
R = [ rings.create_cyclic_class(p[k]) for k in range(N) ]


mor = [ (lambda i: ( lambda x: R[i](x.value) ))(k) for k in range(N-1) ]

GW_mat, choice = GW_matrices(R, mor)


for k in range(N):
  with open(f"GW cyclic{p[k]}.txt", "w") as file:
    file.write(f"Classes: {choice[k+1]}\n-----------------\n\n")
    file.write(str(GW_mat[k]))


# Deux problèmes:
# 1) On veut regarder quels sont les relations (a_i) = (b_i) impliquées par
#    celles de la présentation MW (comment faire ?)
# 2) On veut regarder lesquelles de ces classes sont identifiées dans GW