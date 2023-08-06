#!/usr/bin/python3


#############################################
####################LIST#####################
#############################################
def List(args):
    full_cmd = " ".join(args)

    #janit.println(full_cmd)
    if full_cmd == "users active":
        yield('who')
    elif full_cmd == "users":
        yield("...")
        yield('cut -d: -f1 /etc/passwd | less')
    elif full_cmd == "groups":
        yield("...")
        yield('cut -d: -f1 /etc/group | sort | less')
    elif full_cmd == "cpu-info":
        yield("...")
        yield('lscpu | less')
    elif full_cmd == "hardware":
        yield("...")
        janit.println('This should take some time...')
        yield('sudo hwinfo --short | less')
    elif full_cmd == "block-devices":
        yield('lsblk')


#tab completion for the test CMD
def tab_list(*args):
    full_cmds = ['list users', 'list groups', 'list block-devices', 'list cpu-info', 'list hardware']
    cmd_str = " ".join(args)
    #groups: cut -d: -f1 /etc/group | sort | less
    #users: cut -d: -f1 /etc/passwd | less
    #janit.println(cmd_str)
    if cmd_str.strip().startswith('users'):
        full_cmds.append("list users active")

    janit.debug("in tab def: " + str(args), Level=2)
    return full_cmds


#############################################
####################SETUP####################
#############################################
def setup(args):
    full_cmd = " ".join(args)
    if full_cmd.lower() == "display":
        #alow root to use x11 session (Use term 0)
        #TODO: Let user know: non-network local connections being added to access control list
        janit.bash_run("xhost +local:", ctl_term=True)
        yield 'export DISPLAY=:0'
        janit.println("\nDisplay setup")
        yield '...'

def tab_setup(*args):
    full_cmds = ['setup display']
    cmd_str = " ".join(args)
    return full_cmds

#############################################
####################Find#####################
#############################################

def find(args):
    full_cmd = " ".join(args)
    #janit.println(full_cmd)
    if full_cmd == "biggest folders":
        yield('du -sm ./* 2>/dev/null | sort -n')
    elif full_cmd == "biggest files":
        yield('find ./ -type f -printf "%s\t%p\\n" 2>/dev/null | sort -n | tail -18')

def tab_find(*args):
    full_cmds = ['find biggest folders', 'find biggest files']
    return full_cmds

#############################################
####################Kill#####################
#############################################

def kill(args):
    full_cmd = " ".join(args)
    #janit.println(full_cmd)
    if full_cmd == "gui-application":
        janit.println("\nLeft-click the broken application, Right-click to cancel")
        yield('xkill')
    #TODO
    #by process name (sort cpu%)
    #by pid

def tab_kill(*args):
    return ['kill gui-application']
