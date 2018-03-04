
'''
Cleans up inconsistencies in a script file.
GoT scripts have multiple authors. This file standardizes some features.

This includes
* - Marking stage direction with ### instead of XXX:, as the latter is confusing when
* parsing for dialog
* - Adding the closing square bracket when it is missing
*  - updating the speaker of dialog to consistently use a single identifier
   (for examaple, always use "NED: ..." instead of "EDDARD: ...."

Note: This file might be unnecessary for Shakespeare. If the speaker of dialog is inconsistent,
then perhaps we should just change the script file. Also, the stage directions should already
be compliant.

'''




''' Returns the string without non ASCII characters'''
def strip_non_ascii(string):

    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

'''
Gets the lines of the script from file named filename
'''
def get_script(filename):
    scriptfile = open(filename, 'r')

    scriptlines = []

    for line in scriptfile.readlines():
        # turn every "\r" into "\n"
        for subline in line.split("\r"):
            if len(subline.strip()) > 0:
                scriptlines.append(subline.replace('\n',''))

    return scriptlines

'''
Finds the standard name (eg Ned) for the given name (eg Eddard, Ned Stark, etc).
The name of the speaker will be converted to this standard identifier.
'''
def get_speaker(name):
    speaker = name.upper()

    for name_list in DIALOG_NAMES:
        #print("name list", name_list)
        key = name_list[0].upper()
        #print("key=", key)

        for name_value in name_list:
            if speaker == name_value.upper():
                speaker = key
                break


    return speaker



'''
Merges dialog from same speaker that spans multiple lines.
'''
def fix_dialog(file_name, new_file_name):
    scriptlines = get_script(file_name)

    print("fixing dialog", file_name, new_file_name)

    with open(new_file_name, 'w') as f:
        print(len(scriptlines))

        currentline = ""

        for line in scriptlines:
            line = line.strip()
            print("updating line [" + line + "]")

            if line.startswith("#") or line.startswith("-"):
                # scene change or stage direction: write cached lines
                if (len(currentline) > 0):
                    f.write(currentline)
                    f.write("\n")

                currentline = line
            elif (line.startswith("xxx:")):
                # skip this marker
                if (len(currentline) > 0):
                    f.write(currentline)
                    f.write("\n")
                # xxxab identify stage direction differently
                currentline = "### "
            else:
                # xxxAB this will break with Shakespeare, who actually uses colons!
                tokens = line.split(':')

                if len(tokens) == 1 or " " in tokens[0]:
                    # same speaker
                    currentline = currentline + " " + line
                else:
                    # new speaker: write the cached lines
                    if (len(currentline) > 0):
                        f.write(currentline)
                        f.write("\n")

                    currentline = line

        # write the final cached line
        if (len(currentline) > 0):
            f.write(currentline)
            f.write("\n")



        f.close()

    return

########
#
# main method
#
#######


'''
Creates an updated script file
* Adds closing square bracket (when missing)
* Updates the speaker of dialog to the standard name
'''
def update(old_script_file_name, new_script_file_name):
    scriptlines = get_script(old_script_file_name)

    print("updating", old_script_file_name, new_script_file_name)

    temp_file_name = new_script_file_name.split('.')[0] + "-temp.txt"

    with open(temp_file_name, 'w') as f:
        print(len(scriptlines))

        currentline = ""

        for line in scriptlines:
            line = line.strip()
            #print("updating line [" + line + "]")

            if line.startswith("["):
                if not line.endswith("]"):
                    currentline = line + "]"
                else:
                    currentline = line
            else:
                tokens = line.split(':')
                #print("tokens:",tokens)

                if len(tokens) == 1:
                    currentline = tokens[0]
                else:
                    currentline = ":".join(tokens)

            #print("current:", currentline)

            if (len(currentline) > 0):
                f.write(currentline)
                f.write("\n")

        f.close()

        fix_dialog(temp_file_name, new_script_file_name)

    return



#######
#update("/mac/NarrativeEcosystem/script/season1/data/s1e03.tex",
#      "/mac/NarrativeEcosystem/script/season1/out/s1e03-updated.txt")
