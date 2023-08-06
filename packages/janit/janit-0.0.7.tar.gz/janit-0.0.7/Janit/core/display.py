def update_display(**kwargs):
    global screen_thread
    global call_back_display
    global display_callback_args

    if screen_thread == "":
        #kick of thread for the first time
        debug("New display_thread", Level=-1)
        screen_thread = threading.Thread(target=update_display_core, kwargs=(kwargs))
        screen_thread.start()
        return

    #check if we are still running a update
    if not screen_thread.isAlive():
        debug("New display_thread", Level=-1)
        screen_thread = threading.Thread(target=update_display_core, kwargs=(kwargs))
        screen_thread.start()
    else:
        #Tell current thread to call itself back
        if display_callback_args != {}:
            for key in kwargs:
                if key not in display_callback_args.keys():
                    display_callback_args[key] = kwargs[key]
        else:
            display_callback_args = kwargs #TODO add append new args as we go..
        call_back_display = True
        debug("Skipped update_display!... callback setup " + str(list(display_callback_args.keys())), Level=1)



def update_display_core(pop=False, rerender=False, std='out', interface_only=False, callback=False, show_auto_complete=True, age=0):
    pass
    return #TODO remove


#setting interface_only to true will only update the menu. Not the bash session.
#callback is only used if update_display is called before update is done
#rerender resets displayed buffer (forcing all chars to have changed)
#interface_only skips updating stdout

