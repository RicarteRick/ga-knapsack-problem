import random
import re
import time

# ao inves de trabalhar com matriz, cada item dentro da população terá um cromossomo (também uma lista, agora de 0s e 1s)
def initialize_population(population_size, itens_qtd, security_rate):
  population = []
  for _ in range(population_size):
    chromosome = []
    for _ in range(itens_qtd):
      random_number = random.randint(1,100)
      chromosome.append(1 if random_number <= security_rate else 0)
    
    population.append(chromosome)

  return population

def get_fitness_value(chromossome, vet_value, vet_weight, capacity):
  total_value = 0
  total_weight = 0

  for i in range(len(chromossome)):
    if chromossome[i] == 1:
      total_value += vet_value[i]
      total_weight += vet_weight[i]

  if total_weight > capacity:
    return 0.0001
  else:
    return total_value

def select_parents(population, vet_value, vet_weight, capacity):
  vet_parents = []
  vet_fitness = []
  # candidates_qtd = len(population) * 20 / 100

  for chromossome in population:
    fitness_val = get_fitness_value(chromossome, vet_value, vet_weight, capacity)
    vet_fitness.append(fitness_val)

  vet_parents.append(random.choices(population, weights=vet_fitness, k=1)[0])
  vet_parents.append(random.choices(population, weights=vet_fitness, k=1)[0])

  # TODO: tentar fazer torneio
  # aux_population = random.sample(population, candidates_qtd)
  return vet_parents, vet_fitness

def crossover(vet_parents, itens_qtd):
  vet_children = []

  if itens_qtd <= 3:
    cross_point = random.randint(1, itens_qtd - 1)

    vet_children.append(vet_parents[0][:cross_point] + vet_parents[1][cross_point:])
    vet_children.append(vet_parents[1][:cross_point] + vet_parents[0][cross_point:])
  else:
    cross_point_1 = random.randint(1, itens_qtd - (itens_qtd/2))
    cross_point_2 = random.randint(itens_qtd/2, itens_qtd-1)

    vet_children.append(vet_parents[0][:cross_point_1] + vet_parents[1][cross_point_1:cross_point_2] + vet_parents[0][cross_point_2:])
    vet_children.append(vet_parents[1][:cross_point_1] + vet_parents[0][cross_point_1:cross_point_2] + vet_parents[1][cross_point_2:])

  return vet_children

def mutation(child, itens_qtd):
  mutation_point = random.randint(1, itens_qtd - 1)

  child[mutation_point] = 1 if child[mutation_point] == 0 else 0

  return child

def compareParentsChildren(vet_children, vet_fitness_children, vet_parents, vet_fitness_parents):
  vet_winners = []
  vet_winners_fitness = []
  vet_all_candidates = vet_children + vet_parents
  vet_all_fitness = vet_fitness_children + vet_fitness_parents
  
  dict_infos = dict(zip(vet_all_fitness, vet_all_candidates))

  vet_all_fitness.sort(reverse=True)

  vet_winners_fitness.append(vet_all_fitness[0])
  vet_winners_fitness.append(vet_all_fitness[1])

  vet_winners.append(dict_infos[vet_all_fitness[0]])
  vet_winners.append(dict_infos[vet_all_fitness[1]])

  return vet_winners, vet_winners_fitness
  
def get_best_solution(population, vet_fitness):
  vet_fitness = [0 if val < 0.001 else val for val in vet_fitness]

  dict_infos = dict(zip(vet_fitness, population))

  max_value = max(vet_fitness)

  if max_value == 0:
    return []
  
  return dict_infos[max_value]

