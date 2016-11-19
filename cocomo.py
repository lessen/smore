from __future__ import division,print_function
import sys,string,re, math
sys.dont_write_bytecode=True

class Num:
  def __init__(i,txt,col):
    i.name,i.col, i.lo, i.hi = txt,col,1e32,-1e32
  def compile(i,x):
    return float(x)
  def add(i,x):
    i.lo = min(x, i.lo)
    i.hi = max(x, i.hi)
    return x
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
    i.name,i.col, i.counts = txt,col,{}
  def compile(i,x):
    return x
  def add(i,x):
    i.counts[x] = i.counts.get(x,0) + 1
    return x
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
  
  def __init__(i,file):
    i.rows,i.cols = [],{}
    width = None
    for j,line in enumerate(i.lines(file)):
      width = width or len(line)
      assert width == len(line), "wanted %s cells" % width
      if j > 0:
        i.rows += [ i.compiles(line) ]
      else:
        i.header(line)
        
  def compiles(i,line):
    for log in i.cols["all"]:
      x = log.compile( line[log.col] )
      log.add(x)
      line[log.col] = x
    return line
  
  def header(i,line):
    for col,cell in enumerate(line):
      if cell[0] != Table.ignore:
        for key,(char,what) in Table.cols.items():
          if cell[0] == char:
            new = what(cell,col)
            i.cols[ key ] = i.cols.get( key, []) + [new]
            i.cols["all"] = i.cols.get("all",[]) + [new]
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
              
  def dist(i, j,k):
    ds,ns = 0,1e-32
    for log in i.cols["all"]:
      d,n  = log.dist(j[log.col], k[log.col], Table.missing)
      ds  += d
      ns  += n
    return ds**0.5 / ns**0.5
      
def dists(t):
  ds = {}
  for a,row1 in enumerate(t.rows):
    for b,row2 in enumerate(t.rows):
      ds[a] = ds.get(a,[])
      ds[b] = ds.get(b,[])  
      if a > b:
        d      = t.dist(row1,row2)
        ds[a] += [(d, a, b)]
        ds[b] += [(d, b, a)]
  for a,tuples in ds.items():
    ds[a] = sorted(tuples)
  return ds
      
if __name__ == '__main__':
  f= "data/nasa93.csv"
  t = Table(f)
  print(t.cols["nums"],len(t.rows))
  print(dists(t)[0][:5])
