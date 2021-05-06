# -*- coding: utf-8 -*-

import pickle
import matplotlib.pyplot as plt

pick_filename = "grid_search_values"

with open(pick_filename, "rb") as infile:
    grid = pickle.load(infile)

lengths = [20, 60, 100, 140, 180]
cp_parameters = [10 ** i for i in range(-3, 4)]
max_evals = [100, 300, 500, 700, 900]
color_cycle = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
]
# similarity vs cp for a constant evaluations and length

# evaluations = 900
# length = 180
for length in lengths:
    fig, ax = plt.subplots()
    for evaluations, i in zip(max_evals, range(len(max_evals))):
        mean_similarities = grid[evaluations][length]["mean_sims"]
        std_similarities = grid[evaluations][length]["std_sims"]
        y_minus_error = mean_similarities - std_similarities
        y_plus_error = mean_similarities + std_similarities
        color = color_cycle[i]

        ax.plot(cp_parameters, mean_similarities, color=color, label=evaluations)
        ax.fill_between(
            cp_parameters, y_minus_error, y_plus_error, color=color, alpha=0.2
        )
    ax.set_xscale("log")
    ax.set_ylim(0.7, 1)
    ax.set_xlabel(r"$C_p$")
    ax.set_ylabel("Similarity")
    ax.set_title(f"Sequence length: {length}")
    ax.legend(loc="lower left")
    fig.savefig(f"plots/sim_vs_cp_{length:03d}.pdf")
    # fig.show()