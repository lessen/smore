from __future__ import print_function, division
import sys
sys.dont_write_bytecode=True

from config import *
from sample import *

"""
tbl=o(rows= list of rows
      cols= o(syms= index of nonNumeric indepedents
               nums= index of numeric indepdents
               objs= indenx of numeric classes)
"""

%XXXX cache objective stats in t
def cluster(rows, cols ):
  def cluster1(rows):
    t = o(has=rows, col=None,
          mid=None, left=None, right=None)
    if len(rows) >= small:
      mid = int(len(rows) // 2)
      sd,mid,col = 0,None,None
      for col1 in cols.objs:
        sd1,mid1 = zsd([row[col1] for row in rows])
        if sd1 > sd:
          sd,mid,col = sd1,mid1,col1
      l,r = [],[]
      for row in rows:
        x     = row[col]
        what  = l if x <= mid else r
        what += [x]
      left  = cluster1( l )
      right = cluster1( r )
      if len(rows) < 2*small:
        if different(left,right):
          t.mid  = mid
          t.col  = col
          t.left = left
          t.right= right       
    return t
  small = max(len(tbl.rows)**THE.groups.cull,
               THE.groups.minGroup)
  return cluster1( tbl.rows)
    
 def zsd(rows):
   rows    = sorted(rows)
   mid     = rows[ n // 2 ]
   lo, hi  = int(0.05*n), int(0.95*n) + 1
   min,max = rows[lo], rows[hi]
   num     = Num()
   for i in xrange(min,max):
     x = rows[i][col]
     num( (x - min)/(max - min + 1e-32) )
   return num.sd(), rows[ n // 2 ]
   
def different(
