import argparse

import rings
from main import GW_matrices_output

parser = argparse.ArgumentParser(description="GW_trunc_pol")
parser.add_argument("N", type=int, help="N")

args = parser.parse_args()


C = rings.create_cyclic_class(2)
R = [ rings.create_trunc_pol_class(k, C) for k in range(1, args.N+1) ]
mor = [ (lambda i: ( lambda p: R[i](p.coeffs) ))(k) for k in range(args.N-1) ]

R_eff = [ rings.create_eff_ring(R[k], list(R[k].elements())) for k in range(len(R)) ]

mor_idx = [ (lambda i: rings.precompute(list(range(len(R_eff[i+1].data_el))), (lambda t: R_eff[i].encapsulate(mor[i](R_eff[i+1](t).value())).idx )))(k) for k in range(len(mor)) ]

mor_eff = [ (lambda i: lambda x: R_eff[i](mor_idx[i](x.idx)))(k) for k in range(len(mor)) ]


GW_matrices_output(R_eff, mor_eff, "pol")

