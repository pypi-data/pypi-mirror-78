#!/usr/bin/python 
import sys
import colorful as cf

cfail = cf.bold_red

def init():
  try:
   from . import nfs_main, styles
  except Exception as e:
   print(cfail(f"Fatal: {e}"))
   sys.exit(1)
  
  #return os.popen(f'{dir_path}/nfs_main.py').read()
  #run = lambda filename : exec(open(filename).read(), globals())
  #return run(f'{dir_path}/main.py')
  #fload = lambda filename : exec(open(filename).read(), globals())
  #return fload(f'{dir_path}/styles.py')
