import numpy as np
import random
import os, subprocess
import warnings


"""MONTE CARLO TREE SEARCH"""
class Node:
    def __init__(self, position=None, parent=None, root=False, sequence_dict={}):
        self.children = []
        self.parent = parent
        self.position = position
        self.sequence_dict = sequence_dict #{1:"A", (2,4):"CG"}
        self.similarity = 0 #q
        self.visits = 1 #n
        #self.leaf = #kan worden berekend aan de hand van de lengte van sequence dict of worden bijgehouden.
        self.root = root


    def add_child(self, position, nucleotide):
        #randomly select position from position set
        # select all nucleotides/ nucleotide
        new_node = Node(parent=self, sequence_dict=self.sequence_dict.copy())
        new_node.sequence_dict.update({position:nucleotide})
        self.children.append(new_node)

    def update_stats(self, similarity):
        self.similarity += similarity
        self.visits += 1


class MonteCarloTreeSearch:
    def __init__(
            self,
            target_structure="(((((...(((.....)))...)).)))",
            RNA=False,
            RNAfold_directory= "C:\Program Files (x86)\ViennaRNA Package\RNAfold.exe",
            c_parameter=1000,
            max_evaluations=200,
            max_local_search_evaluations=5,
            base_pairs=None
    ):
        # user defined, TODO: load with parameter file.
        self.target_structure = target_structure
        self.RNA = RNA # else DNA
        self.RNAfold_directory = RNAfold_directory
        self.c_parameter = c_parameter#0.1
        self.max_evaluations = max_evaluations  #alternatively time or MCTS rounds, liefst deelbaar door local search eval + 1
        self.max_local_search_evaluations = max_local_search_evaluations
        self.base_pairs = base_pairs
        if not self.base_pairs:
            self.base_pairs = {"AU":.51, "GC":.20, "UG":.10} if self.RNA else {"AT":.51, "GC":.20, "TG":.10}  #and woble base pairs "GA"and "UG"
        # standard
        self.nucleotides = ["A","C","G","U"] if self.RNA else ["A","C","G","T"]
        self.all_positions = self.get_positions()
        self.number_evaluations = 0
        self.root = Node(root=True)
        self.root.visits += 1
        self.extend(self.root)
        self.structure_memory = {} #similarities as keys.

    def run(self):
        "Runs MCTS, returns sequence, similarity, structure, number of function evaluations"
        while self.resources_left():  # tot target sequence is found]
            leaf = self.select(self.root, final=False)  # leaf = unvisited node
            similarity, sequence, predicted_structure = self.rollout(leaf)
            self.backpropagate(leaf, similarity)
            if similarity > 1:
                return sequence, similarity, predicted_structure, self.number_evaluations
        highest_similarity = max(list(self.structure_memory.keys()))
        self.rollout(self.select(self.root, final=True))
        return self.structure_memory[highest_similarity][0], highest_similarity, \
               self.structure_memory[highest_similarity][1], self.number_evaluations


    def resources_left(self):
        return self.number_evaluations < self.max_evaluations - 2*(self.max_local_search_evaluations+1)

    def select(self, node, final=False): #selection
        if not node.children:
            return node
        selected_node = self.best_child(node, final=final)
        if selected_node.children:
            return self.select(selected_node)
        else:
            self.extend(selected_node)
            return selected_node

    def extend(self, node): #add all children
        try:
            if len(node.sequence_dict.keys()) != 1:
                position = random.sample(self.all_positions - set(node.sequence_dict.keys()),1)[0]
            else:
                positions = self.all_positions.copy()
                positions.remove(list(node.sequence_dict.keys())[0])
                position = random.sample(positions, 1)[0]
        except:
            node.visits = float("Inf") # we cannot extend a leaf node with a full sequence, so we make sure it is not visited again
            print("We are trying to extend a leaf node with a full sequence. It is suboptimal that we end in this leaf")
            return
        if type(position) == tuple:
            for base_pair in self.base_pairs:
                node.add_child(position, base_pair)
                node.add_child(position, base_pair[::-1])
        else:
            for nucleotide in self.nucleotides:
                node.add_child(position, nucleotide)

    def rollout(self, node):
        sequence_dict_rollout = self.rollout_policy(node)
        similarity, i_non_aligned_nucleotides, sequence,  predicted_structure = self.evaluate(sequence_dict_rollout)

        # evt. local search, maintaing  positions of that node. while similarity !=  1.
        local_search_evaluations = 0
        while similarity != 1 and local_search_evaluations < self.max_local_search_evaluations:
            new_sequence_dict, stop_local_search = self.mutate(sequence_dict_rollout, predicted_structure,
                                                               i_non_aligned_nucleotides, node.sequence_dict)
            if stop_local_search:
                break
            new_similarity, new_i_non_aligned_nucleotides, new_sequence, new_predicted_structure = self.evaluate(new_sequence_dict)
            if new_similarity > similarity:
                sequence_dict_rollout, similarity, i_non_aligned_nucleotides, sequence, predicted_structure = \
                    new_sequence_dict, new_similarity, new_i_non_aligned_nucleotides, new_sequence, new_predicted_structure
            local_search_evaluations += 1
        self.structure_memory.update({similarity:(sequence,  predicted_structure)})
        return similarity, sequence,  predicted_structure

    def rollout_policy(self, node):
        # do thesame as in extension, but than random and do not track the node.  #50% chance to turn order around
        sequence_dict_rollout = node.sequence_dict.copy()
        while len(sequence_dict_rollout) < len(self.all_positions):
            if len(node.sequence_dict.keys()) != 1:
                position = random.sample(self.all_positions - set(sequence_dict_rollout.keys()), 1)[0]
            else:
                positions = self.all_positions.copy()
                positions.remove(list(node.sequence_dict.keys())[0])
                position = random.sample(positions, 1)[0]
            if type(position) == tuple:
                base_pair = np.random.choice(a=list(self.base_pairs.keys()),
                                             p=list(self.base_pairs.values())/
                                               np.sum(list(self.base_pairs.values())))[::random.choice([1,-1])]
            else:
                base_pair = np.random.choice(self.nucleotides)
            sequence_dict_rollout.update({position:base_pair})
        return sequence_dict_rollout

    def evaluate(self, sequence_dict_rollout):
        """Evaluate sequence by comparing predicted structure, calculated with RNAfold, with target structure"""
        self.number_evaluations += 1
        sequence = self.get_sequence(sequence_dict_rollout) # get sequence
        predicted_structure = self.call_RNAfold(sequence) # call RNAfold
        similarity, i_non_aligned_nucleotides = self.structure_similarity(predicted_structure)
        return similarity, i_non_aligned_nucleotides, sequence, predicted_structure # compare with target structure

    def backpropagate(self, node, similarity):
        if node.root: return
        node.update_stats(similarity)
        self.backpropagate(node.parent, similarity)

    def best_child(self, node, final=False):
        choices_weights = [
            (child.similarity / child.visits) + self.c_parameter * np.sqrt((np.log(node.visits) / child.visits)) # UCT
            for child in node.children
            ] #initialize visits with 1, otherwise division by zero
        if final:
            choices_weights = [(child.similarity / child.visits) for child in node.children]
        return node.children[np.argmax(choices_weights)]

    # je zou aangekomen bij de leaf node local search kunnen doen, of pas op de finale versie local search

    """Evaluation functions"""
    def call_RNAfold(self, sequence):
        """Call a ViennaRNA program in install location with list of inputs, optional dictionary of flags. Adapted from Ruben Walen"""
        fasta_directory = os.getcwd() + "\\fasta.fa"
        with open(fasta_directory, "w") as f:
            f.write(sequence)

        if not os.path.isfile(self.RNAfold_directory):
            raise ValueError("@callViennaRNAProgram: program directory not found")

        command = [self.RNAfold_directory]
        if not self.RNA:
            command.append("--paramFile=DNA")
        command.append(fasta_directory)
        return str(subprocess.run(command, stdout=subprocess.PIPE).stdout.split()[1], 'utf-8') #capture_output=True for newer version

    def structure_similarity(self, predicted_structure):
        "1 is max, 0 no similarity "
        i_non_aligned_nucleotides = set()
        for i in range(len(self.target_structure)):
            if self.target_structure[i]!= predicted_structure[i]:
                if i not in self.all_positions:
                    i = [item for item in self.all_positions if type(item) == tuple and i in item][0]
                i_non_aligned_nucleotides.add(i)
        similarity = (len(self.target_structure) - len(i_non_aligned_nucleotides))/len(self.target_structure)
        return similarity, i_non_aligned_nucleotides

    def get_sequence(self, sequence_dict):
        ordered_sequence_dict = {}
        for key, value in sequence_dict.items():
            if type(key) == tuple:
                ordered_sequence_dict.update({key[0]:value[0], key[1]:value[1]})
            else:
                ordered_sequence_dict.update({key:value})
        return "".join([value for (key, value) in sorted(ordered_sequence_dict.items())])

    """Local search"""
    # Mutations


    def mutate(self, sequence_dict_rollout, predicted_structure, i_non_aligned_nucleotides, sequence_dict_original={}):
        try:
            if len(sequence_dict_original.keys()) != 1:
                position = random.choice(list(i_non_aligned_nucleotides - set(sequence_dict_original.keys())))
            else:
                positions = i_non_aligned_nucleotides.copy()
                if list(sequence_dict_original.keys())[0] in positions:
                    positions.remove(list(sequence_dict_original.keys())[0])
                position = random.choice(list(positions))
        except IndexError:
           return {}, True
        if type(position) == tuple:
            # vermoedelijk gaat het ergens mis omdat een tuple/paired position niet meer paired is in
            alternatives = list(self.base_pairs.keys()) + [key[::-1] for key in self.base_pairs.keys()]
            alternatives.remove(sequence_dict_rollout[position])
        else:
            alternatives = self.nucleotides.copy()
            alternatives.remove(sequence_dict_rollout[position])
        sequence_dict_rollout.update({position: random.choice(alternatives)})
        return sequence_dict_rollout, False

    """PREPARE"""

    def get_positions(self):
        """Adapted from reverse MCTS RNA"""
        stack = []
        positions = set()
        for i in range(len(self.target_structure)):
            if self.target_structure[i] == '(':
                stack.append(i)
            if self.target_structure[i] == ')':
                positions.add((stack.pop(), i))
            elif self.target_structure[i]=='.':
                positions.add(i)
        return positions

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    mcts_object = MonteCarloTreeSearch()
    output = mcts_object.run()
    print(output)
    None