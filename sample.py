from __future__ import print_function, division
import sys
sys.dont_write_bytecode=True

from config import *
from num    import *

class Sample(o):
  SAMPLES      = THE.sample.samples
  """
  Keep a random sample of values.
  """
  def __init__(i, init=[],max=None,id=Nome):
    max = max or Sample.SAMPLES
    has(i, n=0, some=[], max=max, id=id)
    map(i.add, init)
  def __call__(i,x):
    i.n += 1
    now  = len(i.some)
    if now < i.max:
      i.some += [x]
    elif r() <= now/i.n:
      i.some[ int(r() * now) ]= x
  def midZsd(i):
    n   = len(i.some)
    lo  = int(0.05*n)
    hi  = int(0.95*n)
    lst = sorted(i.some)[lo:hi]
    mid = lst[ len(lst) // 2 ]
    min = tmp[ 0]
    max = tmp[-1]
    zsd = Num([(x - min)/(max - min + 1e-32)
               for x in lst]).sd()
    return mid, zsd
