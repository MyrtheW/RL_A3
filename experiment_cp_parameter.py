from reverse_fold_mcts import MonteCarloTreeSearch
from matplotlib import pyplot as plt
import numpy as np
from target_structures import target_structure_dict

def cp_experiments(structures, cp_parameters=[10**i for i in range(-3,4)], plot=True, evaluations=60):
    """runs for given structures the Cp parameter (x) against similarity (y)"""
    averages_vs_cp = []
    std_vs_cp = []
    for cp_parameter in cp_parameters:
        similarities = []
        for structure in structures:
            similarities.append(MonteCarloTreeSearch(structure, cp_parameter, max_evaluations=evaluations).run()[1])
        averages_vs_cp.append(np.mean(similarities))
        std_vs_cp.append(np.std(similarities))

    if plot:
        #improve plot: plot from 0.5 (random) to 1 and logarthmic scale on x acix.
        plt.errorbar(x=cp_parameters, y=averages_vs_cp, yerr=std_vs_cp, c="black", capsize=10)
        plt.xscale('log')
        plt.ylim(0.5, 1)
        plt.xlabel("Cp parameter")
        plt.ylabel("Similarity")
        plt.title("Sequence length: "+ str(len(structure)) + ", function evaluations: 36")
        plt.savefig("cp_plot")
        plt.show()
        None


if __name__ == "__main__":
    length = 180
    cp_experiments(target_structure_dict[length], cp_parameters=[10**i for i in range(-3,4)])