#!/usr/bin/python3

#debug settings
debugging = False
critical_debug = True

#shit fix for black terms
#BLACKTERM = True
#white terms
BLACKTERM = False

#check if we are running over ssh
if 'SSH_CONNECTION' in os.environ.keys():
    #remove ssh flag (so we can add an auto start to .bashrc without looping in ssh)
    del os.environ['SSH_CONNECTION']

#Setup prompt
#TODO move to settings file
os.environ['PS1'] = "`tty | cut -d/ -f4`|\\u@\\h:\\w> "



###################Setup Global Vars#######################
#############Stuff####################
global output_start
global out_put_screen #used to ctrl which screen is active
global output_data #   only used to init new bash session
global rendered_data #init as well...
global masters #bash sessions input
global autocomplete
global menu_showing
global menu_filter
global object_of_attention
global menu_auto_comp
global MENU_CAN_RUN
global screens
global streams
global input_focus
global RUNNING
global imported_cmd
global lower_imported_cmd
global TTYReady
global force_while_loop
global c
global raw_c
global input_index
global can_complete
global prompt_index
global command_text
global max_input_size
global inputline
global input_offset
global do_resize
global term_size
global old_term_size
global open_windows
global bash_threads
global render_where
global history_buffer
global bash_buff_size
global last_split
global last_resize

RUNNING = True

bash_buff_size = 400
history_buffer = [[]]
CLICK_MAP = []
#Types atm:
#menu: loads .desktop apps
#serial: parse commands for serial switch interface
role = ["menu", "serial"]
WM = True
init_cmd = ""
key_layout = 'Linux'
imported_serial = {}
imported_ssh = {}

#imported_cmd = []
input_index = (0,0)

#track last resize
last_resize = time.time()
DORESIZE = False
#used to hold name of open windows
open_windows = []

#prompt settings
prompt_txt = "janit> "

#vars used to hold pyte objs
streams = []
screens = []
drawing = False

#var used for data display
output_data = [[]]
rendered_data = [[]]
can_complete = []


out_put_screen = 0
input_data = []

menu_auto_comp = []

#prompt/color settings
#
# 0:white or black(default term color), 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white
# black is white... I don't care why.


colors = {'red':1, 'green':2, 'yellow':3, 'blue':4, 'magenta':5, 'cyan':6, 'white':7, 'default':0}

color_map = []
default_color_map = []


#bash settings
run_dir = "/tmp/"
#(child_pid, new_master_handle) = pty.fork()
#masters = [new_master_handle]
masters = []
slaves = []
slave_fd, tmpfile = tempfile.mkstemp()
os.write(slave_fd, b'\x00' * mmap.PAGESIZE)
os.lseek(slave_fd, 0, os.SEEK_SET)
#master, slave = pty.openpty()
#masters = [master]
#masters = [slave]
TTYReady = False

#modules for command 0_o
init_modules = []

desktop_applications = {}
application_categories = {}
application_by_type = {}

menu_showing = False
#default menu: syntax {'MENUENTRY': ['categorie1', 'categorie2']}
main_menu_categories = [{'Utility': ['Accessibility', 'System']},
                      {'Development': ['Development']},
                      {'Games': ['Games', 'Game']},
                      {'Graphics': ['Graphics']},
                      {'Internet': ['Network']},
                      {'Multimedia': ['_audio_video']},
                      {'Office': ['Office']},
                      {'System': ['System', 'Settings']},
                      {'Other': ['Core', 'Settings', 'Screensaver']}]

#(just a list of the keys from main_menu_categories) more readable... :/
main_menu_categories_name_arr = []



for categorie in main_menu_categories:
    main_menu_categories_name_arr.append(list(categorie.keys())[0])

#init filter
menu_filter = ["Applications", ""]

#setup a list of categories based on the above
main_menu_cat_list  = []
for tmp in main_menu_categories:
    key_name = list(tmp.keys())[0]
    main_menu_cat_list.append(key_name)

#create var that will hold tab options


#this will hold all autocomplete data (loaded in init_con)
autocomplete_info = []

#this will hold autocomplete atm suggestions
autocomplete = []


#keep track of screen threading
screen_thread = ""
call_back_display = False
display_callback_args = {}

#what we are running command for
object_of_attention = []


prompt_index = 0

#other global things...
script_path = os.path.dirname(os.path.realpath(__file__))



#used for displayupdate
skip_lines = []

last_split = "1" #keep track of the last screen split


#set to true when screen need resized
do_resize = False
#used to find resize
old_term_size = ()




#####################Define function used by console##############################

