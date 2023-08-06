#this will run and yield the output of bash and will display its output in the top blue box

def get_slaves():
    raw = get_slaves_raw()
    return_data = []
    for less_raw in raw.strip('/').split('/'):
        return_data.append("/dev/pts/" + str(less_raw))
    return return_data


def get_slaves_raw():
    os.lseek(slave_fd, 0, os.SEEK_SET)
    buf = mmap.mmap(slave_fd, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_READ)
    msg = str(buf.readline())
    msg = ':'.join(msg.split(':')[:-1]).split("'")[-1]
    return(msg)


def add_slave(pid):
    global slaves
    offset = get_slaves_raw()
    offset = len(offset)
    os.lseek(slave_fd, offset, os.SEEK_SET)
    buf = mmap.mmap(slave_fd, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_WRITE)
    TTY = subprocess.check_output(['ps', 'hotty', str(pid)]).strip().decode()
    TTY = TTY.split("pts")[-1] + ":" # cut off pts and add a : for spacing
    #slaves.append(TTY)
    for index in range(offset, offset + len(TTY)):
        buf[index] = ord(TTY[index - offset])


def bash_attach(native_bash=True):
    global output_data
    global out_put_screen
    global bash_process_list
    global masters
    global slaves
    #run bash while piping it's ouput/err/in to new pts

    #init process list if needed
    if 'bash_process_list' not in list(globals().keys()):
        bash_process_list = []
    #attach to current screen
    my_screen = out_put_screen

    if native_bash:
        bash_cmd = "bash"
    else: #deprecated
        bash_cmd = "bash"

    #Thanks! https://stackoverflow.com/a/52157066/5282272
    # fork this script such that a child process writes to a pty that is
    # controlled or "spied on" by the parent process

    (child_pid, new_master_handle) = pty.fork()
    masters.append(new_master_handle)
    # A new child process has been spawned and is continuing from here.
    # The original parent process is also continuing from here.
    # They have "forked".

    if child_pid == 0:
        debug("This is the child process fork, pid %s" % os.getpid())
        add_slave(os.getpid())
        bash_process_list.append(subprocess.run(bash_cmd))

    else:
        debug("This is the parent process fork, pid %s" % os.getpid())
        debug(get_slaves())

        while True:
            try:
                data = os.read(masters[my_screen], 1026)
            except Exception:
                #time.sleep(.2)
                continue
            yield data


#will Attach to current screen
def bash_screen_ref(**kwargs):
    global streams
    global screens
    global output_data
    global out_put_screen
    global input_focus
    global TTYReady
    global history_buffer
    global bash_buff_size

    #store current output screen
    debug("OPENING SCREEN WITH DISPLAY: " + str(out_put_screen))
    this_output_screen = out_put_screen
    output_index = 0
    for output_bit in bash_attach(**kwargs):

        if not RUNNING:
            debug("end bash")
            exit()
        #debug("output_bit: " + str(output_bit))

        #feed vt100 into pyte
        if this_output_screen != out_put_screen:
            streams[this_output_screen].feed(output_bit)
        else:
            VT = output_bit.decode('utf-8', errors='ignore')
            #update main terminal
            vt_write(VT)
            #write to slaves too, for clean history loading/switching.
            streams[this_output_screen].feed(output_bit)
        #read screen data
        tmp_data = screens[this_output_screen].buffer

        if tmp_data != "":
            output_data[this_output_screen] = tmp_data


def bash_run(cmd, ctl_term=False):
    cmd = cmd + "\n"
    if not ctl_term:
        try: #If tty are opened fast, this can crash
            os.write(masters[out_put_screen], cmd.encode())
        except Exception:
            time.sleep(.2) #wait for tty
            bash_run(cmd)
    else:
        os.write(masters[0], cmd.encode())

