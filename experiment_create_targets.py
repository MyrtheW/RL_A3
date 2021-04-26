import random
from reverse_fold_mcts import MonteCarloTreeSearch
from target_structures import target_structure_dict

if __name__ == "__main__":
    if input("Do you want to create new targets? y/n") == "y":
        random.seed(10)
        structure_lengths = list(range(20,200,20))
        desired_targets = 10 # per length

        target_structure_dict = {length:[] for length in structure_lengths} # if length not in target_structure_dict.keys()}
        for length in structure_lengths:
            for _ in range(desired_targets):
                 sequence = "".join([random.choice(["A","C", "G", "T"]) for i in range(length)])
                 target_structure_dict[length].append(MonteCarloTreeSearch().call_RNAfold(sequence))
        with open('target_structures.py', 'w') as file:
            file.write('target_structure_dict = '+ str(target_structure_dict))