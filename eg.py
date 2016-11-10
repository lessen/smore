from __future__ import print_function, division
import sys,re,traceback
sys.dont_write_bytecode=True

from config import *

PASS, FAIL = 0,0

def egs():
  "Report status of all tests."
  p,f = PASS,FAIL
  print("\n# PASS= %s FAIL= %s %%PASS = %s%%"  % (
    p,f, int(round(p*100/(p+f+0.001)))))

def eg(f):
  "Run one test."
  global PASS, FAIL
  if THE.all.brave: return f
  try:
    print(";;;;;;;;;; %s " % f.__name__)
    if f.__doc__:
      print("# "+ re.sub(r'\n[ \t]*',"\n# ",f.__doc__))
    f()
    print("# pass")
    PASS += 1
  except Exception,e:
    import traceback
    FAIL += 1
    print(traceback.format_exc()) 
  return f
