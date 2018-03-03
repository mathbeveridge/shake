import itertools
import numpy as np
import re

###### FILE I/O

# get all the character ids
def get_all_characters(filename_list):
    all_char_list = []

    for filename in filename_list:
        char_data = open(filename, 'r')

        for line in char_data.readlines():
            for subline in line.split("\r"):
                words = subline.split(",")
                if len(words[0]) > 0:
                    all_char_list.append(words[0].replace(' ','_').lower())
    return all_char_list

def write_to_txt(matrix, file, type):
    page = open(file, "w")
    page.write("Source,Target,Weight,Type\n")
    log = ""
    #character_list = make_node_list(matrix)
    for character1, interactions in matrix.items():
        #print(character1, interactions)
        for character2, degree in interactions.items():
            log = character1 + "," + (character2) + "," + str(degree) + "," + type + "\n"
            if (degree != 0 and character2 != character1):
                page.write(log)
    page.close()

def make_node_list(matrix):
    log = []
    for character1, interactions in matrix.items():
        log.append(character1)
        for character2, degree in interactions.items():
            log.append(character2)
    log = sorted(list(set(log)))
    return log







# list of ignored characters should be an input
ignored_characters = [
    # season 1
    "A VOICE", "SOLDIER 1", "SOLDIER 2", "SOLDIER", "KINGS LANDING GUARD",
    "KNIGHT OF HOUSE WHENT", "KNIGHT OF HOUSE BRACKEN", "KNIGHT OF HOUSE FREY", "GUARD 1", "GUARD 2",
    "STEWARD", "WILDLING", "WILDLING 2", "KNIGHT 1", "KNIGHT 2", "KNIGHT 3", "KNIGHT 4", "KNIGHT 5",
     "KINGS GUARD", "NIGHTS WATCH BROTHER", "DOTHRAKI MAN", "STARK GUARD",
    "KINGS LANDING PAGE", "KINGS LANDING BAKER", "EVERYONE", "VOICES OUTSIDE", "NIGHTS WATCHER #1",
    "LANNISTER SOLDIER", "STARK BANNERMEN", "STREET URCHIN", "POPULACE", "STEWARD OF HOUSE STARK",
    # season 2
    "ANNOUNCER", "LORD", "THE GROUP", "CROWD", "GOLD CLOAK", "BLACKSMITH", "WATCHMAN", "ALL THREE",
    "GOLD CLOAK #2", "GUARD #1", "GUARD #2", "WOUNDED SOLDIER", "PROSTITUTE #1", "PROSTITUTE #2",
    "PRISONER", "IRONBORN", "MAN #4", "MAN #5", "MAN #6", "MAN #7", "SOLDIER #3", "SOLDIER #4",
    # season 3
    "ALL", "MEN", "MALE VOICE #1", "MALE VOICE #2", "CHILD", "CHILD #2", "MAN", "MAN #2", "BOY", "GIRL",
    "GUARD", "GUARD #2", "UNSULLIED", "MAID", "WHORE", "WOMAN", "WOMAN #2", "WOMAN #3", "WOMAN #4",
    "TAILOR", "SERVANT", "DRIVER",  "SOLDIER #2", "GUESTS", "CROWD",
     "STARK SOLDIER", "FREY SOLDIER", "FREY SOLDIER #2", "FREY SOLDIER #3", "FREY MAN", "FREY MEN",
    # season 5
    "PRIEST", "PROSTITUTE", "MASTER OF ARMS", "BRAAVOSI MAN", "WAITRESS", "KNIGHT 1", "KNIGHT 2", "KNIGHT",
    "SHADOW TOWER BROTHER", "BROTHER", "HARPY", "SQUIRE", "HUNTERS", "BROTHERS", "MAN 1", "MAN 2", "MAN 3", "MAN 4",
    "WOMAN 2", "PRIESTESS", "BYSTANDERS", "CLIENT", "MILITANT", "CAPTAIN", "GIRL", "SLAVER", "SAND SNAKES",
    "SURVIVOR", "WHITE WALKER",

    # season 6
    "NIGHT S WATCHMAN", "NIGHT S WATCHMAN #1", "NIGHT S WATCHMAN #2", "BLOODRIDER #1", "BLOODRIDER #2",
    "BLOODRIDER #3", "BLOODRIDER #4","WIFE #1", "WIFE #2", "BOLTON OFFICER", "KING S SOLDIER", "GHOST",
    "HANDMAIDEN", "LISTENERS", "DROGON", "RHAEGAL", "VISERION", "DOTHRAKI WOMAN", "DOTHRAKI MATRON",
    "KINGS SOLDIER", "KINGSGUARD", "BLOODRIDER", "MAN #1", "DOTHRAKI #1", "KHAL #1", "KHAL #2", "KHAL #3",
    "KHAL #4", "SUMMER", "CHILD OF THE FOREST", "YOUNG MAN", "YOUNG MAN #2", "RED PRIESTESS", "RED_PRIESTESS",
    "SHAGGYDOG", "ATTENDANT", "MISTRESS", "VALE KNIGHT", "SLAVE BUYER", "BOLTON BANNERMAN", "MASTER",
    "WILDLING ELDER", "GIANT", "DAUGHTER", "SHOUTING", "BROTHER", "BROTHEL KEEPER", "PROSTITUTE",
    "ANNOUNCER",

    # season 7
    "MAN #3", "MESSENGER", "UNSULLIED 1", "MAESTER 1", "MAESTER 2", "GUARD 1", "GUARD 2", "ARCHERS"
    ]