#Level 1 is info (Sent to a log file only if debug in True)
#Level 2 will go into a log file
#Level 3 will print in janit and is user visible
def debug(error, new_line='\n', Level=1):
    global debugging
    global critical_debug
    global out_put_screen
    crit_bug = Level > 1
    crit_bug = crit_bug and critical_debug


    if Level >= 3:
        try:
            slaves = get_slaves()
            plus_color = '\033[0;31m' + str(error) + '\n\033[0m'
            tty = open(slaves[out_put_screen], "wb+", buffering=0)
            tty.write(plus_color.encode())
        except Exception:
            crit_bug = True
        #os.write(masters[out_put_screen], plus_color.encode())

    if debugging or crit_bug:
        debug_log = open('/tmp/janit_debug.txt', 'a+')
        debug_log.write(str(error) + new_line)
        debug_log.close()

#screen is the tty number to show the msg on. current is the active tty

def println(msg, std='out', append=False, screen='current'):
    try:
        slaves = get_slaves()
    except Exception as E:
        debug("Could not pull tty for print", Level=2)
    try:
        plus_color = '\033[0;32m' + str(msg) + '\n\033[0m'

        #debug(f"Master: {len(masters)}\nSlaves: {len(slaves)}", Level=2)


        if screen=='current':
            tty = open(slaves[out_put_screen], "wb+", buffering=0)
            #os.write(masters[out_put_screen], plus_color.encode())
        elif isinstance(screen, int) and screen <= len(masters):
            tty = open(slaves[screen], "wb+", buffering=0)
            #os.write(masters[screen], plus_color.encode())
        else:
            tty = open(slaves[out_put_screen], "wb+", buffering=0)
            #os.write(masters[out_put_screen], plus_color.encode())
        tty.write(plus_color.encode())
    except Exception as E:
        debug("Error printing: " + str(E), Level=2)
        #raise(E)


#ctrl + z does not show up as a key in janit. We have to handle this out of the main loop.
def ctrl_zhandler(signum, frame):
    global raw_c
    global c
    global force_while_loop
    global input_focus

    if input_focus == "bash":
        raw_c = b'\032'
        os.write(masters[out_put_screen], raw_c)


signal.signal(signal.SIGTSTP, ctrl_zhandler)


def resize_trigger(signum, frame):
    global DORESIZE
    DORESIZE = True
    #TODO resize virt tv terms
    #vt_clear()


signal.signal(signal.SIGWINCH, resize_trigger)

#resize all ttys #TODO move all resize code out of janit.py
def resize_handler():
    global force_while_loop
    global c
    global TTYReady
    global term_size
    global screens
    global command_text
    global do_resize
    global masters
    global max_input_size
    global inputline
    global output_start
    global out_put_screen
    global last_split
    global render_where
    global last_resize
    global RUNNING
    global DORESIZE
    global max_input_size
    global inputline
    global output_start

    while RUNNING:
        time.sleep(.7)
        if DORESIZE:
            DORESIZE = False
            #force_while_loop = True
            #c = "KEY_RESIZE"

            #check we don't spam this call
            if time.time() - last_resize < 0.1:
                debug("Resized too fast", Level=2)
                debug(time.time() - last_resize, Level=2)
                last_resize = time.time()
                return
            else:
                debug(time.time() - last_resize, Level=2)
                last_resize = time.time()

            try:
                TTYReady = False

                term_size = vt_size()
                debug("Resizing to: " + str(term_size), Level=2)

                if str(out_put_screen) in last_split:
                    #resplit screen after resize
                    split(last_split)
                    #janit.debug("Split: " + janit.last_split, Level=2)
                else:
                    split(str(out_put_screen))
                    #janit.debug("Split: " + str(janit.out_put_screen), Level=2)
                    #render_where[0][
                #janit.debug("Data0: " + str(janit.render_where), Level=2)



                max_input_size = term_size[1] - 5
                inputline = term_size[0] - 1
                output_start = term_size[0] - 4
                debug(render_where, Level=2)
                #loop all screen and resize:
                #janit.input_focus = "janit"
                #vt_clear()
                debug("Done resizing ", Level=2)
                update_display(rerender = True)
                if input_focus == "janit":
                    update_prompt()
            except Exception as E:
                debug("Cannot resize", Level=2)
                raise(E)

#signal.signal(signal.SIGWINCH, resize_handler)
#setup resize Handler
resizer = threading.Thread(target=resize_handler, args=[])
resizer.start()

