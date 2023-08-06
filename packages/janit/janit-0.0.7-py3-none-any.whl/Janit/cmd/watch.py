print("TEST")
def watch(args):
    if args[0] == "sync":
        my_screen = janit.out_put_screen #only print to one tty
        yield 'sync;echo "Done"'
        janit.println("\n\n\n\n\nDirty Data: " + str(_dirty_data()) + " kB", screen=my_screen)
        while _dirty_data() > 10000: #kB
            janit.println('\033[2J')
            janit.println("\n\n\n\n\nDirty Data: " + str(_dirty_data()) + " kB", screen=my_screen)
            janit.time.sleep(2)
        yield '' #press enter
    elif args[0] == "messages":
        yield 'dmesg -w'
    elif args[0] == "temperature":
        yield '''get_temp () {
        for zone in `ls /sys/class/thermal/ | grep thermal_zone`
        do
          echo -n "`cat /sys/class/thermal/$zone/type`: "
          echo `cat /sys/class/thermal/$zone/temp`
        done
        }

        get_processes() {
          top -b -n 1 | head -n 12  | tail -n 6
        }

        update () {
          while :
          do
            clear
            get_temp
            echo -e "\nTop 5 CPU hogs:"
            get_processes
            sleep 5
          done
        }


        update'''.replace('    ', '') #remove the nice looking indent

def _dirty_data():
    lines = open('/proc/meminfo').readlines()
    for line in lines:
        if line.startswith('Dirty:'):
            return(int(line.split(' ')[-2]))

def tab_watch(args):
    return ['watch sync', 'watch messages', 'watch temperature']
