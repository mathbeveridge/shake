import re


#
# Creates an aliased version of the script that removes whitespace and
# apostrophes from nicknames. This way each identifier is a single word.
#
#
#

'''
Loads the list of aliases from each csv file in filename_list
'''
def get_alias_list(filename_list):
    aliaslist = []
    for filename in filename_list:
        print("loading alias file", filename)
        aliasfile = open(filename, 'r')
        for aliasline in aliasfile.readlines():
            aliaslist.extend(aliasline.split('\r'))
        #aliaslist.extend(aliasfile.readlines()[0].split('\r'))
    return aliaslist




'''
Implementation of the update of the file
* replace apostrophe with a space
* update appearances of nicknames with underscored version, ie "foo bar zap" becomes "foo_bar_zap"
  so that each identifier is a single word. 
'''
def change(old_filename, new_filename, aliaslist):
    # Safely read the input filename using 'with'
    with open(old_filename) as f:
        s = f.read()
    # get rid of apostrophes
    s= s.replace("'", " ")

    nick_list = [];

    # first, we update nicknames with underscored versions
    for line in aliaslist:
        line = line.strip("\n");
        print("handling: ", line)

        if len(line) > 0:
            nicknames = line.split(",")
            # record the nickname list for phase two
            temp_nick_list = []
            for nickname in nicknames:
                nick = nickname.strip()
                if (len(nick) > 0):
                    # get rid of spaces and apostrophes in the nickname
                    nick_id = nick.replace("'", " ").replace(' ', '_')
                    temp_nick_list.append((nick_id))
                    if (nick != nick_id):
                        print("replacing with dashed", nick, nick_id)
                        s = s.replace(nick, nick_id)
            nick_list.append(temp_nick_list)

    print("nickname list is: ", nick_list)

    # second, we update tokenized names with the id
    # split on non-word characters
    tokens = re.split("(\W)", s)

    for char_nick in nick_list:
        #print("DEBUG: " , char_nick)
        nick_id = char_nick.pop(0)
        #print("nick_id=", nick_id, char_nick)
        for nick in char_nick:
            #print("replacing tokenized:", nick, nick_id)
            #tokens = [w.replace(nick, nick + " (" + nick_id + ")") for w in tokens]
            if nick in tokens:
                indices = [i for i, x in enumerate(tokens) if x == nick]
                for ind in indices:
                    tokens[ind] = nick + " (" + nick_id + ")"
            #tokens = [w == nick ? w : nick + " (" + nick_id + ")") for w in tokens]

    # write updated script to file
    with open(new_filename, 'w') as f:
        f.write("".join(tokens))

    f.close()


#########################
#
# MAIN
#
#######################

'''
Creates a new version of the script
'''
def update(old_file_name, new_file_name, alias_file_name):
    aliaslist = get_alias_list(alias_file_name)


    change(old_file_name,
           new_file_name,
           aliaslist)
    return

