from reverse_fold_mcts import MonteCarloTreeSearch
from matplotlib import pyplot as plt
import numpy as np
from target_structures import target_structure_dict

def construct_similarities_list(similarity_vs_eval, evaluations):
    for i in range(1, evaluations):
        if i < len(similarity_vs_eval):
            similarity_vs_eval[i] = max(similarity_vs_eval[:i + 1])
        else:
            similarity_vs_eval.append(max(similarity_vs_eval[:i]))
    return similarity_vs_eval

def learning_behaviour(structures, plot=True, evaluations=750):
    """Average """
    similarities_ls, similarities_mcts = [], []
    for structure, i in zip(structures, range(len(structures))):
        mcts_object = MonteCarloTreeSearch(structure, RNA=False, c_parameter=0.5, max_evaluations=evaluations) # change to DNA!
        mcts_object.run()
        similarities_mcts.append(construct_similarities_list(mcts_object.similarity_memory, evaluations))
        ls_object = MonteCarloTreeSearch(structure, RNA=False, c_parameter=0.5, max_evaluations=evaluations)
        ls_object.run_local_search()
        similarities_ls.append(construct_similarities_list(ls_object.similarity_memory, evaluations))

    mean_similarities_mcts = np.array([np.mean(col) for col in zip(*similarities_mcts)])
    std_similarities_mcts = np.array([np.std(col) for col in zip(*similarities_mcts)])
    mean_similarities_ls = np.array([np.mean(col) for col in zip(*similarities_ls)])
    std_similarities_ls = np.array([np.std(col) for col in zip(*similarities_ls)])

    if plot:
        for label, color, linestyle, mean_similarities, std_similarities \
            in [("local search", 'black', "--", mean_similarities_ls, std_similarities_ls),
                ("MCTS", 'black', "-", mean_similarities_mcts, std_similarities_mcts)]:
            plt.plot(list(range(len(mean_similarities))), mean_similarities, color = color, linestyle=linestyle, label=label)
            y_minus_error = mean_similarities - std_similarities
            y_plus_error = mean_similarities + std_similarities
            plt.fill_between(range(len(mean_similarities)), y_minus_error, y_plus_error, color=color, alpha=0.1)
        plt.ylim(0.5, 1)
        plt.xlim(0, len(mean_similarities_mcts)-1)
        plt.legend()
        plt.xlabel(r"Evaluations")
        plt.ylabel("Average similarity")
        plt.savefig(f"learning_behaviour_{len(structure)}.pdf")
        plt.title(f"Sequence length: {len(structure)}")
        plt.show()

    with open('experiment_learning_behaviour_output.py', 'w') as file:
        file.write('similarities_ls = ' + str(similarities_ls) + "\n similarities_mcts= " + str(similarities_mcts))
    return

if __name__ == "__main__":
    length = 180
    learning_behaviour(target_structure_dict[length], evaluations=750)
