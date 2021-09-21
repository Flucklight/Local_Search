import numpy as np
import math
from item.subject import Subject

file = open('reports/test.dat')
best_subject = Subject(0, 0)
poblacion = []
items = []
n_bits = 0
knapsack_weight = 0
problem = 0


def generate_population(gen_code_len, population, mutation_probability):
    for index in range(population):
        poblacion.append(Subject(mutation_probability, quantity=gen_code_len))


def binary_to_decimal(binary, negative=False):
    value = 0
    j = len(binary) - 1
    index = 0
    for v in range(j, -1, -1):
        if v == 0 and negative:
            if binary[v] == 1:
                value = -value
        else:
            value += pow(2.0, index) * (binary[v])
            index += 1
    return int(value)


def genotype_to_phenotype(subject):
    phenotype = []
    if problem == 1 or problem == 3:
        s = 0
        for index in range(1, n_bits + 1):
            e = index * int(len(subject.genotype)/n_bits)
            if problem == 1:
                value = binary_to_decimal(subject.genotype[s:e])
                phenotype.append((index - 1, value))
            elif problem == 3:
                value = binary_to_decimal(subject.genotype[s:e], negative=True)
                phenotype.append(value)
            s = e
    elif problem == 2:
        index = 0
        for item in subject.genotype:
            if item == 1:
                phenotype.append(items[index])
            index += 1
    return phenotype


def evaluation(poblat):
    file.write("\tEvaluacion de individuos\n")
    total = 0
    for subject in poblat:
        phenotype = genotype_to_phenotype(subject)
        review = 0
        weight = 0
        index = 0
        compare = 1
        for data in phenotype:
            if problem == 1:
                if data[1] >= n_bits:
                    review += int(math.pow(n_bits, 2.0))
                for index in range(compare, len(phenotype)):
                    if data[1] == phenotype[index][1]:
                        review += 1
                    elif (data[0] - data[1]) == (phenotype[index][0] - phenotype[index][1]):
                        review += 1
                    elif (data[0] + data[1]) == (phenotype[index][0] + phenotype[index][1]):
                        review += 1
                compare += 1
            elif problem == 2:
                weight += data[1]
                if weight > knapsack_weight:
                    review = 0
                    break
                review += data[0]
            elif problem == 3:
                if index == 0:
                    if data < -5:
                        review += int(math.pow(2.0, 32.0))
                    else:
                        review += int(math.pow(data, 2.0))
                else:
                    if data > 5:
                        review += int(math.pow(2.0, 32.0))
                    else:
                        review += int(math.pow(data, 2.0))
                index = 1
        subject.score = review
        total += review
        file.write('\t\tEvaluacion del individuo {}\n'.format(subject.genotype))
        n = 1
        for data in phenotype:
            if problem == 1:
                file.write('\t\t\tReina {} en la posicion ({}, {})\n'.format(n, data[0], data[1]))
            elif problem == 2:
                file.write('\t\t\tObjeto {} con valor {}, peso {}\n'.format(n, data[0], data[1]))
            elif problem == 3:
                if n == 1:
                    file.write('\t\t\tEl valor en X = {}\n'.format(data))
                else:
                    file.write('\t\t\tEl valor en Y = {}\n'.format(data))
            n += 1
        file.write('\t\tCalificacion = {}\n'.format(review))
    return total


def selection(poblat, elitism):
    file.write("Seleccion de individuos\n")
    total = evaluation(poblat)
    for subject in poblat:
        if total != 0:
            rm = subject.score / total
            subject.mutual_relation = rm
            file.write('\tRelacion Mutua del Individuo {} es = {}\n'.format(subject.genotype, rm))
        else:
            subject.mutual_relation = 0
    if total == 0:
        file.write('\tTodos los individuos fracasaron\n')
    reinsertion(poblat, elitism)


def get_mutual_relation(subject):
    return subject.mutual_relation


def reinsertion(poblat, elit):
    file.write("Reinsercion\n")
    heir = []
    if problem == 1 or problem == 3:
        poblat.sort(key=get_mutual_relation)
    elif problem == 2:
        poblat.sort(key=get_mutual_relation, reverse=True)
    for index in range(int(elit * len(poblat))):
        tmp = poblat[0]
        heir.append(tmp)
        poblat.remove(tmp)
        file.write('\tEl individuo {} destaco de los demas con una relacion mutua de {}\n'
              .format(tmp.genotype, tmp.mutual_relation))
    poblat.clear()
    for subject in heir:
        poblat.append(subject)


