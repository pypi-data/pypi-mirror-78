#!/usr/bin/python 
# -*- coding: utf-8 -*-
import os
from . import config

__version_info__ = (0,2,20)
__version__ = '.'.join(map(str,__version_info__))

__base_path__ = 'feeds.txt'

def main():
 try:
  if os.path.isfile(__base_path__) and os.access(__base_path__, os.R_OK):
    os.mkdir('output')
 except FileExistsError:
    # directory already exists
   pass
 return config.init()
 
if __name__ == '__main__':
    main()