def repaint_display():
    global output_data
    global rendered_data
    global out_put_screen
    global output_start
    global input_data
    global menu_showing
    global menu_filter
    global object_of_attention
    global MENU_CAN_RUN
    global screens
    global TTYReady
    global input_index
    global can_complete
    global call_back_display
    global display_callback_args
    global skip_lines
    global bot_line
    global draw_level
    global menu_len_index
    global command_text
    global prompt_index
    global max_input_size
    global inputline
    global input_offset
    global do_resize
    global old_term_size
    global term_size
    global prompt_txt
    global role
    global open_windows
    global WM
    global CLICK_MAP
    global force_while_loop
    global c
    global render_where
    global non_active_tty
    global empty_line
    new_click_map = []


    debug("REPAINT CALLED: " + str(out_put_screen), Level=2)
    #vt_save_cursor()
    #vt_cursor_off()

    """
    #Don't refresh while resizing
    term_size = vt_size()
    if old_term_size != term_size:
        #vt_write(color_as_vt('white','white',False))
        ##vt_clear()
        #resizing, wait
        debug("Waiting for resize", Level=-1)
        time.sleep(.5)
        old_term_size = term_size
        update_display(**display_callback_args)
    old_term_size = term_size
    """

    #setup empty_line
    empty_line = ""
    for jojo in range(0, term_size[1]):
        empty_line = empty_line + " "

    #level of printing
    draw_level = 0
    max_level = term_size[0] - 5
    bot_line = output_start + 2

    #########################MAIN STDOUT
    printing = True
    text_index = -1
    #line_index = output_start
    screen_offset = output_start
    input_dataMaxIndex = output_start - len(input_data)

    screen_we_displayed = [[]]
    lines = term_size[0] - 2
    rows = term_size[1]

    #used for non active ttys
    last_used_inactive_color = "magenta"
    color_order = ['blue','red','green','magenta']
    tmp_color = last_used_inactive_color
    
    ##clear screen
    #vt_clear()
    #####################################################
    ############### Print Bash Stuff ####################
    #####################################################
    #renderwhere example:
    #[[screen1, start_line, startcol, num_lines, num_col],
    #[screen2, start_line, startcol, num_lines, num_col]]
    vt_lines = [''] * term_size[0]
    for part in render_where:
        debug("REPAINT CALLED2: " + str(out_put_screen), Level=2)

        active = part[0] == out_put_screen
        debug("Render " + str(part) + " active=" + str(active), Level=1)

        try:
            #lol
            #debug(str(part[0]) + " " + str(len(output_data)), Level=2)
            if len(output_data) < int(part[0]) - 1:
                debug('TTYs not ready...', Level=2)
                TTYReady = False
                rerender = False
                drawing = False
                return
            if output_data[out_put_screen] != "":
                for l in range(part[1], part[1] + part[3]):
                    relative_line = l - part[1]
                    screen_we_displayed.append([])
                    if l+1 in skip_lines:
                        continue
                    use_blank_space = False
                    r=0
                    line_vt = ""
                    last_used_color = {}

                    for r in range(part[2], part[2] + part[4]):
                        relative_col = r - part[2]
                        if not use_blank_space:
                            char = output_data[part[0]][relative_line][relative_col].data
                            bg_color = output_data[part[0]][relative_line][relative_col].bg ##TODO support this.. curses color_pairs kinda suck
                            fg_color = output_data[part[0]][relative_line][relative_col].fg
                            bold = output_data[part[0]][relative_line][relative_col].bold
                        else:
                            char = " "
                            bg_color = "white" ##TODO support this.. curses color_pairs kinda suck
                            fg_color = "default"
                            bold = False

                        #swich colors if tty is not active
                        if not active:
                            #find next color to use
                            if color_order.index(last_used_inactive_color) + 1 >= len(color_order):
                                bg_color = color_order[0]
                            else:
                                bg_color = color_order[color_order.index(last_used_inactive_color) + 1]
                            #bg_color = "blue"
                            tmp_color = bg_color
                            fg_color = "white"

                        #build clean dispaly data
                        clean_dic = {}
                        #clean_dic['char'] = char
                        clean_dic['bg_color'] = bg_color
                        clean_dic['fg_color'] = fg_color
                        clean_dic['bold'] = bold

                        if not last_used_color == clean_dic:
                            vt_lines[l] = vt_lines[l] + color_as_vt(clean_dic['fg_color'],clean_dic['bg_color'],clean_dic['bold'])
                            last_used_color = clean_dic

                        vt_lines[l] = vt_lines[l] + char
                        line_vt = line_vt + char
                
                vt_clear()
                #vt_reset_all()
                vt_move(0,0)
                for line in vt_lines:
                    if line.strip() != "":
                        vt_write(line + "\n")
                cursor_pos = screens[out_put_screen].cursor
                vt_move(cursor_pos.y, cursor_pos.x)
                debug((cursor_pos.y, cursor_pos.x), Level=2)
                #for line_index in range(0, len(vt_lines)):
                    #vt_move(line_index + 1, 0)
                    #vt_write(vt_lines[line_index])
                    #debug(vt_lines[line_index], Level=2)

            else:
                debug("Skipping update", Level=2)
            last_used_inactive_color = tmp_color
        except Exception as e:
            debug("failed to update bashscreen\n" + str(e), Level=2)
            TTYReady = False
            drawing = False
            #callback
            #time.sleep(.1)
            call_back_display = False
            debug("Returning display callback", Level=-1)
            display_callback_args['callback'] = True
            display_callback_args['rerender'] = True
            #debug(display_callback_args, Level=2)
            debug("Retrying update...", Level=2)


            #update_display(locals())
            #raise(e)



    #move back and update
    #vt_cursor_on()
    #vt_restore_cursor()
    if input_focus == 'bash':
        #update cursor
        offset = [0,0]
        for screen_dat in render_where:
            if screen_dat[0] == out_put_screen:
                offset[0] = screen_dat[1]
                offset[1] = screen_dat[2]
        try:
            pass#vtMove(screens[out_put_screen].cursor.y + offset[0] + 1, screens[out_put_screen].cursor.x + offset[1])
        except Exception:
            debug("Critical Error updating cursor.", Level=2)
            #debug((screens[out_put_screen].cursor.y + 1, screens[out_put_screen].cursor.x), Level=2)
    else:
        try:
            #\033[<L>;<C>H
            pass#vtMove(*input_index)
        except Exception:
            pass


    #stdscr.refresh()
    drawing = False
    #check if we already have more data to update
    #sleep for 1frame





