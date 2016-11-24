from __future__ import division,print_function
import sys,string,re, math
sys.dont_write_bytecode=True

class Num:
  def __init__(i,txt,col):
    i.name,i.col, i.lo, i.hi = txt,col,1e32,-1e32
    i.n, i.mu, i.m2 = 0,0,0
    i.use = True
  def compile(i,x):
    return float(x)
  def add(i,x):
    i.n += 1
    delta = x - i.mu
    i.mu += delta/i.n
    i.m2 += delta*(x - i.mu)
    i.lo = min(x, i.lo)
    i.hi = max(x, i.hi)
    return x
  def sd(i):
    return 0 if i.n <= 2 else (i.m2/(i.n-1))**0.5
  
  def norm(i,x):
    x = (x - i.lo) / (i.hi - i.lo + 1e-32)
    if x > 1: return 1
    if x < 0: return 0
    return x
  def dist(i,x,y,miss="?"):
    if x == miss and y == miss: return 0,0
    if x == miss:
      y = i.norm(y)
      x = 1 if i.norm(y) < 0.5 else 0
    elif y == miss:
      x = i.norm(x)
      y = 1 if i.norm(x) < 0.5 else 0
    else:
      x,y = i.norm(x), i.norm(y)
    return (x-y)**2, 1  
  def __repr__(i):
    return 'Num(%s,%s)' % (i.name,i.col)
  
class Sym:
  def __init__(i,txt,col):
    i.n,i.name,i.col, i.counts = 0,txt,col,{}
    i.use = True
  def compile(i,x):
    return x
  def add(i,x):
    i.n += 1
    i.counts[x] = i.counts.get(x,0) + 1
    return x
  def entropy(i):
    e = 0
    log2 = lambda x: math.log(x,2)
    for count in i.counts.values():
      p  = count/i.n
      e -= p*log2(p)
    return e
  def dist(i,x,y,miss="?"):
    if   x == miss and y == miss : return 0,0
    elif x == miss or  y == miss : return 1,1
    else: return (0,1) if x==y else (1,1)
  def __repr__(i):
    return 'Sym(%s,%s)' % (i.name,i.col)
        
class Table:
  whitespace = '[\n\r\t]'
  comments   = '#.*'
  sep        = ","
  ignore     = "-"
  missing    = '?'
  cols       = dict(less= ("<", Num),
                    more= (">", Num),
                    nums= ("$", Num),
                    syms= ("=", Sym))

  def __init__(i,file=None):
    i.rows,i.cols,i.all, i.names = [],{},[], []
    i.col2cell, i.cell2col = {}, {}
    for key in Table.cols.keys():
      i.cols[key] = []
    if file:
      return i.create(i.lines(file))

  def clone(i):
    t = Table()
    t.create([i.names[:]] + [row[:] for row in i.rows])
    return t
    
  def create(i,src):
    width = None
    for j,line in enumerate(src):
      if j == 0:
        width = len(line)
        i.names=line
        i.header(line)
      else:
        assert width == len(line), "wanted %s cells" % width
        i.rows += [ i.compile(line) ]

  def compile(i,line):
    for x in i.all:
      y = line[x.col] = x.compile( line[x.col] )
      x.add(y)
    return line
  
  def header(i,line):
    for col,cell in enumerate(line):
      i.col2cell[col] = cell
      i.cell2col[cell] = col
      if cell[0] != Table.ignore:
        for key,(char,what) in Table.cols.items():
          if cell[0] == char:
            new = what(cell,col)
            i.cols[ key ] = i.cols.get( key, []) + [new]
            i.all += [new]
            break
          
  def lines(i,file):
    doomed = re.compile('(' + Table.whitespace + '|' +  Table.comments + ')')
    with open(file) as fs:
      cache = []
      for line in fs:
        line = re.sub(doomed, "", line)
        if line:
          cache += [line]
          if line[-1] != ",":
            line  = "".join(cache)
            cache = []
            row   = map(lambda z:z.strip(),  line.split(Table.sep))
            if len(row)> 0:
              yield row
              
  def dist(i, j,k, what=["nums","syms"]):
    ds,ns = 0,1e-32
    for x in what:
      for y in i.cols[x]:
        if y.use:
          d,n  = y.dist(j[y.col], k[y.col], Table.missing)
          ds  += d
          ns  += n
    return ds**0.5 / ns**0.5

def median(lst):
  lst = sorted(lst)
  l   = len(lst)
  if l < 3:
    return (lst[0] + lst[-1])/2
  m   = l // 2
  return lst[m] if l % 2 else (lst[m] + lst[m+1])/2

def percentiles(lst):
  all = sorted(lst)
  m   = len(lst)
  lo  = int(m*0.05)
  hi  = int(m*0.95)
  most= all[lo:hi]
  q   = len(most)//10
  return [most[0], most[q], most[q*3], most[q*5], most[q*7], most[q*9], most[-1]]

def sa(wantgot):
  sampled = median( [want for want,_ in wantgot] )
  denom   = sum([ abs(got - sampled) for    _,got in wantgot ]) 
  nom     = sum([ abs(got - want)    for want,got in wantgot ]) 
  return nom / (denom + 1e-32)
    
def neighbors(row1, t):
  return sorted(
               [(t.dist(row1,row2), row2)
                for row2 in t.rows ])

def threeVal(t):
  def swap(x):
    if x in ['vl','l']     : return 'l'
    if x in ['xh','vh','h']: return 'h'
    return x
  for i,row in enumerate(t.rows):
    for sym in t.cols["syms"]:
      row[sym.col] = swap(row[sym.col])
  return t
    