def mkconfig():
    config_folder = os.path.expanduser("~/.janit/")

    #make folder ~/.janit
    if not os.path.isdir(config_folder):
        os.makedirs(config_folder)

    #write default config:
    config = "init_cmd=for i in `seq 1 $(tput lines)`; do echo ''; done;echo -e 'Welcome to Janit'; echo 'Ctrl + Right |New shell'; echo 'Ctrl + Left  |Old shells'; echo 'Ctrl + Down  |Enter menu'; echo 'Ctrl + Up    |Enter shell';tty;echo;echo\nrole=menu\nwm=True\n"
    with open(config_folder+"janit.cfg", "w+") as new_config_file:
        new_config_file.write(config)

    #write passwd file for user switching
    with open(config_folder+".shit", "w+") as newpasswd:
        #write 30 random lowercase/digits to newpasswd
        newpasswd.write(''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(30)))
        #chmod 600
        os.chmod(config_folder+".shit", 0o600)



def load_user_config(failed=False):

    #Shit we will load into
    global role
    global init_cmd
    global key_layout
    global imported_serial
    global imported_ssh
    global WM


    #get full path
    config_path = os.path.expanduser("~/.janit/janit.cfg")
    #check if we have a config file for this user
    if os.path.exists(config_path):
        config_lines = open(config_path).readlines()
        #load config
        for config_line in config_lines:
            #load init_cmd from config
            if config_line.startswith("init_cmd"):
                init_cmd = config_line.split("=")[-1].strip()

            #load role from config
            elif config_line.startswith("role"):
                role = config_line.split("=")[-1].strip()

            #load if we are doing the Window managmnet
            elif config_line.startswith("wm"):
                if "False" == config_line.split("=")[-1].strip():
                    WM=False
                else:
                    WM=True
                debug("WINMAN: " + str(WM), Level=2)
            #load Key layout
            elif config_line.startswith("windows_controls=True"):
                key_layout = "Windows"

            #load serial connections
            #serial:Switch name:1.1.1:115200
            if config_line.startswith("serial"):
                split_serial_config = config_line.split(":")
                readable_name = split_serial_config[1]
                port = split_serial_config[2]
                speed = split_serial_config[3]
                imported_serial[readable_name] = [port, speed]

            #load SSH connections
            #ssh:<readable name>:user:IP:Port
            #ssh:testing:root:192.168.1.1:55
            if config_line.startswith("ssh"):
                split_ssh_config = config_line.strip().split(":")
                readable_name = split_ssh_config[1]
                user = split_ssh_config[2]
                IP = split_ssh_config[3]
                #check if we have a port setup
                if len(split_ssh_config) == 5:
                    port = split_ssh_config[4]
                else:
                    port = "22"

                imported_ssh[readable_name] = [user,IP,port]

            debug(config_line)
    else:

        #No config file... Let's make one
        mkconfig()
        #only try to make a config file one time.
        if failed:
            #print("Crit Error loading config")
            debug("Crit Error loading config")
            RUNNING = False

        load_user_config(failed=True)


def init_con():
    global init_modules

    global color_map
    global default_color_map
    global prompt_color
    global complete_color
    global output_color
    global error_color
    global menu_color
    global highlight_color
    global top_color
    global script_path
    global render_where

    os.system("stty -icanon -echo")
    #setup
    term_size = vt_size()
    #[[screen1, start_line, startcol, num_lines, num_col],
    #[screen2, start_line, startcol, num_lines, num_col]]

    #render_where = [[1,0,0,int((term_size[0]-2)/2),term_size[1]],
                   #[0,int((term_size[0]-2)/2),0,int((term_size[0]-2)/2),term_size[1]]]
    render_where = [[1,0,0,int(term_size[0]-2),term_size[1]]]
    debug(render_where, Level=2)


def find_alike(file_path, direction='next'):
    """
    recursively walk directory to specified depth
    :param path: (str) the base path to start walking from
    :param depth: (None or int) max. recursive depth, None = no limit
    :yields: (str) filename, including path
    """

    #find type:
    if "." in file_path:
        file_type = file_path.split(".")[-1]
    else:
        file_type = "unknown"
    debug(file_type)

    depth = 2
    path = os.path.dirname(file_path)
    top_pathlen = len(path) + len(os.path.sep)
    found_files = []
    for dirpath, dirnames, filenames in os.walk(path):
        dirlevel = dirpath[top_pathlen:].count(os.path.sep)
        if depth and dirlevel >= depth:
            dirnames[:] = []
        else:
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                #only match file with the same .whatever
                if full_path.endswith(file_type):
                    found_files.append(full_path)
    #sort files
    found_files = sorted(found_files, key=str.lower)
    #find current index
    current_index = found_files.index(file_path)
    if direction == "next":
        #check if we have a next option...
        if len(found_files) > current_index + 1:
            return found_files[current_index + 1]
        else:
            #no next option... just return the input
            return file_path
    if direction == "back":
        #check if we have a next option...
        if 0 <= current_index - 1:
            return found_files[current_index - 1]
        else:
            #no next option... just return the input
            return file_path

    #failed
    return file_path

