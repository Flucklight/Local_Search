import strategy.genetic_algorithm as ga

while True:
    print('Estrategia: '
          '\n\tAlgorimos geneticos'
          '\nProblemas:'
          '\n\t1) N Reinas'
          '\n\t2) Mochila'
          '\n\t3) Minimizacion de la funcion de la parabola'
          '\n\t4) Salir')
    problem = int(input('Escoja el numero del problema: '))
    if problem == 4:
        break
    else:
        ga.init(p_type=problem)
