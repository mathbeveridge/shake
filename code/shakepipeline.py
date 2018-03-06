import updatescript
import updatealias
import scriptanalysis
import edgemerge
import os

'''
The driver file that turns a set of scripts into a network.
'''

'''
Configuration assumptions:


1. Your alias file must match your play file. 
For example: "macbeth.txt" and "macbeth.csv"

2. The first name that appears in the alias file must match the name used in the dialog of the play.
For example, here is a line from macbeth.csv

oldman_mac,Old Man,old Man,father_oldman

When the Old Man speaks, his dialog is identified by "oldman_mac: xxxxxxxxx"

3. The code automatically includes an all-uppercase version of your aliases. It does NOT currently
include all-lowercase versions of your aliases. (That breaks part of the code right now...)

4. You need to update your play and alias file to use underscore instead of dash.
For example, I ran a Replace All to change "-mac" to "_mac". 

The reason for this change: python treats underscore as a word character, 
but treats dash as a non-word character.

5. You must update your play.txt file as follows:
- The first line should be "---------------------" which indicates the start of a new scene
- Replace "Act 1, Scene 1" with "# Act 1, Scene 1", etc. This leading '#' indicates that
  this line is metadata (not dialog)

6. WARNING: there is one quirk right now. The code identifys a speaker by a line that begins
Character: ....
but this means that when Shakespeare starts a line with a word and then a colon 
(eg "Hark: who goes there?") 
you will get a "Key Error" for "Hark"
The workaround: edit the play.txt file and replace "Hark:" (colon) with "Hark;" (semicolon).
This is a manual process, and there won't be too many of them (probably 5-10). 
So I suggest that you just run the script, let it fail, change the offending colon, and repeat.

'''


########################################
# Configure the following to match your filesystem
# and the play that you want to process

#mydir
my_dir = "/Users/abeverid/PycharmProjects/shake/"

# play
play = "othello"




########################################

#datadir
data_dir = my_dir + "data/"

#outdir
out_dir = my_dir + "out/" + play + "/"


if not os.path.exists(out_dir):
    os.makedirs(out_dir)


# currently support import of more than one alias file
alias_file_list = [
    data_dir + "alias/" + play + ".csv"
]

raw_script_file = data_dir + "plays/" + play +  ".txt"

# output files
out_file_prefix = out_dir + play

update_script_file = out_file_prefix + "-updated.txt"
alias_script_file = out_file_prefix + "-alias.txt"
edge_file_prefix = out_file_prefix + "-edge"
final_edge_file = edge_file_prefix + "-all.csv"

print("UPDATING")
updatescript.update(raw_script_file, update_script_file)

print("ALIASING")
updatealias.update(update_script_file, alias_script_file, alias_file_list)

print("ANALYZING")
edge_file_list = scriptanalysis.analyze(alias_script_file, alias_file_list, edge_file_prefix)

print("MERGING")
edgemerge.merge(edge_file_list, final_edge_file)


