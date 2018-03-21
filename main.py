from pathlib import Path
from os import makedirs
import argparse
from code.preprocess import tokenize, get_alias_mapping
from code.interactions import get_scene_interactions
import sys


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

# get data table with tokens
play_df = tokenize(args.play_file, args.alias_files)
alias_map, reverse_map = get_alias_mapping(args.alias_files)
print(get_scene_interactions(play_df, alias_map))

# parse out and interpret stage directions
# make stage directions table
