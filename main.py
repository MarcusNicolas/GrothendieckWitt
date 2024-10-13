import rings
from GW_presentation import GW_matrices
from MW_presentation import MW_matrix

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
