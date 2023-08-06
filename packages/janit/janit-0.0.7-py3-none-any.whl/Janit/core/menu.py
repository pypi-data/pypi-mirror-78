def get_mime_type(file_name):
    command = "file --mime-type '" + file_name + "'"
    output = subprocess.getoutput(command)
    if ": " in output:
        return output.split(": ")[-1]
    else:
        return ""


def load_desktop_entrys():

    #first find all the .desktops
    paths = []
    if os.path.isdir("/usr/share/applications/"):
        paths.append("/usr/share/applications/")
    if os.path.isdir(os.path.expanduser("~") + "/.local/share/applications/"):
        paths.append("~/.local/share/applications/")
    #paths = ["/usr/share/applications/", "~/.local/share/applications/"]
    #paths = ["~/.local/share/applications/"]
    desktop_entrys_files = []
    for path in paths:
        path = os.path.expanduser(path)
        walk = list(os.walk(path))

        for entry in walk[0][-1]:
            desktop_entrys_files.append(path + entry)

    for full_path in desktop_entrys_files:
        #skip non .desktops
        if not full_path.endswith(".desktop"):
            continue
        fh = open(full_path)
        tmp_entry = {}

        #read lines from file into tmp_entry
        try:
            desktop_file_list = fh.readlines()
        except Exception:
            continue
        for line in desktop_file_list:
            #TODO add support for multi entry .desktop files
            if line.startswith("[") and line != desktop_file_list[0]:
                debug("Failed to load: " + full_path + "\n" + line, Level=1)
                break #before we overwrite the right values ;)
            #skip bad lines/first line
            if "=" in line:
                tmp_entry[line.split('=')[0]] = " ".join(line.split('=')[1:]).strip()

        if tmp_entry != {}:
            #check tmp_entry has what we need
            keys = list(tmp_entry.keys())
            if 'Type' in keys and 'Name' in keys and 'Exec' in keys:
                name_fixed = tmp_entry['Name'].replace("\xad", "")
                #check if this is a app
                if tmp_entry['Type'] == 'Application':
                    #setup min info
                    desktop_applications[name_fixed] = {'Exec': tmp_entry['Exec']}
                    #add Categories if available
                    if 'Categories' in keys:
                        desktop_applications[name_fixed]['Categories'] = tmp_entry['Categories'].strip(";").split(";")
                        #add new categories to known categories
                        for cat in desktop_applications[name_fixed]['Categories']:
                            if cat not in list(application_categories.keys()):
                                application_categories[cat] = [name_fixed]
                            else:
                                if name_fixed not in application_categories[cat]:
                                    application_categories[cat].append(name_fixed)
                    #add comment if available
                    if 'Comment' in keys:
                        desktop_applications[name_fixed]['Comment'] = tmp_entry['Comment']

                    #setup mime_type per app
                    if 'mime_type' in keys:
                        found_mimes = tmp_entry['mime_type'].strip(";").split(";")
                        desktop_applications[name_fixed]['mime_type'] = found_mimes
                        for mime in found_mimes:
                            if mime not in list(application_by_type.keys()):
                                application_by_type[mime] = [name_fixed]
                            elif name_fixed not in application_by_type[mime]:
                                application_by_type[mime].append(name_fixed)
                    else:
                        desktop_applications[name_fixed]['mime_type'] = []

    #we hand a list of all desktop entrys... Lets load them in mem
    #debug(desktop_applications)
    debug(application_by_type)
    #debug(application_categories)
