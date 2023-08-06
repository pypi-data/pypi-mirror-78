####################Starting with the most important##############################\
#broken :'( TODO
def freethefish(args):
    #TODO have fish exit screen clean, wait and re-enter.
    #TODO start fish in randint place
    term_size = janit.vt_size()
    fishyx = [int(term_size[0]/2),0]
    old_fishyx = fishyx
    fish_text = "><>"
    org_text = ""
    janit.fish_rest = False


    while janit.RUNNING and not janit.fish_rest:
        #janit.debug("Fish status: " + str(janit.fish_rest), Level=3)
        if org_text != "":
            for i in range(0, len(org_text)):
                try:
                    janit.output_data[janit.out_put_screen][fishyx[0]][fishyx[1] + i].data = org_text[i]
                except Exception:
                    pass
            #debug("Moving to: " + str(old_fishyx))
            #debug("added: " + str(org_text))

        #org_text = janit.stdscr.instr(fishyx[0], fishyx[1], 3)
        for i in range(0,3):
            try:
                org_text = org_text + janit.output_data[janit.out_put_screen][fishyx[0]][fishyx[1] + i].data
            except Exception:
                pass

        #output_data[janit.out_put_screen][fishyx[0]][fishyx[1]].data

        #janit.debug(org_text)
        #janit.debug(fishyx)


        for i in range(0, len(fish_text)):
            try:
                janit.output_data[janit.out_put_screen][fishyx[0]][fishyx[1] + i].data = fish_text[i]
            except Exception:
                pass
        #janit.stdscr.move(fishyx[0], fishyx[1])
        #janit.stdscr.addstr(fish_text)
        janit.debug("HELLO", Level=3)
        old_fishyx = [fishyx[0], fishyx[1]] #Why The Fuck can't I put: old_fishyx = fishyx ???
        ###move fish
        direction = janit.random.randint(1,3)
        if direction == 2 and fishyx[0] < term_size[0] -5:
            fishyx[0] = fishyx[0] + 1
        if direction == 3 and fishyx[0] > 2:
            fishyx[0] = fishyx[0] - 1
        #move forward
        if fishyx[1] < term_size[1] - 2:
            fishyx[1] = fishyx[1] + 1
        #fish at end of screen.. sleep and reset.
        else:
            #time.sleep(2)
            fishyx = [int(term_size[0]/2),0]
        #update screen
        #debug(yx)
        #sleep
        janit.time.sleep(.5)


def stopthefish(args):
    janit.debug("Fish status change: " + str(janit.fish_rest), Level=3)
    janit.fish_rest = True

def starwars(args):
    return(["telnet towel.blinkenlights.nl"])