def elite(poblat):
    tmp = poblat[0]
    file.write('Elitismo\n')
    file.write('\tIndividuo con mejor resultado fue {} con calificacion de {}\n'
               .format(tmp.genotype, tmp.score))
    if best_subject.score == -math.inf:
        return tmp
    if (problem == 1 or problem == 3) and tmp.score < best_subject.score or \
            problem == 2 and tmp.score > best_subject.score:
        return tmp
    else:
        return best_subject


def cross(subject_a, subject_b, percentage, herd):
    index = int(percentage * len(subject_a.genotype))
    gen_a = subject_a.genotype[:index]
    gen_b = subject_b.genotype[index:]
    gen = np.concatenate((gen_a, gen_b), axis=0)
    new = Subject(subject_a.mutationProbability, genotype=gen)
    herd.append(new)
    gen_a = subject_a.genotype[index:]
    gen_b = subject_b.genotype[:index]
    gen = np.concatenate((gen_b, gen_a), axis=0)
    new2 = Subject(subject_b.mutationProbability, genotype=gen)
    herd.append(new)
    file.write('\tNuevos individuos nacidos de {} y {}.\n\t\tLos individuos son {} y {}\n'
          .format(subject_a.genotype, subject_b.genotype, new.genotype, new2.genotype))


def mutate(poblat):
    file.write('Mutacion\n')
    for subject in poblat:
        tmp = subject.genotype.copy()
        if subject.mutation():
            file.write('\tEl individuo {} muto a {}\n'.format(tmp, subject.genotype))


def start(gen_code_len=32, generations=100, population=10, mutation_percentage=.2,
          elitism=.4, genetic_merch=.5, percentage_newcomers=.6):
    i = 1
    global file, best_subject
    generate_population(gen_code_len, population, mutation_percentage)
    if problem == 1:
        file = open('reports/N_Queens.txt', 'w')
    elif problem == 2:
        file = open('reports/Knapsack.txt', 'w')
    elif problem == 3:
        file = open('reports/Parable.txt', 'w')
    while True:
        file.write("<-------------------------------------------------------------------------------------->\n")
        file.write('Generacion {}\n'.format(i))
        for ind in poblacion:
            file.write('\t{}\n'.format(ind.genotype))
        selection(poblacion, elitism)
        best_subject = elite(poblacion)
        if (problem == 1 or problem == 3) and best_subject.score == 0:
            break
        elif problem == 2 and i == generations:
            break
        file.write('Herederos\n')
        for index in range(0, int(population * percentage_newcomers), 2):
            ind_a = poblacion[np.random.randint(0, len(poblacion) - 1)]
            ind_b = poblacion[np.random.randint(0, len(poblacion) - 1)]
            cross(ind_a, ind_b, genetic_merch, poblacion)
        mutate(poblacion)
        i += 1
    phenotype = genotype_to_phenotype(best_subject)
    file.write('Solucion\n')
    file.write('\tIndividuo {}\n'.format(best_subject.genotype))
    n = 1
    for data in phenotype:
        if problem == 1:
            file.write('\t\tReina {} en la posicion ({}, {})\n'.format(n, data[0], data[1]))
        elif problem == 2:
            file.write('\t\t\tObjeto {} con valor {}, peso {})\n'.format(n, data[0], data[1]))
        n += 1
    file.close()


def init(p_type=1, n=8, path='data/ks_4_0'):
    global problem
    global n_bits
    global items
    global knapsack_weight
    problem = p_type
    if problem == 1:
        index = 0
        n_bits = n
        tmp = 0
        while tmp < n_bits:
            tmp += math.pow(2.0, index)
            index += 1
        start(gen_code_len=n_bits * index)
    elif problem == 2:
        with open(path, 'r') as doc:
            data = doc.readline()[:-1].split(' ')
            n_bits = int(data[0])
            knapsack_weight = int(data[1])
            for line in doc:
                data = line[:-1].split(' ')
                items.append((int(data[0]), int(data[1])))
            start(gen_code_len=n_bits)
    elif problem == 3:
        n_bits = 2
        start(gen_code_len=n_bits*16)
