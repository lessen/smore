from __future__ import print_function, division
import sys,argparse
sys.dont_write_bytecode=True

"""---------------------------------------------------
Options system
This code is in the base since many classes have options
(magic config params).
Expand the shorthand (h,x=y) to command-line options
(as understood by the Python ArgumentParser class).
Use h as the help text.
Enable --x as a command line options. 
Use x as a key for a default value. 
Use y as the default (except for lists, see below)
Finally, use y to set expectations for args.
If y == False, then the flag --x sets y=True
If y isa lst, then range==lst and default is lst[0].
If y isa float, then expect a float.
If y isa integer, the expect an int.
Else expect a string.
After expansion, set up an Argument parser and automatically
handle all its quirky flags.
""" 

from o import *

def h(help,**d):
  key,val = d.items()[0]
  default = val[0] if isinstance(val,list) else val
  # step0: remember defaults
  out = dict(default=default)
  add = lambda **d : out.update(d) # convenience function for adding args
  # step1: Set type and meta var
  if   val is  not False: 
    if   isinstance(default,int  ): add(metavar= "I", type= int)
    elif isinstance(default,float): add(metavar= "F", type= float)
    else                          : add(metavar= "S", type= str)
  # step2: add help and type-specific misc flags
  if   val is False :        add(help=help, action="store_true")
  elif isinstance(val,list): add(help=help, choices=val)
  else:                      add(help=help + ("; e.g. %s" % str(val)))
  # step3: add "--" to key and return key and out
  return key, out
      
def options(prog, before, after, **d):
  """Convert dictionary 'd' to command line options
     divided into comand-line groups (one for every key
     in 'd'."""
  parser = argparse.ArgumentParser(
               prog        = prog,
               description = before,
               epilog      = after, 
               formatter_class=argparse.RawTextHelpFormatter)
  inside,out = {}, o()
  for context in sorted(d.keys()):
    out[context] = o()
    description = d[context][0]
    group = parser.add_argument_group(context, description)
    for key,rest in d[context][1:]:
      group.add_argument("--" + key,**rest)
      assert key not in inside, 'keys cannot repeat' 
      inside[key] = context      
  parsed = vars(parser.parse_args())
  for key,val in parsed.items():
    out[inside[key]][key]= val
  return out
