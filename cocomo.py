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

  def __init__(i,file=None):
    i.rows,i.cols,i.name,i.all = [],{},[],[]
    if file:
      return i.create(i.lines(file))

  def create(i,src):
    width = None
    for j,line in enumerate(src):
      if j == 0:
        width = len(line)
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
        d,n  = y.dist(j[y.col], k[y.col], Table.missing)
        ds  += d
        ns  += n
    return ds**0.5 / ns**0.5

def nearest(row1, t, k=3):
  return sorted([(t.dist(row1,row2), row2)
                 for row2 in t.rows ])[1:k+1]
      
if __name__ == '__main__':
  f= "data/nasa93.csv"
  t = Table(file=f)
  print(t.cols["nums"],t.rows[0])
  print(t.rows[0])
  for row in nearest(t.rows[0], t, k=3):
    print(row)
