#
# Merges together multiple edge CSV files into a single CSV file.
# This is helpful for GoT, where we start by making a network for each episode,
# but want to create a network for the season as a whole.
#



################## HELPER METHODS

# loads the script file
def get_lines(filename):
    matrixfile = open(filename, 'r')
    matrixlist = matrixfile.readlines()
    return matrixlist


# debug print of the given dictionary
def pretty(d):
    pretty(d, 0)

# debug print implementation
def pretty(d, indent=0):
    keys = sorted(d.keys())
    for key in keys:
        print('\t' * indent + str(key))
        value = d.get(key)
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


# add the edges from edge_list to edge_dict
def add_edges(edge_dict, edge_list):
    for line in edge_list:
        val = line.split(",")
        # character names in alphabetical order
        if (val[0] < val[1]):
            char1 = val[0]
            char2 = val[1]
        else:
            char2 = val[0]
            char1 = val[1]

        print("adding", char1, char2, val[2])
        if (not char1 in edge_dict):
            edge_dict[char1] = {}

        char_dict = edge_dict[char1]

        if (not char2 in char_dict):
            edge_dict[char1][char2] = 0

        edge_dict[char1][char2] += int(val[2])

    return edge_dict

# Add the edges in file_name to the edge_dict
def add_edges_from_file(edge_dict, file_name):
    edge_list = get_lines(file_name)
    # don't need the header line
    edge_list.pop(0)

    edge_dict = add_edges(edge_dict, edge_list)

    return edge_dict

# Write the contents of edge_dict to filename
def write_edge_file(edge_dict, filename):
    print("writing to", filename)
    with open(filename, 'w') as f:
        f.write("Source,Target,Weight,Type\n")
        keys = sorted(edge_dict.keys())
        for key in keys:
            values = edge_dict.get(key)
            for value in values:
                f.write(key + "," + value + "," +  str(edge_dict[key][value]) + ",Undirected\n" )
        f.close()

################## MAIN METHOD


def merge(file_name_list, out_file_name):

    edge_dict = dict()

    for file_name in file_name_list:
        edge_dict = add_edges_from_file(edge_dict, file_name)

    write_edge_file(edge_dict, out_file_name)

    return




############
# testing
#############
#
#file_names = ["/mac/NarrativeEcosystem/script/season3/s3e03mat-scene.csv",
#            "/mac/NarrativeEcosystem/script/season3/s3e03mat-dialog.csv",
#            "/mac/NarrativeEcosystem/script/season3/s3e03mat-reference.csv",
#            "/mac/NarrativeEcosystem/script/season3/s3e03mat-stage.csv" ]
#
#
# edge_dict = add_edges_from_file(edge_dict, "/mac/NarrativeEcosystem/script/season3/s3e03mat-scene.csv")
# #pretty(edge_dict)
#
# #edge_dict = add_edges_from_file(edge_dict, "/mac/NarrativeEcosystem/script/season3/s3e01edges-full.csv")
# #edge_dict = add_edges_from_file(edge_dict, "/mac/NarrativeEcosystem/script/season3/s3e02edges-full.csv")
#
# write_edge_file(edge_dict, "/mac/NarrativeEcosystem/script/season3/s3e03edges-v2.csv")