# -*- coding: iso-8859-1 -*-
from distutils.core import setup
import py2exe
import sys
import os
import os.path
sys.argv.append ('py2exe')
setup (
    options    = 
        {'py2exe': 
            { "bundle_files" : 1    # 3 = don't bundle (default) 
                                     # 2 = bundle everything but the Python interpreter 
                                     # 1 = bundle everything, including the Python interpreter
            , "compressed"   : False  # (boolean) create a compressed zipfile
            , "unbuffered"   : False  # if true, use unbuffered binary stdout and stderr
            , "includes"     : 
                [ "Tkinter", "Tkconstants","tkintertable"

                ]
            , "excludes"      : ["tcl", ]
            , "optimize"     : 0  #-O
            , "packages"     : 
                [ 
                ]
            , "dist_dir"     : "foo"
            , "dll_excludes": ["tcl85.dll", "tk85.dll"]
            ,               
            }
        }
    , windows    = 
        ["caritas.py"
        ]
    , zipfile    = None
    # the syntax for data files is a list of tuples with (dest_dir, [sourcefiles])
    # if only [sourcefiles] then they are copied to dist_dir 
    , data_files = [   os.path.join (sys.prefix, "DLLs", f) 
                   for f in os.listdir (os.path.join (sys.prefix, "DLLs")) 
                   if  (   f.lower ().startswith (("tcl", "tk")) 
                       and f.lower ().endswith ((".dll", ))
                       )
                    ] 

    , 
)