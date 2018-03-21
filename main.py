from pathlib import Path
from os import makedirs
import argparse
import sys

from code import updatescript
from code import updatealias
from code import scriptanalysis
from code import edgemerge


parser = argparse.ArgumentParser(description="Create graphs for analyzing Shakespeare plays")
parser.add_argument('play_name', metavar='Play name',
                    help='the name of the play to be parsed, for example "macbeth"')
parser.add_argument('--play-file', help='the path of the play file')
parser.add_argument('--alias-files', nargs='+',
                    help='the path of the alias file(s)')
parser.add_argument('--out-dir', default='out',
                    help='location to put output directory')
args = parser.parse_args()

root_dir = Path(sys.argv[0]).parent.resolve()
data_dir = root_dir / 'data'

args.alias_files = args.alias_files or [data_dir.joinpath('alias', args.play_name + '.csv')]
args.alias_files = [Path(x) for x in args.alias_files]
args.alias_files = [x for x in args.alias_files if x.exists()]

args.play_file = args.play_file or data_dir.joinpath('plays', args.play_name + '.txt')
args.play_file = Path(args.play_file)

if not args.alias_files or not args.play_file.exists():
    raise FileExistsError("Could not find play and alias file(s) for {}".format(args.play_file.name))

# make out directory if it doesn't already exist
out_dir = root_dir.joinpath(args.out_dir, args.play_name)
if not out_dir.exists():
    makedirs(str(out_dir))

args.play_file = str(args.play_file)
args.alias_files = [str(x) for x in args.alias_files]
update_script_file = str(out_dir.joinpath(args.play_name + "-updated.txt"))
alias_script_file = str(out_dir.joinpath(args.play_name + "-alias.txt"))
edge_file_prefix = str(out_dir.joinpath(args.play_name + "-edge"))
final_edge_file = str(out_dir.joinpath(args.play_name + "-all.csv"))

print("UPDATING")
updatescript.update(args.play_file, update_script_file)

print("ALIASING")
updatealias.update(update_script_file, alias_script_file, args.alias_files)

print("ANALYZING")
edge_file_list = scriptanalysis.analyze(alias_script_file, args.alias_files, edge_file_prefix)

print("MERGING")
edgemerge.merge(edge_file_list, final_edge_file)