def knapsack_alg(vet_value, vet_weight, capacity, population_size, generation_qtd, mutation_rate, security_rate):
  itens_qtd = len(vet_value)
  population = initialize_population(population_size, itens_qtd, security_rate)
  vet_fitness = []
  best_value = 0
  best_weight = 0
  best_ids = []

  for gen in range(generation_qtd):
    vet_parents, vet_fitness = select_parents(population, vet_value, vet_weight, capacity)

    vet_children = crossover(vet_parents, itens_qtd)

    random_number_mutation = random.uniform(0,1)

    if random_number_mutation <= mutation_rate:
      vet_children[0] = mutation(vet_children[0], itens_qtd)
      vet_children[1] = mutation(vet_children[1], itens_qtd)

    vet_fitness_children = []
    vet_fitness_parents = []
    population_parents_indexes = []

    population_parents_indexes.append(population.index(vet_parents[0]))
    population_parents_indexes.append(population.index(vet_parents[1]))
    
    vet_fitness_children.append(get_fitness_value(vet_children[0], vet_value, vet_weight, capacity))
    vet_fitness_children.append(get_fitness_value(vet_children[1], vet_value, vet_weight, capacity))

    vet_fitness_parents.append(vet_fitness[population_parents_indexes[0]])
    vet_fitness_parents.append(vet_fitness[population_parents_indexes[1]])

    vet_winners, vet_winners_fitness = compareParentsChildren(vet_children, vet_fitness_children, vet_parents, vet_fitness_parents)

    population[population_parents_indexes[0]] = vet_winners[0]
    population[population_parents_indexes[1]] = vet_winners[1]

    vet_fitness[population_parents_indexes[0]] = vet_winners_fitness[0]
    vet_fitness[population_parents_indexes[1]] = vet_winners_fitness[1]

  best_solution = get_best_solution(population, vet_fitness)

  if best_solution == []:
    return [], 0, 0, []

  for i in range(len(best_solution)):
    if best_solution[i] == 1:
      best_value += vet_value[i]
      best_weight += vet_weight[i]
      best_ids.append(i+1)

  return best_solution, best_value, best_weight, best_ids

def get_input_values(file_path):
  with open(file_path, "r") as file:
    lines = file.readlines()

  capacity = int(lines[-1].strip())

  vet_value, vet_weight = [], []
  for line in lines[1:-1]:
    numbers = re.findall(r"[0-9]+", line)
    vet_value.append(int(numbers[1]))
    vet_weight.append(int(numbers[2]))

  return vet_value, vet_weight, capacity

def main():
  population_size = 100
  generation_qtd = 10000
  mutation_rate = 0.5
  security_rate = 1    # 0 - 100%
  header_line = f"Instancia;Valor;Peso;Capacidade restante;Execucao(s)\n"
  with open("output/ga.out", "a+") as output_file:
    output_file.write(header_line)

  for iterator in range(1, 5):
    start_time = time.time()

    input_file_path = f"input/input{iterator}.in"

    vet_value, vet_weight, capacity = get_input_values(input_file_path)

    best_solution, best_value, best_weight, best_ids = knapsack_alg(vet_value, vet_weight, capacity, population_size, generation_qtd, mutation_rate, security_rate)

    print("---------------------------------------")
    print("Iteracao #" + str(iterator) + ":")
    if best_solution == []:
      print('Nao foi encontrada uma solucao')
    else:
      capacity_diff = capacity - best_weight
      print("Melhor Solução:", best_solution)
      print("Valor da Solução:", best_value)
      print("Itens adicionados:", best_ids)
      print("Peso da Solução:", best_weight)
      print("Capacidade restante na mochila:", capacity_diff)
      
      execution_time = time.time() - start_time

      # coloca no arquivo qual a iteração e os valores da solucao
      output_line = f"{iterator};{best_value};{best_weight};{capacity_diff};{execution_time}\n"

      with open("output/ga.out", "a+") as output_file:
        output_file.write(output_line)

if __name__ == "__main__":
  main()
  
  # with open("output/ga.out", "a+") as output_file:
  #   output_file.write(str(execution_time)+'\n')
  # print(f"Execution time: {execution_time} seconds")
