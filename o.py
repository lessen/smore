from __future__ import print_function, division
import sys
sys.dont_write_bytecode=True

class o:
  """
  Basic class = dynamic updates+ pretty prints
  Also handles Javascript envy.  Javascript instance 
  fields can be accessed via thing.x or thing[x]. 
  Useful for data sources where there
  is names fields, and not methods. 
  This is in the base since it is needed by 'options'.
  """
  def __init__(i, **kwargs)  : i.__dict__.update(kwargs)
  def __getitem__(i, key)    : return i.__dict__[key]
  def __setitem__(i,key,val) : i.__dict__[key] = val
  def __repr__(i):
    show = [':%s %s' % (k, i.__dict__[k]) 
            for k in sorted(i.__dict__.keys()) 
            if k[0] is not "_"]
    txt = ' '.join(show)
    if len(txt) > 60:
      show = map(lambda x: '\t' + x + '\n', show)
    return '{' + ' '.join(show) + '}'
  
def has(i,**kwargs):
  "Easy inits"
  o.__init__(i,**kwargs)