def knn(row,t,k=5, goal=-1, combine = median,prep = lambda z:z,ent=None,sd=None):
  t      = prep(t)
  t      = prune(ent,sd)
  second = lambda z:z[1]
  dists = map(second, neighbors(row,t))
  nears = dists[1:k+1]
  gots  = [x[goal] for x in nears]
  got   = combine(gots)
  return got

def knnC(row,t,k=5, goal=-1, combine = None,prep = lambda z:z,weight=1,ent=None,sd=None):
  t      = prep(t)
  t      = prune(t,ent,sd)
  second = lambda z:z[1]
  dists  = neighbors(row,t)
  nears  = dists[1:k+1]
  gots   = [(d,x[goal]) for d,x in nears]
  denom,nom = 0,0
  for d,got in gots:
    d     += 1e-32
    w      = (1/d)**weight
    nom   += w*got
    denom += w
  return nom/denom

def triangle(l):
  n     = len(l)
  denom = sum([(n-i) for i,x in enumerate(l)])
  return sum((n-i)*x for i,x in enumerate(l))/denom

def prune(t,ent=None, sd=None):
  if ent:
    prune1(t,"syms",ent,lambda z: z.entropy)
  if sd:
    prune1(t,"nums",sd,lambda z: z.sd())
  return t
    
def prune1(t,what,where,how):
  all = t.cols[what]
  for col in all:
    all.use = False
  good = sorted(all,key=how)
  best = syms[where:] if where < 0 else syms[:where]
  for col in best:
    all.use = True
  return t
    
_  = None;  Coc2tunings = [[
#              vlow  low   nom   high  vhigh  xhigh   
# scale factors:
'Flex',        5.07, 4.05, 3.04, 2.03, 1.01,    _],[
'Pmat',        7.80, 6.24, 4.68, 3.12, 1.56,    _],[
'Prec',        6.20, 4.96, 3.72, 2.48, 1.24,    _],[
'Resl',        7.07, 5.65, 4.24, 2.83, 1.41,    _],[
'Team',        5.48, 4.38, 3.29, 2.19, 1.01,    _],[
# effort multipliers:        
'acap',        1.42, 1.19, 1.00, 0.85, 0.71,    _],[
'aexp',        1.22, 1.10, 1.00, 0.88, 0.81,    _],[
'cplx',        0.73, 0.87, 1.00, 1.17, 1.34, 1.74],[
'data',           _, 0.90, 1.00, 1.14, 1.28,    _],[
'docu',        0.81, 0.91, 1.00, 1.11, 1.23,    _],[
'ltex',        1.20, 1.09, 1.00, 0.91, 0.84,    _],[
'pcap',        1.34, 1.15, 1.00, 0.88, 0.76,    _],[ 
'pcon',        1.29, 1.12, 1.00, 0.90, 0.81,    _],[
'plex',        1.19, 1.09, 1.00, 0.91, 0.85,    _],[ 
'pvol',           _, 0.87, 1.00, 1.15, 1.30,    _],[
'rely',        0.82, 0.92, 1.00, 1.10, 1.26,    _],[
'ruse',           _, 0.95, 1.00, 1.07, 1.15, 1.24],[
'sced',        1.43, 1.14, 1.00, 1.00, 1.00,    _],[ 
'site',        1.22, 1.09, 1.00, 0.93, 0.86, 0.80],[ 
'stor',           _,    _, 1.00, 1.05, 1.17, 1.46],[
'time',           _,    _, 1.00, 1.11, 1.29, 1.63],[
'tool',        1.17, 1.09, 1.00, 0.90, 0.78,    _]]

def COCOMO2(project,  a = 2.94, b = 0.91, 
                      tunes= Coc2tunings):
  sfs,ems,kloc   = 0, 5 ,22        
  scaleFactors, effortMultipliers = 5, 17
  for i in range(scaleFactors):
    sfs += tunes[i][project[i]]
  for i in range(effortMultipliers):
    j = i + scaleFactors
    ems *= tunes[j][project[j]] 
  return a * ems * project[kloc] ** (b + 0.01*sfs)

class Rx():
  def __init__(i,txt, get):
    i.txt, i.mres, i.wantgot = txt, [], []
    i.get = get
  def __call__(i,row,want):
    got = i.get(row)
    i.mres += [ (want - got) / want ]
    i.wantgot += [ (want,got) ]
  def report(i,**d):
    p = lambda x:  int(x*100)
    i.mres = sorted(i.mres)
    print(map(p, percentiles( i.mres )),i.txt,d)

def loo(f,g):
  t = Table(file=f)
  for k in [1,2,3,4,5]:
    print("#")
    rs = [Rx("k=%snn"      % k,    lambda row: knn(row,  t.clone(), goal=g, k=k))
          #,Rx("k=%snn.3val" % k,   lambda row: knn(row,  t.clone(), goal=g, k=k, prep=threeVal))
          #Rx("k=%snn.w" % k, lambda row: knnC(row,  t.clone(), goal=g, k=k))
          #,Rx("k=%snn.w2.3val" % k, lambda row: knn(row,  t.clone(), goal=g, k=k,prep=threeVal,ent=-5))
          #,Rx("k=%snnC.w2.3val" % k, lambda row: knnC(row,  t.clone(), goal=g, k=k,prep=threeVal,ent=-5))
         #,Rx("triangle",           lambda row: knn(row,  t.clone(), goal=g, k=k, combine= triangle))
         #,Rx("baseline",           lambda row: median(row[g] for row in t.clone().rows))       
         ]
    for row in t.rows:
      for r in rs:
        r(row,row[g])
    for r in rs: r.report()
  

if __name__ == '__main__':
  f = "data/nasa93_2000.csv"
  g = -3
  if len(sys.argv) > 1: f = sys.argv[1]
  if len(sys.argv) > 2: g = int(sys.argv[2])
  loo(f,g)