# new scene words
# this will need to be fixed later
new_scene_char = ["-", "*"]


###### script parsing

def is_new_scene(line):
    return (line[0] in new_scene_char)

def is_stage_direction(line):
    return line.startswith("[") or line.startswith("-")

# pulls the characters out of the line
def get_characters(line):
    words = strip_non_ascii(line)
    return words

# returns the string without non-ASCII characters
def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

# is this a background character?
def is_background_character(character):
    return character in ignored_characters

# gets the speaker of the dialog
def get_speaker(line):
    return line.split(":")[0]

# gets the line  dialog
def get_dialog(line):
    print("dialog is:", line)
    return line[line.index(':'):]


# creates an array of scene logs of the form
# [["[SCENE num]", line1, line2, ...], ["SCENE, line1, line2, ...] ...]
def create_script(text_file):
    scene_num = 1
    script = open(text_file, 'r')
    character_log = []
    #print("length", script.readlines().__len__())
    for line in script.readlines():
        line = strip_non_ascii(line).strip()
        print(line)
        if len(line) > 0:
            if is_new_scene(line):
                # a new scene has started
                #print("NEW SCENE WORD", line)
                character_log.append(["[SCENE " + str(scene_num) + "]"])
                scene_num = scene_num + 1
            #else:
            #    print("NOT NEW SCENE", line)
            character_log[len(character_log) - 1].append(line)
    script.close()
    return character_log



##### Encounters and Interactions

'''
return all 2-sets from the given set t
'''
def pairs(t):
    return list(itertools.combinations(t, 2))

'''
turns a character list into a dictionary
'''
def make_matrix(character_list):
    print("cl=",character_list)
    temp_dict = dict((k, 0) for k in character_list)
    matrix = dict((k, (dict((k, 0) for k in character_list))) for k in temp_dict)
    return matrix

'''
add an encounter to matrix between character1 and character2
'''
def addEncounter(matrix, character1, character2):
    # only record for first character alphabetically
    # these interactions are undirected
    character1 = character1.strip()
    character2 = character2.strip()
    if (len(character1) > 0) and (len(character2) > 0):
        print("addEncounter", character1, character2)
        if not is_background_character(character1) and not is_background_character(character2):
            if character1 < character2:
                print("matrix[", character1, "][", character2, "]")
                matrix[character1][character2] += 1
            elif character2 < character1:
                matrix[character2][character1] += 1
        else:
            print("skipping background encounter", character1, character2)

'''
Creates an interaction when characters are in the scene together. 
'''
def get_scene_interaction(script, char_list):
    temp_matrix = make_matrix(char_list)
    for scene in script:
        print(">>>>", scene)
        if (len(scene) > 0):
            inscene_characters = get_inscene_characters(scene, char_list)
            print(scene[0], inscene_characters)
            for chars in pairs(inscene_characters):
                addEncounter(temp_matrix, chars[0], chars[1])
    return temp_matrix




