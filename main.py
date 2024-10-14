import rings
from GW_presentation import GW_matrices
from MW_presentation import MW_matrix, remove_doubles, solution_exists

import sympy.matrices.normalforms

def GW_matrices_output(R, mor):
  N = len(R)
  GW_mat, vec_rel, choice = GW_matrices(R, mor)

  for k in range(N):
    G, pr_G = rings.units_mod_sq(R[k])
    MW_mat = MW_matrix(R[k], G, pr_G)

    
    MW_smith = sympy.matrices.normalforms.smith_normal_form(MW_mat, domain=sympy.ZZ)
    GW_smith = sympy.matrices.normalforms.smith_normal_form(GW_mat[k], domain=sympy.ZZ)

    with open(f"GW_{R[k].__name__}.txt", "w") as file:
      file.write(f"Classes: {choice[k+1]}\n\n")
      file.write(f"MW_rel: {str(MW_mat.transpose())}\n")
      file.write(f"MW_smith: {str(MW_smith.transpose())}\n----------------\n\n")
      file.write(f"GW_rel: {str(GW_mat[k].transpose())}\n")
      file.write(f"GW_smith: {str(GW_smith.transpose())}\n----------------\n\n")
      file.write(f"Relations (pour GW): {str(vec_rel[k])}")



N = 4

# Groupes cycliques

p = [ 2**(k+1) for k in range(N) ]
R = [ rings.create_cyclic_class(p[k]) for k in range(N) ]
mor = [ (lambda i: ( lambda x: R[i](x.value) ))(k) for k in range(N-1) ]


# Polynômes tronqués

C = R[0]
S = [ rings.create_trunc_pol_class(k, C) for k in range(1, N+1) ]
mor_cyc = [ (lambda i: ( lambda p: S[i](p.coeffs) ))(k) for k in range(N-1) ]

S_eff = [ rings.create_eff_ring(S[k], list(S[k].elements())) for k in range(len(S)) ]

mor_idx = [ (lambda i: rings.precompute(list(range(len(S_eff[i+1].data_el))), (lambda t: S_eff[i].encapsulate(mor_cyc[i](S_eff[i+1](t).value())).idx )))(k) for k in range(len(mor_cyc)) ]

mor_eff = [ (lambda i: lambda x: S_eff[i](mor_idx[i](x.idx)))(k) for k in range(len(mor_cyc)) ]




T = R[2]
G, pr_G = rings.units_mod_sq(T)
u = list(rings.units(T))

rels = []


print(T.__name__)


for a in u:
  for b in u:
    for c in u:
      for d in u:
        rel = [ 0 for _ in G ]

        rel[pr_G(a)] += 1
        rel[pr_G(b)] += 1
        rel[pr_G(c)] += 1
        rel[pr_G(d)] += 1

        rel[pr_G(b+c+d)] -= 1
        rel[pr_G(a+c+d)] -= 1
        rel[pr_G(a+b+d)] -= 1
        rel[pr_G(a+b+c)] -= 1

        
        rels.append(rel)


MW_rels = MW_matrix(T, G, pr_G).transpose()

rels = sympy.Matrix(remove_doubles(rels)).col_join(MW_rels)

GW_rels = sympy.Matrix([[-1, 1, 1, -1], [-2, 0, 2, 0], [-1, -1, 1, 1], [0, -2, 0, 2], [-4, 4, 0, 0], [-2, 4, -2, 0], [-1, 3, 1, -3], [-3, 3, -1, 1], [-1, 3, -3, 1], [-2, 2, 2, -2], [-4, 2, 0, 2], [-2, 2, -2, 2], [-3, 1, 3, -1], [-3, 1, -1, 3], [-1, 1, -3, 3], [-4, 0, 4, 0], [0, -4, 4, 0], [0, -2, 4, -2], [-3, -1, 3, 1], [-2, -2, 2, 2], [-1, -3, 1, 3], [-4, 0, 0, 4], [-2, 0, -2, 4], [0, -4, 0, 4], [0, 0, -4, 4]])
GW_mat = GW_rels.transpose()

mat = rels.transpose()
print(mat)

MW_solver = solution_exists(MW_rels)

rels_explains_GW = all(MW_solver(ln) for ln in GW_rels)

print(rels_explains_GW)

mat = mat.transpose()


