#!/usr/bin/python3
import time

#function that don't start with _ show up as commands
#CMD: test, Showes args given
def test(args):
    yield 'clear'
    yield 'echo "' + str(janit.render_where) + '"'
    janit.os.environ['PS1'] = "TEST> " # visible in this process + all children


def enter_term(args):
    #user visable string is printed
    janit.debug("focus set to bash, Ctrl+Down to enter menu")
    #Enter terminal and exit
    return (['...']) # you can also yield ... to enter terminal

#not a command, this is a support function
def _thing():
    pass

#tab completion for the test CMD
def tab_test(*args):
    janit.debug("in tab def: " + str(args), Level=2)
    full_cm_ds = ['test example1','test if it works', 'testing']
    return full_cm_ds
