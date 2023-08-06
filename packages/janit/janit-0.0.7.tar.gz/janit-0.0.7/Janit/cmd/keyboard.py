def Type(args):
    what = " ".join(args)
    janit.println("Sleeping for 2 seconds: " + what)
    janit.time.sleep(2)

    script = ""
    for char in what:
        if char == " ":
            char = 'space'
        script = script + "xdotool key " + char + '\n'
    yield script

def keep_awake(args):
    yield """while :
    do
    xdotool key control
    sleep 30
    done"""
