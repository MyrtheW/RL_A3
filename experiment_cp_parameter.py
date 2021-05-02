from reverse_fold_mcts import MonteCarloTreeSearch
from matplotlib import pyplot as plt
import numpy as np
from target_structures import target_structure_dict

def cp_experiments(structures, length, cp_parameters=[10**i for i in range(-3,4)],
                   runs_per_structure = 1, plot=True, evaluations=750):
    """runs for given structures the Cp parameter (x) against similarity (y)"""
    mean_similarities = np.empty(0)
    std_similarities = np.empty(0)
    for cp_parameter in cp_parameters:
        similarities = np.empty(0)
        for structure, i in zip(structures, range(len(structures))):
            for j in range(runs_per_structure):
                similarity = MonteCarloTreeSearch(structure,
                                                  RNA=False,
                                                  c_parameter=cp_parameter,
                                                  max_evaluations=evaluations).run()[1]
                print(f'Cp = {cp_parameter}, i = {i}, j = {j}, sim = {similarity:.2f}')
                similarities = np.append(similarities, similarity)
        mean_similarities = np.append(mean_similarities, np.mean(similarities))
        std_similarities = np.append(std_similarities, np.std(similarities))
    return cp_parameters, mean_similarities, std_similarities

if __name__ == "__main__":
    length = 180
    evaluations = 2*length
    cp_parameters, mean_similarities, std_similarities = cp_experiments(
                   target_structure_dict[length],
                   length,
                   cp_parameters=[10**i for i in range(-3,4)],
                   runs_per_structure=1,
                   evaluations=evaluations)
    #improve plot: plot from 0.5 (random) to 1 and logarthmic scale on x acix.
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
    plt.savefig(f"cp_plot_{length}_{evaluations}.pdf")
    plt.show()
    
