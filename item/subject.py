import numpy as np
import math as m


class Subject:

    def __init__(self, mutation_percentage, quantity=0, genotype=None):
        self.score = -m.inf
        self.mutual_relation = 0
        self.mutationProbability = mutation_percentage
        if genotype is None:
            self.genotype = np.random.randint(0, 2, quantity)
        else:
            self.genotype = genotype

    def mutation(self):
        i = np.random.randint(0, 100)
        if (self.mutationProbability * 100) >= i:
            i = np.random.randint(0, len(self.genotype) - 1)
            self.genotype[i] = abs(self.genotype[i] - 1)
            return True
        return False
