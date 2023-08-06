import subprocess

def _service(args, action="disable"):
    if len(args) != 1 or args[0] == "":
        janit.debug(action + " OS", Level=3)
        return
    if args[0] in _get_machines() or action=="start" or action=="enable":
        systemctl_str = "systemctl " + action + " systemd-nspawn@"+ args[0] +".service"
        yield (systemctl_str)


def disable(args):
    return _service(args)

def enable(args):
    return _service(args, action="enable")

def start(args):
    return _service(args, action="start")

def stop(args):
    return _service(args, action="stop")

def OS(args):
    if len(args) != 1 or args[0] == "":
        janit.debug("No OS specified", Level=3)
        return
    #janit.debug(str(args), Level=3)
    if args[0] in _get_machines():
        user = janit.os.getlogin()
        janit.open_tty()
        janit.time.sleep(.2)
        print("Found " + args[0])
        yield ('...')
        yield ('machinectl shell ' + user + '@' + args[0] + " /bin/bash")
        return
    else:
        janit.debug("Cannot find '" + args[0] + "' Running machines:", Level=3)
        return (['machinectl list'])


#tab def must be lowercase
def tab_os(*args):
    full_ruturn = []
    for machine in _get_machines():
        full_ruturn.append("OS " + "KDKD" +machine)
    return full_ruturn

#same tabbing as tab_os
def tab_disable(*args):
    full_ruturn = []
    for machine in _get_machines():
        full_ruturn.append("disable " + machine)
    return full_ruturn

def tab_enable(*args):
    full_ruturn = []
    for machine in ['ubuntu','arch']:
        full_ruturn.append("enable " + machine)
    return full_ruturn

def tab_start(*args):
    full_ruturn = []
    for machine in ['ubuntu','arch']:
        full_ruturn.append("start " + machine)
    return full_ruturn

def tab_stop(*args):
    full_ruturn = []
    for machine in _get_machines():
        full_ruturn.append("stop " + machine)
    return full_ruturn



def _get_machines():
    std_out = subprocess.check_output(['machinectl', 'list'])
    #janit.debug("OUT='" + std_out + "'", Level=3)
    machines = []
    for line in str(std_out).split('\\n'):
        if "MACHINE CLASS" in line:
            continue
        if line == "":
            break
        #janit.debug(line, Level=3)
        machines.append(line.split(" ")[0])
    return machines
