# -*- coding: utf-8 -*-

import pickle
from reverse_fold_mcts import MonteCarloTreeSearch
import numpy as np
from target_structures import target_structure_dict

grid = {}
lengths = [20, 60, 100, 140, 180]
cp_parameters = [10 ** i for i in range(-3, 4)]
decay_factors = [10 ** i for i in range(-6, -1)]

for decay_factor in decay_factors:
    grid[decay_factor] = {}
    for length in lengths:
        grid[decay_factor][length] = {}
        structures = target_structure_dict[length]
        mean_similarities = np.empty(0)
        std_similarities = np.empty(0)
        for cp_parameter in cp_parameters:
            similarities = np.empty(0)
            for structure, i in zip(structures, range(len(structures))):
                # similarity = (decay_factor, cp_parameter, length, i) line used to test the grid
                similarity = MonteCarloTreeSearch(
                    structure,
                    RNA=False,
                    c_parameter=cp_parameter,
                    max_evaluations=500,
                    decaying_cp=True,
                    cp_decay=decay_factor,
                ).run()[1]
                print(
                    f"decay factor = {decay_factor}, length = {length}, Cp = {cp_parameter}, i = {i}, sim = {similarity:.2f}"
                )
                similarities = np.append(similarities, similarity)
            mean_similarities = np.append(mean_similarities, np.mean(similarities))
            std_similarities = np.append(std_similarities, np.std(similarities))
        grid[decay_factor][length] = {
            "mean_sims": mean_similarities,
            "std_sims": std_similarities,
        }

pick_filename = "grid_search_decay_values"
with open(pick_filename, "wb") as outfile:
    pickle.dump(grid, outfile)

with open(pick_filename, "rb") as infile:
    grid_load = pickle.load(infile)