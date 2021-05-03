# -*- coding: utf-8 -*-

import pickle
import matplotlib.pyplot as plt

pick_filename = 'grid_search_values'

with open(pick_filename, 'rb') as infile:
    grid = pickle.load(infile)
    
lengths = [20,60,100,140,180]
cp_parameters = [10**i for i in range(-3,4)]
max_evals = [100,300,500,700,900]

evaluations = 100
length = 180

mean_similarities = grid[evaluations][length]['mean_sims']
std_similarities = grid[evaluations][length]['std_sims']

color = 'g'
plt.plot(cp_parameters, mean_similarities, color = color)
y_minus_error = mean_similarities - std_similarities
y_plus_error = mean_similarities + std_similarities
plt.fill_between(cp_parameters, y_minus_error, y_plus_error, color = color, alpha = 0.2)
plt.xscale('log')
plt.ylim(0.5, 1)
plt.xlabel(r"$C_p$")
plt.ylabel("Similarity")
plt.title(f"Sequence length: {length}, max MCTS evaluations: {evaluations}")
# plt.savefig(f"cp_plot_{length}_{evaluations}.pdf")
plt.show()