'''
In-scene characters have dialog or stage direction
'''
def get_inscene_characters(scene, char_list):
    scene_char_list = []
    for name in char_list:
        #scene_char_list.append(name)
        indices = [i for i, x in enumerate(scene) if name in x]
        if len(indices) > 0:
            print(name, indices)
        for ind in indices:
            line = scene[ind]
            print("     ", line)
            if is_stage_direction(line):
                if name in re.split("(\W)", line):
                    print("adding char:", name, "stage direction", line)
                    scene_char_list.append(name)
                    break
            elif name == get_speaker(scene[ind]):
                print("adding char:" , name, "speaker", scene[ind])
                scene_char_list.append(name)
                break

    print("SCENE CHARACTERS:", scene_char_list)
    return scene_char_list


'''
Creates an interaction when characters speak in sequence 
'''
def get_dialog_interaction(script, char_list):
    temp_matrix = make_matrix(char_list)

    for scene in script:
        print(">>>>", scene)
        character1 = ""
        character2 = ""

        for line in scene:
            line = line.strip()

            if len(line) > 0:
                print(line)
                if is_stage_direction(line):
                    character1 = ""
                    character2 = ""
                else:
                    character1 = character2
                    character2 = get_speaker(line)
                if len(character1) > 0 and len(character2) > 0:
                    print("adding Dialog encounter", character1, character2)
                    addEncounter(temp_matrix, character1, character2)

    return temp_matrix

'''
Creates an interaction when a character talks about other characters.
Adds a connection from speaker to referenced characters in dialog line
Adds a connection between each pair of referenced characters
'''
def get_reference_interaction(script, char_list):
    temp_matrix = make_matrix(char_list)

    for scene in script:
        for line in scene:
            print(line)
            if not is_stage_direction(line):
                speaker = get_speaker(line)
                dialog_tokens = tokens = re.split("(\W)", get_dialog(line))

                indices = [i for i, x in enumerate(char_list) if x in dialog_tokens]
                if (len(indices) > 0):
                    arr = np.array(char_list)
                    ref_list = arr[indices]

                    print("speaker:", speaker, "referenced:", ref_list)

                    for ref_char in ref_list:
                        addEncounter(temp_matrix, speaker, ref_char)

                    for chars in pairs(ref_list):
                        addEncounter(temp_matrix, chars[0], chars[1])

    return temp_matrix


'''
Creates an interaction when characters are references in a stage direction together
'''
def get_stage_interaction(script, char_list):
    temp_matrix = make_matrix(char_list)

    for scene in script:
        for line in scene:
            if is_stage_direction(line) and not is_new_scene(line):
                stage_tokens = re.split("(\W)", line)
                indices =[i for i, x in enumerate(char_list) if x in stage_tokens]
                if (len(indices) > 0):
                    arr = np.array(char_list)
                    stage_list = arr[indices]

                    print("STAGE ACTION: ", stage_list)
                    for chars in pairs(stage_list):
                        addEncounter(temp_matrix, chars[0], chars[1])

    return temp_matrix


##########################
#
# MAIN
#
##########################


'''
 perform the analysis
'''
def analyze(source_file, char_file_list, out_file_prefix):
    # sourcefile="/mac/NarrativeEcosystem/script/season3/s3e01-alias-v5.txt";

    scene_file = out_file_prefix + "-scene.csv"
    dialog_file = out_file_prefix + "-dialog.csv"
    ref_file = out_file_prefix + "-reference.csv"
    stage_file = out_file_prefix + "-stage.csv"

    all_char_list = get_all_characters(char_file_list)

    print(all_char_list)

    script = create_script(source_file)

    #############################
    # Interaction 1: in a scene together
    #print("writing scene interactions")
    #scene_matrix = get_scene_interaction(script, all_char_list)
    #write_to_txt(scene_matrix, scene_file, "undirected")

    #############################
    # Interaction 2: speak in sequence
    print("writing dialog interactions")
    dialog_matrix = get_dialog_interaction(script, all_char_list)
    write_to_txt(dialog_matrix, dialog_file, "undirected")

    #############################
    # Interaction 3: dialog reference
    print("writing reference interactions")
    ref_matrix = get_reference_interaction(script, all_char_list)
    write_to_txt(ref_matrix, ref_file, "undirected")

    #############################
    # Interaction 4: stage direction reference
    print("writing stage interactions")
    stage_matrix = get_stage_interaction(script, all_char_list)
    write_to_txt(stage_matrix, stage_file, "undirected")

    # return the names of the files that we just created
    return [ scene_file, dialog_file, ref_file, stage_file]

