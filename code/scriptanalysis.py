import itertools
import numpy as np
import re

#### Constants

# list of ignored characters
ignored_characters = [
    "All"
    ]

# new scene words
# this will need to be fixed later
new_scene_char = ["-", "*"]

stage_dir_char = ["[","#"]

###### FILE I/O

# get all the character ids, which are the first column of the alias csv file
def get_all_characters(filename_list):
    all_char_list = []

    for filename in filename_list:
        char_data = open(filename, 'r')

        for line in char_data.readlines():
            for subline in line.split("\r"):
                words = subline.split(",")
                if len(words[0]) > 0:
                    all_char_list.append(words[0].replace(' ','_'))
    return all_char_list

# writes out the edges in matrix to a file
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

# creates a list of all the characters appearing in edges
def make_node_list(matrix):
    log = []
    for character1, interactions in matrix.items():
        log.append(character1)
        for character2, degree in interactions.items():
            log.append(character2)
    log = sorted(list(set(log)))
    return log



###### script parsing

def is_new_scene(line):
    return (line[0] in new_scene_char)

def is_stage_direction(line):
#    return line.startswith("[") or line.startswith("-") or line.startswith("#")
   return (line[0] in stage_dir_char)

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
    print("char list is ",character_list)
    temp_dict = dict((k, 0) for k in character_list)
    matrix = dict((k, (dict((k, 0) for k in character_list))) for k in temp_dict)
    print("matrix is ", matrix)
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
            elif name == get_speaker(line):
                print("adding char:" , name, "speaker", scene[ind])
                scene_char_list.append(name)
                break
            else:
                # xxxab look for stage direction within dialog
                stage_dir = re.findall('\[.*?\]', line)
                for s in stage_dir:
                    if name in re.split("(\W)", line):
                        print("adding char:", name, "dialog stage direction", line)
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
                    # break the chain of interaction
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
Creates an cvs file whose lines are character1, character2, Line Number(of character1)
'''
def get_dialog_timeline(script, char_list, dialog_timeline_file):
    output_file = open(dialog_timeline_file, "w")
    char_set = set(char_list)

    lineNum = 1

    for scene in script:
        print(">>>>", scene)
        character1 = ""
        character2 = ""

        for line in scene:
            line = line.strip()

            if len(line) > 0:
                print(line)
                if is_stage_direction(line):
                    # break the chain of interaction
                    character1 = ""
                    character2 = ""
                else:
                    character1 = character2
                    character2 = get_speaker(line)
                if len(character1) > 0 and len(character2) > 0:
                    if character1 in char_set and character2 in char_set:
                        print("adding Dialog and line number", character1, character2)
                        output_file.write(character1 + "," + character2 + "," + str(lineNum) + "\n")

            lineNum += 1

    output_file.close()

'''
Creates an interaction when a character talks about other characters.
Adds a connection from speaker to referenced characters in dialog line
Adds a connection between each pair of referenced characters
'''
def get_reference_interaction(script, char_list):
    temp_matrix = make_matrix(char_list)

    for scene in script:
        for line in scene:
            #print("<", line, ">")
            if not is_stage_direction(line) and not is_new_scene(line):
                speaker = get_speaker(line)
                dialog_tokens = tokens = re.split("(\W)", get_dialog(line))

                indices = [i for i, x in enumerate(char_list) if x in dialog_tokens]
                if (len(indices) > 0):
                    arr = np.array(char_list)
                    ref_list = arr[indices]

                    #print("speaker:", speaker, "referenced:", ref_list)

                    for ref_char in ref_list:
                        addEncounter(temp_matrix, speaker, ref_char)

                    for chars in pairs(ref_list):
                        addEncounter(temp_matrix, chars[0], chars[1])

    return temp_matrix


'''
Creates an interaction when a character talks about other characters.
Creates a timeline of all the interactions using line number
'''
def get_reference_timeline(script, reference_timeline_file, char_list):

    output_file = open(reference_timeline_file, "w")

    lineNum = 1

    for scene in script:
        for line in scene:
            if not is_stage_direction(line) and not is_new_scene(line):
                speaker = get_speaker(line)
                dialog_tokens = tokens = re.split("(\W)", get_dialog(line))

                indices = [i for i, x in enumerate(char_list) if x in dialog_tokens]
                if (len(indices) > 0):
                    arr = np.array(char_list)
                    ref_list = arr[indices]
                    for ref_char in ref_list:
                        output_file.write(speaker + "," + ref_char + "," + str(lineNum)  + "\n")
                    for chars in pairs(ref_list):
                        output_file.write(chars[0] + "," + chars[1] + "," + str(lineNum) + "\n")
            lineNum += 1

    output_file.close()



'''
Creates an interaction when characters are references in a stage direction together
Right now, this assumes that the character id matches the way that they are referred to in 
stage direction, which is not necessarily true.
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

                    #print("STAGE ACTION: ", stage_list)
                    for chars in pairs(stage_list):
                        addEncounter(temp_matrix, chars[0], chars[1])

    return temp_matrix


'''
Creates an interaction when characters are references in a stage direction together
Creates a timeline of all the interactions using line number
'''
def get_stage_timeline(script, stage_timeline_file, char_list):

    output_file = open(stage_timeline_file, "w")

    lineNum = 1

    for scene in script:
        for line in scene:
            if is_stage_direction(line) and not is_new_scene(line):
                stage_tokens = re.split("(\W)", line)
                indices =[i for i, x in enumerate(char_list) if x in stage_tokens]
                if len(indices) > 0:
                    arr = np.array(char_list)
                    stage_list = arr[indices]

                    for chars in pairs(stage_list):
                        output_file.write(chars[0] + "," + chars[1] + "," + str(lineNum) + "\n")
            lineNum += 1

    output_file.close()


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
    dialog_timeline = out_file_prefix + "-dialog-timeline.csv"
    reference_timeline = out_file_prefix + "-reference-timeline.csv"
    stage_timeline = out_file_prefix + "-stage-timeline.csv"

    all_char_list = get_all_characters(char_file_list)

    print(all_char_list)

    script = create_script(source_file)

    #############################
    # Interaction 1: in a scene together
    print("writing scene interactions")
    scene_matrix = get_scene_interaction(script, all_char_list)
    write_to_txt(scene_matrix, scene_file, "undirected")

    #############################
    # Interaction 2: speak in sequence
    print("writing dialog interactions")
    dialog_matrix = get_dialog_interaction(script, all_char_list)
    write_to_txt(dialog_matrix, dialog_file, "undirected")

    #############################
    # Interaction 2.1: dialog timeline
    print("writing dialog timeline")
    get_dialog_timeline(script, all_char_list, dialog_timeline)

    #############################
    # Interaction 3: dialog reference
    print("writing reference interactions")
    ref_matrix = get_reference_interaction(script, all_char_list)
    write_to_txt(ref_matrix, ref_file, "undirected")

    #############################
    # Interaction 3.1: dialog reference timeline
    print("writing reference timeline")
    get_reference_timeline(script, reference_timeline, all_char_list)

    #############################
    # Interaction 4: stage direction reference
    print("writing stage interactions")
    stage_matrix = get_stage_interaction(script, all_char_list)
    write_to_txt(stage_matrix, stage_file, "undirected")

    #############################
    # Interaction 4.1: stage direction timeline
    print("writing stage timeline")
    get_stage_timeline(script, stage_timeline, all_char_list)

    # return the names of the files that we just created
    return [ scene_file, dialog_file, ref_file, stage_file]

