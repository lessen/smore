from collections import defaultdict

def thing():
  return (1,0)

d1 = defaultdict(int)
d2 = defaultdict(list)

d1["a"] += 1
d2["a"] += [1,2,3,45]
print d1
print d2
