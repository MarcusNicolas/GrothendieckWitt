import rings
from GW_presentation import GW_matrices
from MW_presentation import MW_matrix


def GW_matrices_output(R, mor, pfx):
  N = len(R)
  GW_mat, vec_rel, choice = GW_matrices(R, mor)

  for k in range(N):
    G, pr_G = rings.units_mod_sq(R[k])
    MW_mat = MW_matrix(R[k], G, pr_G)

    with open(f"GW_{pfx}{k}.txt", "w") as file:
      file.write(f"Classes: {choice[k+1]}\n\n")
      file.write(f"MW: {str(MW_mat)}\n")
      file.write(f"GW: {str(GW_mat[k])}\n----------------\n\n")
      file.write(f"Relations (pour GW): {str(vec_rel[k])}")
