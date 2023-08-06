#yield ... to enter shell after

def ssh(name):
    global imported_ssh
    if name in imported_ssh.keys():
        cmd = "ssh " + imported_ssh[name][0] + "@" + imported_ssh[name][1] + " -p " + imported_ssh[name][2]
        yield cmd
        yield "..."

def tab_ssh():
    can_return = []
    for name in imported_ssh.keys():
        can_return.append(name)
    return can_return
