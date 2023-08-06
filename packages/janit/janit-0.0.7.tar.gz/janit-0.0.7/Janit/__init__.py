import os

import time
import os
import sys
import signal
import threading
import subprocess
import re
import random
import struct
import importlib
import socket
import glob
import string
import signal
import mmap
import tempfile

#import curses
import fcntl
import termios
try:
    import pyte
except Exception:
    print("\nError finding pyte.\nTry running: sudo pip3 install pyte")
    exit()
import pty
import tty

try:
    import ewmh
    WM = True
except Exception:
    print("Error finding ewmh.\nTry running: sudo pip3 install ewmh")
    print("Disabled window manager")
    WM = False
#import importlib

#import ./Janit/*.py
#Something like: from Janit.* import *
script_path = os.path.dirname(os.path.realpath(__file__))



########################################################
################ Import ./Janit/core/* #################
########################################################

init_modules = []
imported_cmd = []


#setup init_modules
for file_with_cm_ds in os.listdir(script_path + "/core/"):

    #filter stuff
    if "__" in file_with_cm_ds:
        continue
    #lol... builds somthing like:  ['rename', 'tell'] by reading ./plugins/*
    init_modules.append(file_with_cm_ds.split('.py')[0])

#TODO don't import files that use used names
sys.path.insert(0, script_path + '/core/')

for mod in init_modules:
    #don't import ewmh_core if we don't need it
    #if not WM and mod == "ewmh_core":
    print("Loading:::: " + mod)
    if not WM and mod == "desktop":
        print("skipping: : " + mod)
        continue
    mod_file = script_path + "/core/" + mod + ".py"
    #print(mod_file)
    script = ""
    for python_line in open(mod_file).readlines():
        script = script + python_line
        #don't add CORE file defs to auto complete
    #print("running: " + script)

    try:
        exec(script)
    except Exception as e:
        print('Error Loading ' + mod_file)
        #Error loading, Exit with error
        raise e
        #exit()


#########################################
#import CMDs#############################
#########################################
print("TEST")
sys.path.insert(0, script_path + "/cmd/")
import_CMDs_to_run = []
for file_with_cm_ds in os.listdir(script_path + "/cmd/"):
    if file_with_cm_ds.startswith("__"):
        continue
    import_CMDs_to_run.append(script_path + "/cmd/" + file_with_cm_ds)

