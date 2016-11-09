from __future__ import print_function, division
import sys
sys.dont_write_bytecode=True

from config import *

class Sample(o):
  SAMPLES      = THE.sample.samples
  """
  Keep a random sample of values.
  """
  def __init__(i, init=[],max=None):
    max = max or Sample.SAMPLES
    has(i, n=0, some=[], max=max)
    map(i.add, init)
  def __call__(i,x):
    i.n += 1
    now  = len(i.some)
    if now < i.max:
      i.some += [x]
    elif r() <= now/i.n:
      i.some[ int(r() * now) ]= x
