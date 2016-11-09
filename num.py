from __future__ import print_function, division
import sys
sys.dont_write_bytecode=True

from config import *

class Num(o):
  HEDGES = THE.num.hedges # 0.38
  CONF= THE.num.conf # 0.95
  def __init__(i,inits=[]):
    has(i, mu=0, n=0, m2=0, hi=-1e32,lo=1e32)
    map(i.add, inits)
  def add(i,x):
    i.n += 1
    if x > i.hi: i.hi=x
    if x < i.lo: i.lo=x
    delta = x - i.mu
    i.mu += delta/i.n
    i.m2 += delta*(x - i.mu)
    return x 
  def sub(i,x):
    i.n   = max(0,i.n - 1)
    delta = x - i.mu
    i.mu  = max(0,i.mu - delta/i.n)
    i.m2  = max(0,i.m2 - delta*(x - i.mu))
  def sd(i):
    return 0 if i.n <= 2 else (i.m2/(i.n-1))**0.5
  def norm(i,x):
    tmp = (x - i.lo) / (i.hi - i.lo + 10**-32)
    return max(i.lo, min(i.hi,tmp))
  def smallEffect(i,j):
    "Hedges effect size test."
    small = Num.HEDGES
    num   = (i.n - 1)*i.s**2 + (j.n - 1)*j.s**2
    denom = (i.n - 1) + (j.n - 1)
    sp    = ( num / denom )**0.5
    delta = abs(i.mu - j.mu) / sp  
    c     = 1 - 3.0 / (4*(i.n + j.n - 2) - 1)
    return delta * c < small
 def significantlyDifferent(i,j,
          nums= {0.95: {5:2.015, 10:1.812, 15:1.753,
                        20:1.725, 25:1.708, 30:1.697}
                 0.99: {5:3.365, 10:2.764, 15:2.602,
                        20:2.528, 25:2.485, 30:2.457}}):   
   df     = min(i.n - 1, j.n - 1)
   n      = min(30,int(df/5 + 0.5)*5)
   delta  = abs(i.mu - j.mu)
   si, sj = i.sd(), j.sd()
   tmp    = delta/((si/i.n + sj/j.n)**0.5) if si+sj else 1
   return  tmp > nums[conf][n]
 def different(i,j):
   return not smallEffect(i,j) and significantlyDifferent(i,j)

