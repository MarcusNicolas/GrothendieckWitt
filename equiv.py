# On prend une liste munie d'une rel d'équivalence, et on renvoie la liste
#   des classes d'équivalence
def classes(dom, equiv):
  classes = []
  mark = [ True for _ in dom ]
  ref = [ None for _ in dom ]


  for i in range(len(dom)):
    if mark[i]:
      classe = [ ]
      m = len(classes)

      for j in range(len(dom)):
        if mark[j] and equiv(dom[i], dom[j]):
          mark[j] = False
          ref[j] = m
          classe.append(dom[j])
        
      classes.append(classe)
    
  return classes, lambda i: classes[ref[i]]
