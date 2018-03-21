import itertools
import numpy as np
from scipy import sparse


def get_scene_interactions(df, alias_map):
    def get_interaction_matrix(char_list):
        char_pairs = itertools.combinations([alias_map[c] for c in char_list], 2)
        row, col = list(zip(*char_pairs))
        n = len(row)
        matrix = sparse.coo_matrix((np.ones(n), (row, col)), shape=(n, n))
        return matrix + matrix.T

    # groups data by each scene and flattens the token column to get all the characters who we referred to in the scene
    grouped = df.groupby(['Act','Scene'])['Tokens'] \
        .agg(lambda x: get_interaction_matrix(list(set(itertools.chain.from_iterable(x)))))
    print(grouped)
    return grouped.agg(np.add)


def get_dialog_interactions(df):
    pass


def get_reference_interactions(df):
    pass


def get_stage_interactions(df):
    pass

