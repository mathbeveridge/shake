import re
import pandas as pd
import csv
from pathlib import Path


def parse_play(play_file):
    play = [s.strip() for s in Path(play_file).read_text().split(sep='\n' * 2)]
    col_names = ['Act', 'Scene', 'Speaker', 'Text']
    df = pd.DataFrame(columns=col_names)

    act, scene = 0, 0
    timestamp = 1
    for line in play:
        match = re.search(r"Act (\d), Scene (\d)", line)
        if match:
            act, scene = match.groups()
        elif line and line[0] != '-' and line[0] != '*':
            split_lines = line.splitlines()
            speaker = re.search(r"(\w+):*", split_lines[0]).group(1)  # remove the colon
            text = '\n'.join(split_lines[1:])
            # TODO: make this more efficient – this is not the recommended way to work with pandas
            df = df.append(pd.DataFrame(dict(zip(col_names, [int(act), int(scene), speaker, text])), index=[timestamp]))
            timestamp += 1
    return df.query('Act > 0 & Scene > 0')


def _read_alias_files(alias_files):
    # read the alias file and parse into list of aliases
    aliases = []
    for i, alias_file in enumerate(alias_files):
        with open(alias_file) as f:
            reader = csv.reader(f)
            aliases.extend([l for l in reader if l])
    # eliminate empty strings if there are any
    for i, a in enumerate(aliases):
        aliases[i] = [name for name in a if name]

    return aliases


def get_alias_mapping(alias_files):
    aliases = _read_alias_files(alias_files)
    names = [alias[0] for alias in aliases]
    alias_map = {name: i for i, name in enumerate(names)}
    reverse_map = dict(zip(alias_map.values(), alias_map.keys()))
    return alias_map, reverse_map


def tokenize(play, alias_files):
    if isinstance(play, pd.DataFrame):
        play_df = play
    else:
        play_df = parse_play(play)

    aliases = _read_alias_files(alias_files)

    def tokenize_text(text):
        text_tokens = []
        for alias in aliases:
            if any([name in text for name in alias]):
                text_tokens.append(alias[0])
        return text_tokens

    tokens = [tokenize_text(t) for t in play_df['Text']]
    play_df['Tokens'] = tokens
    return play_df
