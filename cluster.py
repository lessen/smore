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

def cluster( tbl0):
  def cluster1(tbl):
    t = o(has=tbl, pos=None, val=None, left=None, right=None)
    rows = tbl._rows
    if len(rows) >= small:
      cols  = sorted(tbl.cols.objs,
                     key = lambda z: z.sd(),
                     reversed=True)
      col   = cols[0]
      t.pos = col.pos
      t.val = sorted(col.sample.some)[ int(len(rows) / 2) ]
      tbll, tblr = tbl.clone(), tbl.clone()
      for row in rows:
        (tbll if row[ t.pos ] <= t.val else tblr)(row)
      t.left  = cluster1( tbll )
      t.right = cluster1( tblr )
    return t
 
  small = max(len(population)**THE.groups.cull,
               THE.groups.minGroup)
  return cluster1( tbl0)

