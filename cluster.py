from __future__ import print_function, division
import sys
sys.dont_write_bytecode=True

from config import *
from sample import *

"""
tbl=o(rows=list of lists
      pos = o(syms= index of nonNumeric indepedents
               nums= index of numeric indepdents
               objs= indenx of numeric classes)
"""

def cluster( tbl ):
  def cluster1(rows):
    t = o(has=rows, col=None,
          mid=None, left=None, right=None)
    if len(rows) >= small:
      # find obj with max var
      sd = 0
      ## tod do combine the sort and divide as one thing
      for col1 in pos.objs:
        mid, sd1 = minSd([ row[col1] for row in rows ])
        if sd1 > sd:
          sd, t.col, t.mid = sd1, col, mid
      # split
      l,r = [],[]
      for row in rows:
        what = l if row[ t.col ] <= t.mid else r
        what.rows += [rows]
      # recurse
      t.left  = cluster1( l )
      t.right = cluster1( r )
    return t
  pos = tbl.pos
  small = max(len(tbl.rows)**THE.groups.cull,
               THE.groups.minGroup)
  return cluster1( tbl.rows)
    
 def midZsd(vals):
    n   = len(vals)
    lo  = int(0.05*n)
    hi  = int(0.95*n)
    lst = sorted(vals)[lo:hi]
    mid = lst[ len(lst) // 2 ]
    min = tmp[ 0]
    max = tmp[-1]
    zsd = Num([(x - min)/(max - min + 1e-32)
               for x in lst]).sd()
    return mid, zsd
