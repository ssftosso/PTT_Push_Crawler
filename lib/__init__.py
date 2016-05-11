import os, sys, inspect
from os.path import dirname, basename, isfile
import glob

 # realpath() will make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

 # use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

cmd_parentfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"..")))
if cmd_parentfolder not in sys.path:
    sys.path.insert(0, cmd_parentfolder)

modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = []
for f in modules:
    if isfile(f):
        f_name = basename(f)[:-3]
        if f_name != '__init__':
            __all__.append(f_name)

##for module in __all__:
##    print "[Module][Load][{:}]:{:}".format(module,__name__)