def split(split_str):
    #janit.render_where
    #your render_where is showing... lol
    #[[screen1, start_line, startcol, num_lines, num_col],
    #[screen2, start_line, startcol, num_lines, num_col]]
    #[[1,0,0,int((term_size[0]-2)/2),term_size[1]],
    #[0,int((term_size[0]-2)/2),0,int((term_size[0]-2)/2),term_size[1]]]

    #1 2/3 = split vertical 1 and 2 and horizontal with 3 on the bottom
    #space = split vertical
    #/ = split horizontal

    #reset last display data
    global render_where
    global screens
    global masters


    old_render = render_where
    debug("Old render_where: " + str(old_render), Level=1)
    render_where = []


    #in case we need to change term size
    global last_split
    last_split = split_str

    term_size = vt_size()

    lines,col = term_size[0]-2,term_size[1]

    #0 1/2 becomes [0,1,2]

    #positions = split_str.replace(' ','~').replace('/','~')
    #TTYs = positions.split('~')
    #positions = "~" + positions + "~"

    display_line = lines
    number_horiz = len(split_str.split("/"))
    horiz_size = int(lines/number_horiz)
    position = [0,0]
    for horiz_win in split_str.split("/"):
        #0 1
        number_virt = len(horiz_win.split(' '))
        virt_size = int(col/number_virt)
        #write position
        for tty in horiz_win.split(' '):
            #use tty and info
            data = [int(tty),position[0], position[1],horiz_size, virt_size]
            render_where.append(data)
            debug("Display info: "+ str(data), Level=0)
            position[1] = position[1] + virt_size

        #update position
        position[0] = position[0] + horiz_size
        position[1] = 0

    debug("Updated render_where: " + str(render_where), Level=1)

    #resize ttys
    for screen_data in render_where:
        if len(screens) - 1 < screen_data[0]:
            #TTY is not setup
            debug("SKIPPING ", Level=2)
            continue
        #janit.debug("Data: " + str(screen_data), Level=2)
        #size can never be negative
        screen_data[3] = abs(screen_data[3])
        screen_data[4] = abs(screen_data[4])
        debug("Resize Part: " + str((screen_data[3], screen_data[4])), Level=2)
        screens[screen_data[0]].resize(screen_data[3], screen_data[4])
        screens[screen_data[0]].set_margins(screen_data[3], screen_data[4])
        win_size = struct.pack("HHHH", screen_data[3], screen_data[4], 0, 0)
        fcntl.ioctl(masters[screen_data[0]], termios.TIOCSWINSZ, win_size)
        command_text = ""



def vt_clear():
    sys.stdout.write('\033[2J')
    sys.stdout.flush()

def vt_move(l,c):
    sys.stdout.write('\033[' + str(int(l) + 1) + ';' + str(int(c) + 1) + 'f')
    sys.stdout.flush()
#def vt_write(na):
    #debug("BAD VT CALL: " + str(na), Level=2)
def vt_write(vt100):
    try:
        sys.stdout.write(vt100)
        sys.stdout.flush()
    except Exception as E:
        debug("failed write VT\n" + str(E), Level=2)

def vt_size():
    tmp = os.popen('stty size', 'r').read().split()
    return [int(tmp[0]), int(tmp[1])]

def vt_save_cursor():
    vt_write('\033[s')

def vt_restore_cursor():
    vt_write('\033[u')

def vt_cursor_off():
    vt_write('\033[?25l')
    #os.system('setterm -cursor off')

def vt_cursor_on():
    vt_write('\033[?25h')
    #os.system('setterm -cursor on')

def vt_reset_all():
    vt_write('\033c')

def color_as_vt(fg,bg,bold):
    return_vt = ""
    if bold:
        return_vt = return_vt + '\033[1m'
    else:
        return_vt = return_vt + '\033[0m\033[27m'

    if fg == 'black':
        return_vt = return_vt +  '\033[30m'
    if fg == 'red':
        return_vt = return_vt +  '\033[31m'
    if fg == 'green':
        return_vt = return_vt +  '\033[32m'
    if fg == 'yellow':
        return_vt = return_vt +  '\033[33m'
    if fg == 'blue':
        return_vt = return_vt +  '\033[34m'
    if fg == 'magenta':
        return_vt = return_vt +  '\033[35m'
    if fg == 'cyan':
        return_vt = return_vt +  '\033[36m'
    if fg == 'white':
        return_vt = return_vt +  '\033[37m'


    if bg == 'black':
        return_vt = return_vt +  '\033[40m'
    if bg == 'red':
        return_vt = return_vt +  '\033[41m'
    if bg == 'green':
        return_vt = return_vt +  '\033[42m'
    if bg == 'yellow':
        return_vt = return_vt +  '\033[43m'
    if bg == 'blue':
        return_vt = return_vt +  '\033[44m'
    if bg == 'magenta':
        return_vt = return_vt +  '\033[45m'
    if bg == 'cyan':
        return_vt = return_vt +  '\033[46m'
    if bg == 'white':
        return_vt = return_vt +  '\033[47m'

    return return_vt
