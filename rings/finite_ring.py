import equiv
from .ring import Ring

class FiniteRing(Ring):
  # Renvoie l'ensemble des éléments
  @staticmethod
  def elements():
    raise NotImplementedError("'elements' non implémentée.")
  
  def __hash__(self):
    raise NotImplementedError("Fonction de hash non implémentée.")
  

def units(finite_ring_type):
  elements = finite_ring_type.elements()

  return { x for x in elements if any(x*y == finite_ring_type.unit() for y in elements) }

# Prend un anneau fini R en entrée, et renvoie le couple (G, pr_G) où
# - cl: list(list(R)) est la liste des classes d'équivalence des unités de R modulo les carrés
# - pr : R -> option(int) prend un élément de R et renvoie sa classe s'il
#   est inversible, None sinon
def units_mod_sq(finite_ring_type):
  el = finite_ring_type.elements()
  u = units(finite_ring_type)
  sq = { x*x for x in u }

  G, _ = equiv.classes(list(u), lambda x, y : any(a*x == y for a in sq))
  ring_idx = { finite_ring_type.zero(): None }

  for x in el:
    ring_idx[x] = None

  for i in range(len(G)):
    for x in G[i]:
      ring_idx[x] = i

  return G, lambda x: ring_idx[x]