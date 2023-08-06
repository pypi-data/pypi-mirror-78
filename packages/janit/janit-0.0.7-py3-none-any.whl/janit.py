#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Janit GPL3
#Copyright (C) 2019 David Hamner

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.


import sys
import os
import time

import Janit as janit
#setup path
main_dir = janit.os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, main_dir)



#########################################
#import CMDs#############################
#########################################
#sys.path.insert(0, main_dir + "/Janit/cmd/")
janit.init_modules = []
for file_with_cm_ds in janit.import_CMDs_to_run:
    #filter stuff
    if "__" in file_with_cm_ds:
        continue
    #lol... builds somthing like:  ['rename', 'tell'] by reading ./plugins/*
    janit.init_modules.append(file_with_cm_ds.split("/")[-1].split('.py')[0])

#TODO don't import files that use used names
for mod_file in janit.import_CMDs_to_run:
    #don't import ewmh_core if we don't need it
    #if not WM and mod == "ewmh_core":
    print(mod_file)
    script = ""
    for python_line in open(mod_file).readlines():
        script = script + python_line
        #don't add CORE file defs to auto complete
        if python_line.strip().startswith('def'):
            def_name = python_line.split('def')[-1].split('(')[0].strip()
            if def_name.startswith("_"):
                continue
            janit.imported_cmd.append(def_name)
    try:
        exec(script)
    except Exception as e:
        raise(e)

janit.lower_imported_cmd = [x.lower() for x in janit.imported_cmd]


#run command in a thread
def run_in_thread(function, args):
    #janit.debug("RUNNING function: " + str(globals()[function]([])), Level=1)
    try:
        for bash_out in globals()[function](args):
            #check if this is a cmd for us...
            if bash_out == "...":
                janit.input_focus = "bash"
                janit.force_while_loop =True
                continue
            #pipe bash commands to active bash session
            bash_out = bash_out + '\n'
            os.write(janit.masters[janit.out_put_screen], bash_out.encode())
            #debug("Piping: " + str(bash_out))
    except type_error as e:
        janit.debug("done in thread:" + str(e), Level=2)
        return #no bash commands yielded
    except Exception as e:
        janit.debug("Error running: " + function + "(" + str(args) + ") " + str(repr(e)), Level=3)
        return
    janit.debug("done in thread ", Level=2)
    return



