from reverse_fold_mcts import MonteCarloTreeSearch
import config
parameter_dictionary, _ = config.loadConfig("./config.txt")
sequence, similarity, predicted_structure, _ = MonteCarloTreeSearch(**parameter_dictionary).run()
print(sequence)

