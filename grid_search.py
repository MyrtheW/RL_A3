# -*- coding: utf-8 -*-

import pickle
from reverse_fold_mcts import MonteCarloTreeSearch
import numpy as np
from target_structures import target_structure_dict

grid = {}
lengths = [20,60,100,140,180]
cp_parameters = [10**i for i in range(-3,4)]
max_evals = [100,300,500,700,900]

for evaluations in max_evals:
    grid[evaluations] = {}
    for length in lengths:
        grid[evaluations][length] = {}
        structures = target_structure_dict[length]
        mean_similarities = np.empty(0)
        std_similarities = np.empty(0)
        for cp_parameter in cp_parameters:
            similarities = np.empty(0)
            for structure, i in zip(structures, range(len(structures))):
                similarity = MonteCarloTreeSearch(structure,
                                                  RNA=False,
                                                  c_parameter=cp_parameter,
                                                  max_evaluations=evaluations).run()[1]
                print(f'evals = {evaluations}, length = {length}, Cp = {cp_parameter}, i = {i}, sim = {similarity:.2f}')
                similarities = np.append(similarities, similarity)
            mean_similarities = np.append(mean_similarities, np.mean(similarities))
            std_similarities = np.append(std_similarities, np.std(similarities))
        grid[evaluations][length] = {'mean_sims': mean_similarities, 
                                     'std_sims': std_similarities}

# mean_similarities = np.empty(0)
# std_similarities = np.empty(0)
# 
# for evaluations in max_evals:
#     for length in lengths:
#         structures = target_structure_dict[length]
#         for cp_parameter in cp_parameters:
#             similarities = np.empty(0)
#             for structure, i in zip(structures, range(len(structures))):
#                 similarity = MonteCarloTreeSearch(structure,
#                                                   RNA=False,
#                                                   c_parameter=cp_parameter,
#                                                   max_evaluations=evaluations).run()[1]
#                 print(f'evals = {evaluations}, length = {length}, Cp = {cp_parameter}, i = {i}, sim = {similarity:.2f}')
#                 similarities = np.append(similarities, similarity)
#             mean_similarities = np.append(mean_similarities, np.mean(similarities))
#             std_similarities = np.append(std_similarities, np.std(similarities))
#         grid[evaluations] = {length: {'mean_sims': mean_similarities, 
#                                       'std_sims': std_similarities}}

pick_filename = 'grid_search_values'
with open(pick_filename, 'wb') as outfile:
    pickle.dump(grid, outfile)

with open(pick_filename, 'rb') as infile:
    grid_load = pickle.load(infile)