def main():


    #########################################
    #Init stuff##############################
    #########################################
    #startup janit
    janit.load_user_config()
    janit.load_desktop_entrys()
    janit.init_con()

    #########################################
    #setup vars##############################
    #########################################
    
    janit.term_size = janit.vt_size()
    janit.old_term_size = janit.term_size
    try_autocomplete = False
    janit.MENU_CAN_RUN = ""
    #TODO update janit.max_input_size on resize...
    janit.max_input_size = janit.term_size[1] - 5
    janit.inputline = janit.term_size[0] - 1


    #setup output_space
    janit.output_start = janit.term_size[0] - 4


    #setup init V-term
    janit.debug(str((janit.term_size[1], janit.term_size[0] - 2)))


    new_screen = janit.pyte.screens.HistoryScreen(janit.term_size[1],janit.term_size[0] - 2,history=1000,ratio=0.5)

    janit.screens.append(new_screen)
    janit.streams.append(janit.pyte.ByteStream(janit.screens[-1]))


    #setup colors n stuff
    empty_line = ""
    for jojo in range(0, janit.term_size[1]):
        empty_line = empty_line + " "


    #set input focus (bash or janit)
    janit.input_focus = "janit"

    #mouse stuff
    mouse_event = []
    click_time = time.time()
    selection_mode = False

    #setup vars for main loop
    janit.command_text = ""
    display_text = ""

    command_sentence = ""


    janit.can_complete = []
    janit.input_offset = 0
    level = 1
    janit.force_while_loop = True
    janit.c = ""
    janit.raw_c = ""
    first_run = True

    #kick off shell thread (the middle bash part)
    janit.bash_threads = []

    #for ubuntu use
    #janit.bash_threads.append(janit.threading._thread(target=janit.bash_screen_ref, kwargs={"native_bash": False, "OS": 'ubuntu'}))
    #for native OS
    janit.bash_threads.append(janit.threading.Thread(target=janit.bash_screen_ref))
    janit.bash_threads[-1].start()

    janit.debug("INIT: " + janit.init_cmd, Level=2)
    #test the bash shit..
    janit.bash_run(janit.init_cmd)

    #wait for tty to be ready and run cmd

    time.sleep(.02)

    #done setting shit up. This is the main loop
    while janit.RUNNING:
        try:
            janit.debug('tick')

            # get keyboard input, returns -1 if none available (janit.force_while_loop set to true will let you set janit.c manually)
            if not janit.force_while_loop:
                try:
                    if not janit.TTYReady:
                        janit.TTYReady = True
                    janit.raw_c = sys.stdin.buffer.peek()
                    janit.c = sys.stdin.read(1)
                except Exception:
                    janit.debug("Error reading from term")
                    #try again
                    continue
            else:
                janit.force_while_loop = False
                janit.raw_c = ""

            try_autocomplete = False #only set to try when tab is pressed

            ####################remap keys... ################
            #Mostly cuz I had to move away from janit.curses (Cannot get keys on a diff thread than the one that draws)


            if len(janit.c) < len(janit.raw_c) and not first_run:
                #clear read buffer
                sys.stdin.read(len(janit.raw_c) - len(janit.c))

                #look for shit
                #          Ctrl + Right
                if janit.raw_c == b'\x1b[1;5C':
                    janit.c = "kRIT5"

                #            Ctrl + Left
                elif janit.raw_c == b'\x1b[1;5D':
                    janit.c = "kLFT5"

                #            Ctrl + up
                elif janit.raw_c == b'\x1b[1;5A':
                    janit.c = "kUP5"

                #            Ctrl + Down
                elif janit.raw_c == b'\x1b[1;5B':
                    janit.c = "kDN5"

                #            right
                elif janit.raw_c == b'\x1b[C':
                    janit.c = "KEY_RIGHT"

                #            left
                elif janit.raw_c == b'\x1b[D':
                    janit.c = "KEY_LEFT"

                #            up
                elif janit.raw_c == b'\x1b[A':
                    janit.c = "KEY_UP"

                #            down
                elif janit.raw_c == b'\x1b[B':
                    janit.c = "KEY_DOWN"

                #            Delete
                elif janit.raw_c == b'\x1b[3~':
                    janit.c = "KEY_DC"

                #            Shift + Tab
                elif janit.raw_c == b'\x1b[Z':
                    janit.c = "KEY_BTAB"

                #            Alt + .
                elif janit.raw_c == b'\x1b.':
                    janit.c = "alt_dot"

                #            Ctrl + Left
                elif janit.raw_c == b'\x1b[1;5D':
                    janit.c = "kLFT5"

                #            Ctrl + Left
                elif janit.raw_c == b'\x1b[1;5D':
                    janit.c = "kLFT5"
                elif janit.raw_c.startswith(b'\x1b[<0;'):
                    strsplit = str(janit.raw_c).split(';')
                    x = strsplit[-2]
                    y = strsplit[-1]
                    janit.click(x=x, y=y)
                    janit.c = ""
                    janit.raw_c = ""
                elif janit.raw_c.startswith(b'\x1b[<2'):
                    strsplit = str(janit.raw_c).split(';')
                    x = strsplit[-2]
                    y = strsplit[-1]
                    janit.click(x=x, y=y, right=True)
                    janit.c = ""
                    janit.raw_c = ""
                #History page up/down
                elif janit.raw_c.startswith(b'\x1b[5~'):
                    janit.screens[janit.out_put_screen].prev_page()
                    #janit.debug(str(janit.screens[janit.out_put_screen].history.position), Level=2)
                    janit.c = ""
                    janit.raw_c = ""
                    #janit.update_display(rerender = True)
                elif janit.raw_c.startswith(b'\x1b[6~'):
                    janit.screens[janit.out_put_screen].next_page()
                    #janit.debug(str(janit.screens[janit.out_put_screen].history.position), Level=2)
                    janit.c = ""
                    janit.raw_c = ""
                    #janit.update_display(rerender = True)
                else:
                    janit.c = janit.raw_c.decode("utf8")
                    #janit.debug("Unhandled KEY: "+ str(janit.raw_c), Level=2) #TODO don't let this happen
            else:
                #the only esc key that is one char long is... esc... :)
                if janit.c == "\x1b":
                    janit.c = "KEY_ESC"

            ############################################################################################################
            #####KEYs are setup, janit.raw_c is input data, janit.c is a char or a readable name like KEY_FISH###########
            ############################################################################################################
            #Resize! Not here... moved to core.py
            #Resize!
            if janit.do_resize:
                janit.do_resize = False
                janit.command_text = ""
                #janit.input_focus = "janit"
                janit.c = ""
                #janit.update_display()
                continue
            
            #done processing arrows
            if janit.input_focus == "janit" and (janit.c == "KEY_LEFT" or janit.c == "KEY_RIGHT" or janit.c == "KEY_UP" or janit.c == "KEY_DOWN"):
                janit.c = ""
            
            #change input focus
            janit.debug("INFO: RUN WITH c='" + janit.c + "'")
            if janit.c == 'kDN5':
                janit.input_focus = "janit"
                janit.vt_write('\n\n\n')
                janit.update_prompt()
                #force janit to update
                janit.force_while_loop = True
                janit.c = ""
                continue
            elif janit.c == 'kUP5':
                janit.input_focus = "bash"
                janit.os.write(janit.masters[janit.out_put_screen], " \n".encode())
                janit.menu_showing = False
                #force bash up refresh
                janit.os.write(janit.masters[janit.out_put_screen], " \b".encode())
                continue
            if janit.c == "KEY_BTAB":
                janit.c = ""
                if janit.key_layout == "Windows":
                    #toggle janit.input_focus
                    if janit.input_focus == "bash":
                        janit.input_focus = "janit"
                        janit.vt_write('\n')
                        janit.update_prompt()
                    else:
                        janit.input_focus = "bash"
                        janit.vt_write('\n')
                        janit.menu_showing = False
                        janit.os.write(janit.masters[janit.out_put_screen], " \n".encode())
                        janit.os.write(janit.masters[janit.out_put_screen], " \b".encode())
                    janit.force_while_loop = True
                    continue

            #kRIT5 = ctrl + right
            #switch input janit.screens
            switched = False
            repaint_needed = False
            if janit.c == 'kRIT5' or (janit.c == "KEY_RIGHT" and janit.key_layout == "Windows" and janit.input_focus == "janit") or first_run:
                first_run = False
                janit.c = ""
                janit.TTYReady = False
                janit.out_put_screen = janit.out_put_screen + 1
                switched = True
                repaint_needed = True
                #janit.input_focus = "janit"

                #TODO rename out_put_screen to in_put_screen
                render_not_found = True
                for rendered in janit.render_where:
                    if rendered[0] == janit.out_put_screen:
                        render_not_found = False
                #New screen not being displayed
                if render_not_found:
                    janit.render_where[0][0] = janit.out_put_screen

            if janit.c == 'kLFT5' or (janit.c == "KEY_LEFT" and janit.key_layout == "Windows" and janit.input_focus == "janit"):
                janit.c = ""
                janit.TTYReady = False
                #janit.input_focus = "bash"
                
                if janit.out_put_screen > 0:
                    janit.out_put_screen = janit.out_put_screen - 1
                    if len(janit.render_where) == 1:
                        janit.last_split = str(janit.out_put_screen)
                    switched = True
                    repaint_needed = True
                    render_not_found = True
                    for rendered in janit.render_where:
                        if rendered[0] == janit.out_put_screen:
                            render_not_found = False
                    #New screen not being displayed
                    if render_not_found:
                        janit.render_where[0][0] = janit.out_put_screen


            if len(janit.output_data) <= janit.out_put_screen:
                janit.open_tty()
                if janit.input_focus == "janit":
                    repaint_needed = False

            if switched:
                #force update
                janit.os.write(janit.masters[janit.out_put_screen], " \b".encode())
                janit.c = ""
                janit.force_while_loop = True
                if repaint_needed:
                    janit.repaint_display()
                continue

            janit.debug("screen: " + str(janit.out_put_screen))

            #capture mouse input if we entered anything normal
            if selection_mode and len(janit.c) == 1:
                janit.curses.mousemask(janit.curses.ALL_MOUSE_EVENTS)
                janit.debug("Set mouse_mode to click interface")

            #handle mouse_event
            if janit.c == "" and mouse_event != []:
                pass#TODO
                #CLICK_MAP = [[(1,2),(1,4), 'toggle_menu']]
                #check if click is in range
                #read tag and do something.


            ###################################################################
            ##############bash mode.. pipe shit to bash########################
            ###################################################################
            if janit.input_focus == "bash":

                #esc blocks next key input BUG
                #if janit.raw_c == "\x1b":
                if janit.c == "CTRL_C":
                    janit.raw_c = b'\003'
                if janit.c == "CTRL_Z":
                    janit.raw_c = b'\003'

                if type(janit.raw_c) == bytes:
                    janit.os.write(janit.masters[janit.out_put_screen], janit.raw_c)
                elif type(janit.raw_c) == str:
                    janit.os.write(janit.masters[janit.out_put_screen], janit.raw_c.encode())
                else:
                    janit.debug("Cannot write to bash screen: " + str(type(janit.raw_c)), Level=2)

            ########################################################################
            ############################time for janit##############################
            ########################################################################
            if janit.input_focus == "janit" or janit.force_while_loop:
                #rewrite

                #Catch/handle ctrl + ]
                c_clean = str(janit.c.encode("utf8"))[2:-1]
                if c_clean == "\\x1d":
                    continue

                ##########################run command!! :) #############################
                if janit.c == '\n':
                    janit.vt_write('\n')
                    janit.menu_showing = False
                    #add new line to ouput if no text was entered
                    if janit.command_text.strip() == "":
                        janit.input_focus = "bash"
                        if janit.key_layout == "Linux":
                            janit.println("\nCtrl + ↓\n to swich back to menu")
                            pass
                            #janit.os.write(janit.slaves[janit.out_put_screen], "\nCtrl + ↓\n to swich back to menu".encode())
                            #janit.os.write(janit.masters[janit.out_put_screen], "\n".encode())
                        elif janit.key_layout == "Windows":
                            janit.println("\nShift + Tab\n to swich back to menu")
                            #janit.os.write(janit.slaves[janit.out_put_screen], "\nShift + Tab\n to swich back to menu".encode())
                            #janit.os.write(janit.masters[janit.out_put_screen], "\n".encode())
                        continue

                    janit.lower_cmd = janit.command_text.split(" ")[0].lower()
                    janit.entered_cmd = janit.command_text.split(" ")[0]
                    #check if we need to change the string case
                    if (janit.lower_cmd in janit.lower_imported_cmd) and not (janit.entered_cmd in janit.imported_cmd):
                        for cmd in janit.imported_cmd:
                            if janit.lower_cmd == cmd.lower():
                                janit.entered_cmd = cmd
                                break
                    janit.debug("CMD: " + janit.entered_cmd, Level=1)
                    if janit.entered_cmd in janit.imported_cmd:
                        imported_def = janit.entered_cmd
                        argz = janit.command_text.split(" ")[1:]
                        janit.debug("cmd_def: " + imported_def)
                        janit.debug("argz: " +str(argz))
                        janit.threading.Thread(target=run_in_thread, args=(imported_def,argz,)).start()
                        janit.debug("Started CMD: " + janit.entered_cmd)
                        janit.force_while_loop = True
                        #janit.update_display(rerender = True, interface_only=_true)
                        janit.c = ""

                    #handle display command
                    #EX: 1 2/3
                    test = janit.command_text.replace(' ','').replace('/','')
                    if test.isdigit():
                        #check we have all needed TTYs open
                        test2 = janit.command_text.replace(' ','~').replace('/','~')
                        #don't start with a split or end with one
                        test2 = test2.strip("~")
                        test2 = test2.split('~')

                        can_run = True
                        for tty_name in test2:
                            tty_name = int(tty_name)
                            if tty_name + 1 > len(janit.masters):
                                janit.debug("Display: '" + str(tty_name) + "' is not open", Level=3)
                                janit.command_text = ""
                                janit.update_prompt()
                                can_run = False
                        if can_run:
                            janit.split(janit.command_text.strip(' /'))
                            janit.last_split = janit.command_text.strip(' /')
                            janit.do_resize = True
                            janit.force_while_loop = True
                        continue
                    #This cannot be in this file! TODO: Move to ssh.py
                    #check if this is an ssh command
                    if janit.command_text in janit.tab_ssh():
                        janit.threading.Thread(target=run_in_thread, args=("ssh",janit.command_text,)).start()
                        #ssh(janit.command_text)

                    #check if we should exit
                    if janit.command_text == "exit":
                        #this will let the threads kill themselfs.
                        janit.RUNNING = False
                        for bash in janit.masters:
                            if janit.role != "serial":
                                janit.os.write(bash, "exit\n".encode())
                            else: #serial term
                                #quit picocom nice
                                janit.os.write(bash, "\x01".encode()) #ctrl + a
                                janit.time.sleep(.2)
                                janit.os.write(bash, "\x18".encode()) #ctrl + x
                                janit.time.sleep(.2)

                    #if we enter done... reset target shit
                    if janit.command_text == 'done':
                        janit.object_of_attention = []
                        janit.menu_filter = janit.menu_filter = ["Applications", ""]
                        #janit.update_display(rerender = True, interface_only=_true)

                    if janit.command_text == 'next' or janit.command_text == 'previous' or janit.command_text == 'back':

                        #find current target
                        current_file = ""
                        for obj in janit.object_of_attention:
                            if obj[0] == "FILE":
                                current_file = obj[1]


                        if current_file != "":
                            #get new file
                            if janit.command_text == 'previous' or janit.command_text == 'back':
                                new_file = find_alike(current_file, direction='back')
                            else:
                                new_file = find_alike(current_file)
                            janit.debug(new_file)

                        #update target
                        for obj in janit.object_of_attention:
                            if obj[1] == current_file:
                                obj[1] = new_file

                        #reset stuff and fouce update
                        janit.command_text = ""
                        janit.update_prompt()
                        #janit.update_display(interface_only=_true, rerender = True)
                        janit.c = ""
                        janit.force_while_loop = True
                        continue


                    if janit.MENU_CAN_RUN:
                        #parse options
                        #Hack support for %U and %u (treat like %f)
                        janit.MENU_CAN_RUN = janit.MENU_CAN_RUN.replace('%U', '%f')
                        janit.MENU_CAN_RUN = janit.MENU_CAN_RUN.replace('%u', '%f')
                        janit.MENU_CAN_RUN = janit.MENU_CAN_RUN.replace('%F', '%f')

                        #%f (single file)
                        if '%f' in janit.MENU_CAN_RUN:
                            for attention in janit.object_of_attention:
                                if attention[0] == "FILE":
                                    janit.MENU_CAN_RUN = janit.MENU_CAN_RUN.replace("%f", "'" + attention[1] + "'")

                        janit.debug("running Menu cmd " + janit.MENU_CAN_RUN)
                        #cut off unhandled % things
                        janit.MENU_CAN_RUN = janit.MENU_CAN_RUN.split("%")[0]
                        #print("# " + janit.MENU_CAN_RUN)
                        janit.bash_run(janit.MENU_CAN_RUN + ' &')
                    else:
                        janit.understand(janit.command_text)
                        janit.debug("command: " + janit.command_text.replace("\n", ""))
                    janit.command_text = ""
                    janit.c = ""
                    janit.update_prompt()


                #catch tab (for janit.autocomplete_info)
                if janit.c == "\t":
                    if janit.command_text == "":
                        #janit.update_display(toggle_menu=_true, interface_only=_true, rerender = True)
                        janit.menu_showing = not janit.menu_showing
                        janit.debug('menu toggled')
                    else:
                        try_autocomplete = True
                    janit.c = ''
                #handle backspace
                if janit.c == "\x7f":
                    #debug("BACKSPACE>>>>>>>>>>>")
                    deleted_key = ""
                    #don't delete the prompt :)
                    if janit.command_text == "":
                        continue
                    if janit.input_offset == 0:
                        deleted_key = janit.command_text[-1]
                        janit.command_text = janit.command_text[:-1]
                        janit.update_prompt()
                    else:
                        deleted_key = janit.command_text[janit.input_offset -1]
                        janit.command_text = janit.command_text[:janit.input_offset-1] + janit.command_text[janit.input_offset:]
                        janit.update_prompt()

                    #update dispaly on multi line input
                    if deleted_key == "\n":
                        pass
                        #we need to update the middle text as well..
                        #janit.update_display(interface_only=False)
                    #reset janit.c so we don't add it to the command
                    janit.c = ""

                #handle left
                if janit.c == "KEY_LEFT":
                    #don't let you left key off the screen :)
                    if abs(janit.input_offset) < len(janit.command_text) and janit.input_offset <= 0:
                        janit.input_offset = janit.input_offset - 1
                    janit.c = ""

                #handle key right
                if janit.c == "KEY_RIGHT":
                    #only alow moving right if we have already moved left :)
                    if janit.input_offset < 0:
                        janit.input_offset = janit.input_offset + 1
                    janit.c = ""

                if janit.c == "KEY_ESC":
                    janit.c = ""
                    janit.object_of_attention = []
                    janit.menu_filter = janit.menu_filter = ["Applications", ""]
                #find index to write this to the screen:
                janit.prompt_index = len(janit.prompt_txt)

                #add char to janit.command_text
                if janit.input_offset == 0:
                    janit.command_text = janit.command_text + janit.c
                    janit.update_prompt()
                    #dispaly char
                    #janit.vt_write(janit.c)
                else:
                    if janit.c != "":
                        janit.command_text = janit.command_text[:janit.input_offset] + janit.c + janit.command_text[janit.input_offset:]
                        janit.update_prompt()


                #rename ~ to real path
                if janit.command_text == "~":
                    janit.command_text = janit.os.path.expanduser("~") + "/"
                    janit.update_prompt()

                if janit.command_text == "./":
                    janit.command_text = janit.os.getcwd() + "/"
                    janit.update_prompt()




                #command text is half setup...

                #find what to janit.autocomplete
                janit.autocomplete = []

                #if no target yet
                if len(janit.object_of_attention) == 0:
                    if janit.command_text.startswith("/") or janit.command_text.startswith("./") or janit.command_text.startswith("~"):
                        #lets janit.autocomplete a file Yo
                        janit.autocomplete = janit.find_files(janit.command_text)
                #find autocomple_grids #TODO this looks old and unused...

                #find janit.autocomplete options
                #reset stuff
                janit.can_complete = []


                #find word we are entering atm
                #for files just autocomp all of janit.command_text
                if janit.command_text.startswith("/"):
                    last_word = janit.command_text
                #for other commands... strip off categories and autocomp what is left.
                else:
                    last_word = janit.command_text
                    for cat in janit.main_menu_categories_name_arr:
                        if last_word.startswith(cat):
                            last_word = last_word[len(cat)+1:]
                            break

                janit.debug("last_word: " + last_word)

                #call external janit.autocomplete
                tmp_cmd = janit.command_text.split(" ")[0].strip()
                tmp_args = " ".join(janit.command_text.split(" ")[1:])
                #debug(str(tmp_args), Level=2)
                if len(janit.command_text.split(" ")) > 1 and tmp_cmd.lower() in janit.lower_imported_cmd:
                    #check if we have a tab function
                    might_have = "tab_" + tmp_cmd.lower()
                    if might_have in janit.imported_cmd:

                        ###Add try
                        try:
                            #janit.debug(str("tab_test" in str(globals())), Level=3)
                            tab_data = ""
                            tab_data = globals()[might_have](tmp_args)
                        except Exception as e:
                            janit.debug("Error running : " + str(globals().keys()) + "(" + str(tmp_args) + ") " + str(repr(e)), Level=3)
                            raise(e)
                            tab_data = ""
                        #debug(str(tab_data), Level=3)
                        #debug("README: " + str(tab_data), Level=2)
                        if isinstance(tab_data, str):
                            janit.autocomplete = janit.autocomplete + [tab_data]
                        elif isinstance(tab_data, list):
                            janit.autocomplete = janit.autocomplete + tab_data


                ####################################################################
                ####################Setup what we can auto_comp######################
                ####################################################################
                janit.autocomplete = janit.autocomplete + janit.menu_auto_comp
 
                #add categories/Desktop Entrys to auto complete
                janit.autocomplete = janit.autocomplete + janit.main_menu_cat_list
                janit.autocomplete = janit.autocomplete + list(janit.desktop_applications.keys())

                #add janit.imported_cmd to auto complete
                janit.autocomplete = janit.autocomplete + janit.imported_cmd
                
                janit.autocomplete.append("fishfood")


                #don't care about case
                all_lower = [x.lower() for x in janit.autocomplete]
                #loop what we can janit.autocomplete and filter by janit.command_text (janit.autocomplete -> janit.can_complete)
                janit.can_complete = []
                for possibility_index in range(0, len(all_lower)):
                    if all_lower[possibility_index].startswith(last_word.lower()) and last_word != "":
                        #janit.println("tst")
                        this_thing = [janit.prompt_index + len(janit.command_text) - len(last_word), janit.autocomplete[possibility_index]]
                        if this_thing not in janit.can_complete:
                            janit.can_complete.append(this_thing)
                    ####needs cleaned
                    if command_sentence != "":
                        if all_lower[possibility_index].startswith(last_word.lower()):
                            janit.can_complete.append([janit.prompt_index + len(janit.command_text) - len(last_word), janit.autocomplete[possibility_index]])
                        else:
                            janit.can_complete.append([janit.prompt_index + len(janit.command_text + " "), janit.autocomplete[possibility_index]])
                #debug("janit.can_complete " +  str(janit.can_complete),Level=3)



                ##READ janit.can_complete and append to command Text
                #try a part auto_complete
                #debug("_the_bug: " + str(try_autocomplete) + " " + str(len(janit.can_complete)) ,Level=3)
                janit.command_text_lower = janit.command_text.lower()

                #setup try_complete with chars in common
                try_complete = []
                if try_autocomplete and len(janit.can_complete) >= 1:
                    needs_added = ""
                    #if we have more than one, find common chars
                    if len(janit.can_complete) > 1:
                        common = ""
                        test_text = janit.can_complete[0][1]
                        found_difference = False
                        for tmp_index in range(0, len(test_text)):
                            #debug("index: "+ str(tmp_index), Level=3)
                            for test_item in janit.can_complete:
                                #check size:
                                if len(test_item[1]) <= tmp_index:
                                    found_difference = True
                                    break
                                #check char
                                if test_item[1][tmp_index] != test_text[tmp_index]:
                                    found_difference = True
                                    break
                            if found_difference:
                                break
                            common = common + test_text[tmp_index]
                            #overwite janit.can_complete with common text
                            try_complete = [[janit.can_complete[0][0], common]]
                            #debug("less Fuck",Level=3)
                        if common == "":
                            for commands_to_print in janit.can_complete:
                                ws = " " * commands_to_print[0]
                                janit.vt_write('\n' + ws + commands_to_print[1])
                            janit.vt_write("\n\n\n")
                            janit.update_prompt()
                    else:
                        try_complete = janit.can_complete

                    found_to_complete = ""
                    if try_complete != []:
                        for char in try_complete[0][1].split(janit.command_text_lower)[-1]:
                            testing_for = needs_added.lower() + char.lower()
                            for complete_option in try_complete:
                                this_options_text = complete_option[1]
                                #this_options_text = this_options_text.split(janit.command_text)[-1]
                                this_options_text = this_options_text[len(janit.command_text):]
                                #debug("if: " + this_options_text + " startswith " + testing_for, Level=2)
                                if this_options_text.lower().startswith(testing_for):
                                    #needs_added = needs_added + char
                                    found_to_complete = complete_option[1]
                                    #debug("needs_added: " + needs_added, Level=2)
                                else:
                                    break

                        if found_to_complete != "":
                            janit.command_text = found_to_complete
                            needs_added = ""
                            janit.update_prompt()
                        elif len(janit.can_complete) >= 2:
                            #print what can be completed
                            for tab_thing in janit.can_complete:
                                #create white space:
                                ws = " " * tab_thing[0]
                                janit.vt_write('\n' + ws + tab_thing[1])
                            janit.vt_write('\n\n\n')
                            janit.update_prompt()
                            #janit.println(str(janit.can_complete))


                #janit.command_text is setup and tabbed...


                #update menu display
                #check if we have a valid categorie in buffer
                known_cat = ""
                found_commands = ""
                janit.desktop_applications
                janit.application_categories


                #check for a valid command
                #strip off categories
                tmp_text = janit.command_text
                for cat in janit.main_menu_categories_name_arr:
                    if tmp_text.startswith(cat):
                        tmp_text = tmp_text[len(cat)+1:]
                        break
                tmp_text = tmp_text.strip()
                #tmp_text has the categorie removed
                for app_name in list(janit.desktop_applications.keys()):
                    if tmp_text.lower() == app_name.lower():
                        found_commands = app_name


                #reset janit.MENU_CAN_RUN if it was set before
                if not found_commands and janit.MENU_CAN_RUN:
                    janit.MENU_CAN_RUN = ""


                #show menu filtered by a categorie
                lower_cat_list = [x.lower() for x in janit.main_menu_cat_list]
                if janit.command_text.split(" ")[0].strip().lower() in lower_cat_list and not found_commands:
                    janit.debug("Found menu categorie")
                    text_to_show = janit.command_text.split(" ")[0].strip().lower()
                    text_to_show = text_to_show[0].upper() + text_to_show[1:]
                    janit.menu_filter = ["Applications", text_to_show]
                    janit.menu_showing = True
                    #janit.update_display(interface_only=_true, rerender = True)
                #show menu for found command
                elif found_commands:
                    janit.menu_filter = ["Applications", found_commands]
                    janit.menu_showing = True
                    janit.MENU_CAN_RUN = janit.desktop_applications[found_commands]['Exec']
                    janit.debug("Found menu Command: " + janit.MENU_CAN_RUN)
                    #janit.update_display(interface_only=_true, rerender = True)
                #show apps menu
                elif janit.menu_showing and janit.menu_filter[0] == 'Applications':
                    janit.menu_filter = ["Applications", ""]
                    #janit.update_display(interface_only=_true, rerender = True)
                #hell if I know
                elif janit.menu_showing and janit.menu_filter[0] == 'Type':
                    pass
                    #janit.update_display(interface_only=_true, rerender = True)


                #janit.update_display()
                #stdscr.refresh()
        #hanle ctrl+c
        except (KeyboardInterrupt, Exception) as E:
            if isinstance(E, KeyboardInterrupt):
                janit.debug("ctrlc")
                janit.c = 'CTRL_C'
                janit.force_while_loop = True
            else:
                janit.debug("Main Loop Error: " + str(E), Level=3)
                raise(E)


    #MAIN LOOP OVER
    #cleanly exit
    for bash in janit.masters:
        #TODO, encode <ctrl-a>#<end>\nexit
        #for better bash exit
        janit.os.write(bash, "exit\n".encode())



#try to exit clean
try:
    main()
except base_exception as e:
    if janit.role == "serial":
        janit.os.system("pkill picocom")
    print(repr(e))
    janit.time.sleep(0.1)
    janit.os.system('stty sane')
    janit.vt_reset_all()
    raise(e)
    #janit.curses.endwin()

janit.os.system('stty sane')
janit.time.sleep(0.1)
janit.vt_reset_all()
#janit.curses.endwin()
sys.exit()
