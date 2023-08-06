
#NOT USED
#returns a list of setup/unsetup chroots in ../chroots
#all = all chroots
#setup = only setup
#unsetup = only unsetup
def chroots(show="all"):
    chroot_dir = "/chroots/"
    setup_chroots = []
    unsetup_chroots = []
    for chroot_name in os.listdir(chroot_dir):
        debug("chroot_name: " + chroot_name, Level=2)
        #check if chroot is setup or not
        if os.path.isfile(chroot_dir + chroot_name + "/dev/tty"):
            setup_chroots.append(chroot_name)
        else:
            unsetup_chroots.append(chroot_name)

    if show == "all":
        return setup_chroots + unsetup_chroots
    elif show == "setup":
        return setup_chroots
    elif show == "unsetup":
        return unsetup_chroots
    else:
        #lol
        debug("chroots(show='all/setup/unsetup') called wrong...", Level=2)



#setup unsetup chroots
def setup_chroots():
    for chroot in chroots(show='unsetup'):
        pass
    #for i in dev sys proc
    pass
