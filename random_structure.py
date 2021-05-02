# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 14:26:04 2021

@author: thven
"""

import numpy as np

def create_random_structure(length=100):
    structure = ''
    p = np.random.uniform(0,1)
    while len(structure) < length:
        unfair_coin_flip = np.random.binomial(n=1,p=p)
        if unfair_coin_flip == 0 or len(structure) == length - 1:
            fair_coin_flip = np.random.binomial(n=1,p=0.5)
            if fair_coin_flip == 0:
                structure = structure + '.'
            else:
                structure = '.' + structure
        else:
            structure = '(' + structure + ')'
    assert len(structure) == length, 'structure does not have right length.'
    return structure
    
if __name__ == '__main__':
    print(create_random_structure())