import glob
import pip
import sys
from os import getcwd
from os.path import dirname, basename, isfile

sys.path.append(getcwd())

import Grapher
from rss2neo import RssFeeder
import Parser
import Recorder


modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]

libnames = ['unicodedata', 'validators', 'nltk', 'json', 'timeit', 'inflect', 'Pattern']
for libname in libnames:
    try:
        lib = __import__(libname)
    except:
        print sys.exc_info()
        pip.main(['install', libname])
    else:
        globals()[libname] = lib