#returns a list of autocomplete that work

#returns files/folders of a path... returns false if path cannot be found
def find_files(path):
    options = []
    dir_name = os.path.dirname(path)
    end_part = path.split(dir_name)[-1].strip("/")
    if end_part != "":
        if os.path.isdir(path):
            dir_name = path + "/"

    if not dir_name.endswith("/"):
        dir_name += "/"

    #if root dirname is not really a folder
    if not os.path.isdir(dir_name):
        return ['wtf']


    #get list of what is in the root of the path
    for name in os.listdir(dir_name):
        path = os.path.join(dir_name, name)
        if os.path.isdir(path):
            name = name + "/"
        options.append(dir_name + name)

    return options

#read all runread ouput
def read_out():
    pass #TODO


def understand(some_cmd):
    global object_of_attention
    global menu_filter

    #no target yet.. lets check for some now and return
    if object_of_attention == []:
        #find if this is a file
        if some_cmd.startswith("/") or some_cmd.startswith("./") or some_cmd.startswith("~"):
            #looks like we have a path or file... lets check
            if os.path.isfile(some_cmd):
                tmp_type = get_mime_type(some_cmd)
                object_of_attention.append(['FILE', some_cmd])
                object_of_attention.append([tmp_type, some_cmd])
                menu_filter[0] = 'Type'
                menu_filter[1] = tmp_type
                #it's a file but what kind? TODO
            if os.path.isdir(some_cmd):
                object_of_attention.append(['DIR', some_cmd])
        #IPV4
        if re.match("^(\d{0,3})\.(\d{0,3})\.(\d{0,3})\.(\d{0,3})$", some_cmd):
            object_of_attention.append(['IP', some_cmd])
        #we set a new target or we did not.. we don't want to continue.
        debug(object_of_attention)
        update_display(interface_only=True,  rerender = True)
        return


def open_tty():
    #TODO we don't need this many global vars in here
    global out_put_screen #used to ctrl which screen is active
    global output_data #   only used to init new bash session
    global history_buffer# needs to be the size of the open screens
    global rendered_data #init as well...
    global masters #bash std out err
    global masters #bash sessions input
    global screens
    global streams
    global force_while_loop
    global c
    global raw_c
    global term_size
    global bash_threads


    out_put_screen = len(output_data)
    #init new bash session
    if len(output_data) <= out_put_screen:
        term_size = vt_size()
        debug("NEW bash session")
        output_data.append([])
        rendered_data.append([])
        history_buffer.append([])

        #kick off shell thread (the middle bash part)
        #master_new, slave_new = pty.openpty()
        #masters.append(master_new)
        #masters.append(slave_new)
        #open new virt term
        #new_screen = pyte.Screen(term_size[1], term_size[0] - 2)
        debug("Opening tty with size: " + str(term_size), Level=1)
        new_screen = pyte.screens.HistoryScreen(term_size[1],term_size[0] - 2,history=1000,ratio=0.5)
        #debug("80 : " + str(term_size[1]))
        screens.append(new_screen)
        streams.append(pyte.ByteStream(screens[-1]))

        streams[-1].escape["N"] = "next_page"
        streams[-1].escape["P"] = "prev_page"


        #resize tty:
        screens[-1].resize(term_size[0] - 2, term_size[1])
        screens[-1].set_margins(term_size[0] - 2, term_size[1])
        win_size = struct.pack("HHHH", term_size[0] - 2, term_size[1], 0, 0)
        fcntl.ioctl(masters[-1], termios.TIOCSWINSZ, win_size)

        #debug(dir(streams.copy), Level=3)
        #wait for tty to be ready
        #try to a connect over socket
        bash_threads.append(threading.Thread(target=bash_screen_ref))
        bash_threads[-1].start()
        vt_clear()
        vt_move(0,0)
        bash_run(init_cmd)
        c = 'KEY_RESIZE' #force resize
        force_while_loop = True
        #wait for term to move
        time.sleep(0.15)
        update_prompt()




def update_prompt():
    global term_size
    global input_focus
    global empty_line
    if input_focus == "bash":
        vt_save_cursor()
    
    empty_line = ""
    for jojo in range(0, term_size[1]):
        empty_line = empty_line + " "

    vt_move(abs(term_size[0] - 3), 0)
    vt_write(empty_line)
    vt_move(abs(term_size[0] - 3), 0)
    if object_of_attention != []:
        file_name = object_of_attention[-1][-1]
        vt_write('\r' + file_name.strip('/').split('/')[-1] + ":" + prompt_txt + command_text + " " + '\033[1D')
    else:
        vt_write('\r' + prompt_txt + command_text + " " + '\033[1D')
    
    if input_focus == "bash":
        vt_restore_cursor()
