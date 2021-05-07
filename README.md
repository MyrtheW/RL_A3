# Reinforcement Learning Assignment 3
Implementation of Monte Carlo Tree Search for the inverse RNA and DNA folding problem. 


## Table of contents
* [General info](#general-info)
* [Dependencies](#dependencies)
* [Usage](#usage)
* [Mainfunction](#mainfunction)
* [References](#references)

## General info
The project was done in the context of the Reinforcement Learning course at Leiden University. We refer to our report for more information on the project. The code is written in Python 3.

## Dependencies

The algorithm depends on the RNAfold programme of the ViennaRNA. The executables can be installed via the binaries available [online](https://www.tbi.univie.ac.at/RNA/#binary_packages). 
The link to the directory of the RNAfold.exe should be provided as input to the algorithm.

Next to the standard library, the following packages are used in the main code:

- numpy

And the following libraries for the experiments: 
- matplotlib



## Usage
To run the algorithm, set the parameters in the `config.txt` file and run the `run_example` file. Especially the target structure and directory location are required. 

### Experiments
- `experiment_learning_behaviour.py` was used to test MCTS against local search. 
- `grid_search.py` was used to find the optimal Cp parameter for different number of evaluations and sequence lenghts
- `grid_search_decay.py` runs a grid search experiment for the decay parameter.
- `grid_search_analysis.py` and `grid_search_decay_analysis.py` were used to plot graphs of the grid search results stored in `grid_search_values` and `grid_search_decay_values`.
- `experiment_create_targets.py` was used to create random sequences of different length, 
  of which the structures were predicted by RNAfold. 
  These structures are stored in `target_structures` and used as targets for testing the MCTS algorithm. 


## References
The code is inspired by several sources on the internet, which are cited in the report. 