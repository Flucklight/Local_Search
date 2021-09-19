import numpy as np
import math
from item.subject import Subject

poblacion = []
herederos = []
n_bits = 0
problem = 0
file = open('reports/test.dat')


def generate_population(gen_code_len, population, mutation_probability):
    for index in range(population):
        poblacion.append(Subject(mutation_probability, quantity=gen_code_len))


def binary_to_decimal(binary):
    value = 0
    j = len(binary) - 1
    index = 0
    for v in range(j, -1, -1):
        value += pow(2.0, index) * (binary[v])
        index += 1
    return int(value)


def genotype_to_phenotype(subject):
    phenotype = []
    if problem == 1:
        s = 0
        for index in range(1, n_bits + 1):
            e = index * int(len(subject.genotype)/n_bits)
            value = binary_to_decimal(subject.genotype[s:e])
            phenotype.append((index - 1, value))
            s = e
    return phenotype


def evaluation(poblat):
    file.write("\tEvaluacion de individuos\n")
    for subject in poblat:
        if problem == 1:
            phenotype = genotype_to_phenotype(subject)
            compare = 1
            review = 0
            for data in phenotype:
                for index in range(compare, len(phenotype)):
                    if data[1] == phenotype[index][1]:
                        review += 1
                    elif (data[0] - data[1]) == (phenotype[index][0] - phenotype[index][1]):
                        review += 1
                    elif (data[0] + data[1]) == (phenotype[index][0] + phenotype[index][1]):
                        review += 1
                compare += 1
            subject.score = review
            file.write('\t\tEvaluacion del individuo {}\n'.format(subject.genotype))
            r = 1
            for data in phenotype:
                file.write('\t\t\tReina {} en la posicion ({}, {})\n'.format(r, data[0], data[1]))
                r += 1
            file.write('\t\tCalificacion = {}\n'.format(review))


def selection(poblat):
    file.write("Seleccion de individuos\n")
    total = 0
    evaluation(poblat)
    for subject in poblat:
        total += subject.score
    for subject in poblat:
        rm = subject.score / total
        subject.mutual_relation = rm
        file.write('\tRelacion Mutua del Individuo {} es = {}\n'.format(subject.genotype, rm))


def mutate(poblat):
    file.write('Mutacion\n')
    for subject in poblat:
        tmp = subject.genotype.copy()
        if subject.mutation():
            file.write('\tEl individuo {} muto a {}\n'.format(tmp, subject.genotype))


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


def reinsertion(poblat, herd, elit):
    file.write("Reinsercion\n")
    for index in range(int(elit * len(poblat))):
        tmp = poblat[0]
        for subject in poblat:
            if tmp.mutual_relation > subject.mutual_relation:
                tmp = subject
        herd.append(tmp)
        poblat.remove(tmp)
        file.write('\tEl individuo {} destaco de los demas con una relacion mutua de {}\n'
              .format(tmp.genotype, tmp.mutual_relation))
    poblat.clear()
    for subject in herd:
        poblat.append(subject)
    herd.clear()


def elite(poblat):
    tmp = poblat[0]
    file.write('Elitismo\n')
    for subject in poblat:
        if tmp.mutual_relation > subject.mutual_relation:
            tmp = subject
    file.write('\tIndividuo con mejor resultado fue {} con calificacion de {}\n'
          .format(tmp.genotype, tmp.score))
    return tmp


def start(gen_code_len=32, population=50, mutation_percentage=.2,
          elitism=.4, genetic_merch=.5, percentage_newcomers=.6):
    i = 1
    generate_population(gen_code_len, population, mutation_percentage)
    if problem == 1:
        global file
        with open('reports/N_Queens.txt', 'w') as file:
            while True:
                file.write("<-------------------------------------------------------------------------------------->\n")
                file.write('Generacion {}\n'.format(i))
                for ind in poblacion:
                    file.write('\t{}\n'.format(ind.genotype))
                selection(poblacion)
                best_subject = elite(poblacion)
                if best_subject.score == 0:
                    break
                file.write('Herederos\n')
                while len(herederos) < (len(poblacion) * percentage_newcomers):
                    ind_a = poblacion[np.random.randint(0, len(poblacion) - 1)]
                    ind_b = poblacion[np.random.randint(0, len(poblacion) - 1)]
                    cross(ind_a, ind_b, genetic_merch, herederos)
                reinsertion(poblacion, herederos, elitism)
                mutate(poblacion)
                i += 1
            phenotype = genotype_to_phenotype(best_subject)
            file.write('Solucion\n')
            file.write('\tIndividuo {}\n'.format(best_subject.genotype))
            r = 1
            for data in phenotype:
                file.write('\t\tReina {} en la posicion ({}, {})\n'.format(r, data[0], data[1]))
                r += 1
        file.close()


def init(p_type=1, n=8):
    global problem
    problem = p_type
    global n_bits
    n_bits = n
    if problem == 1:
        index = 0
        tmp = 0
        while tmp <= n_bits:
            tmp += math.pow(2.0, index)
            index += 1
        start(gen_code_len=n_bits * (index - 1))
