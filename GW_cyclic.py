import argparse

import rings
from main import GW_matrices_output

parser = argparse.ArgumentParser(description="GW_cyclic")
parser.add_argument("N", type=int, help="N")

args = parser.parse_args()


p = [ 2**(k+1) for k in range(args.N) ]
R = [ rings.create_cyclic_class(p[k]) for k in range(args.N) ]
mor = [ (lambda i: ( lambda x: R[i](x.value) ))(k) for k in range(args.N-1) ]

GW_matrices_output(R, mor)
