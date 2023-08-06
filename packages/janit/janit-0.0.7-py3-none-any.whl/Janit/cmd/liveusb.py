#!/usr/bin/python3

def make_usb(args):
    if len(janit.object_of_attention) == 0:
        #create error user can see
        janit.debug("Error. Set path to iso in menu...", Level=3)
        return
    yield 'clear'
    yield 'lsblk'
    if len(args) == 0:
    #enter shell
        yield "..."
        yield 'read -p "WARNING! This will distroy data!\nWhat device (sda,sdb,sdc,etc): " DEV;sudo dd bs=4M if="' + janit.object_of_attention[-1][-1]+'" of=/dev/$DEV count=10M status=progress; sync'
    else:
        yield 'echo "argument not implemented yet' + str(args) + '"'


#let you add a device as an arg
#def tab_make_usb(*args):
#  debug("in tab def: " + str(args), Level=2)
#  full_cm_ds = ['test example1','test if it works', 'testing']
#  return full_cm_ds
