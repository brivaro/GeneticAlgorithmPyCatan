import random
import time
import numpy as np
import os
import csv
import multiprocessing
from deap import base, creator, tools, algorithms

# Importación de los agentes
from Agents.RandomAgent import RandomAgent as ra
from Agents.AdrianHerasAgent import AdrianHerasAgent as aha
from Agents.AlexPastorAgent import AlexPastorAgent as apa
from Agents.AlexPelochoJaimeAgent import AlexPelochoJaimeAgent as apja
from Agents.CarlesZaidaAgent import CarlesZaidaAgent as cza
from Agents.CrabisaAgent import CrabisaAgent as ca
from Agents.EdoAgent import EdoAgent as ea
from Agents.PabloAleixAlexAgent import PabloAleixAlexAgent as paaa
from Agents.SigmaAgent import SigmaAgent as sa
from Agents.TristanAgent import TristanAgent as ta

# Repo de Catan
from Managers.GameDirector import GameDirector

# Lista de agentes
AGENTS = [ra, aha, apa, apja, cza, ca, ea, paaa, sa, ta]

# Parámetros del algoritmo genético y de la simulación
POP_SIZE = 50         # Tamaño de la población
N_GEN = 5             # Número de generaciones
CXPB = 0.8            # Probabilidad de cruce
MUTPB = 0.2           # Probabilidad de mutación
N_SIM = 10            # Número de partidas simuladas por evaluación de fitness

# Función para normalizar un vector (la suma será 1)
def normalize(individual):
    s = sum(individual)
    if s == 0:
        return [1.0 / len(individual)] * len(individual)
    return [x / s for x in individual]

# Función para crear un individuo ya normalizado
def create_normalized_individual():
    ind = [random.random() for _ in range(len(AGENTS))]
    return creator.Individual(normalize(ind))

# Configuración de DEAP
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Se utiliza la función personalizada para crear individuos
toolbox.register("individual", create_normalized_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalCatan(individual):
    """
    Función de evaluación: simula N_SIM partidas.
    En cada partida se selecciona el agente optimizado según la distribución
    definida en el individuo y se enfrentan a 3 oponentes elegidos al azar.
    Si el agente optimizado (ubicado en la posición 0) gana la partida,
    se suma una victoria.
    """
    # Aseguramos que los valores sean no negativos y normalizamos para obtener probabilidades
    arr = np.array(individual)
    arr[arr < 0] = 0
    if arr.sum() == 0:
        probs = np.ones_like(arr) / len(arr)
    else:
        probs = arr / arr.sum()

    wins = 0
    for _ in range(N_SIM):
        # Seleccionar el agente optimizado según la distribución de probabilidades
        chosen_agent = np.random.choice(AGENTS, p=probs)
        # Seleccionar 3 oponentes de forma equiprobable (sin incluir al agente elegido)
        other_agents = [agent for agent in AGENTS if agent != chosen_agent]
        opponents = random.sample(other_agents, 3)
        
        # Construir la lista de agentes para la partida, colocando al agente optimizado en la posición 0
        game_agents = [chosen_agent] + opponents
        
        try:
            game_director = GameDirector(agents=game_agents, max_rounds=200, store_trace=False)
            game_trace = game_director.game_start(print_outcome=False)
        except Exception as e:
            print(f"Error en la simulación: {e}")
            continue
        
        # Análisis de resultados (los jugadores se etiquetan como "J0", "J1", etc.)
        try:
            last_round = max(game_trace["game"].keys(), key=lambda r: int(r.split("_")[-1]))
            last_turn = max(game_trace["game"][last_round].keys(), key=lambda t: int(t.split("_")[-1].lstrip("P")))
            victory_points = game_trace["game"][last_round][last_turn]["end_turn"]["victory_points"]
            winner = max(victory_points, key=lambda player: int(victory_points[player]))
            if winner == "J0":  # Si gana el jugador J0 (el optimizado)
                wins += 1
                #print("Gana")
        except Exception as e:
            print(f"Error al analizar el resultado: {e}")
            continue

    return wins,

toolbox.register("evaluate", evalCatan)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    random.seed(42)
    pop = toolbox.population(n=POP_SIZE)
    
    # Creamos el pool para paralelizar SOLO la fitness
    #print(os.cpu_count()) # Número de núcleos (tengo 8)
    pool = multiprocessing.Pool(processes=6)
    
    start_time = time.time()
    
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)
    
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + stats.fields
    record = stats.compile(pop)
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    print(logbook.stream)
    
    for gen in range(1, N_GEN + 1):
        # Aplicar operadores de variación (cruce y mutación)
        offspring = algorithms.varAnd(pop, toolbox, cxpb=CXPB, mutpb=MUTPB)
        
        # Evaluación en paralelo SOLO para la función de evaluación
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        pop = toolbox.select(offspring, k=len(offspring))
        hof.update(pop)
        
        record = stats.compile(pop)
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        print(logbook.stream)
        
        # Si se alcanza el máximo posible (gana en todas las simulaciones), se para la evolución
        if hof[0].fitness.values[0] == N_SIM:
            print(f"Solución óptima encontrada en la generación {gen}")
            break

    print("Tiempo de ejecución:", time.time() - start_time)
    print("Mejor individuo (vector sin normalizar):", hof[0])
    
    # Normalizamos el mejor individuo para obtener la distribución de probabilidades final
    best_arr = np.array(hof[0])
    best_arr[best_arr < 0] = 0
    if best_arr.sum() == 0:
        best_probs = np.ones_like(best_arr) / len(best_arr)
    else:
        best_probs = best_arr / best_arr.sum()
    print("Distribución de probabilidades optimizada:", best_probs)
    print("Fitness (número de victorias en", N_SIM, "simulaciones):", hof[0].fitness.values[0])

    # Guardar el logbook en CSV
    csv_filename = "evolution_log.csv"
    with open(csv_filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=logbook.header)
        writer.writeheader()
        for record in logbook:
            writer.writerow(record)
    print(f"Logbook guardado en {csv_filename}")
    
    pool.close()
    pool.join()
    return pop, logbook, hof

if __name__ == "__main__":
    main()
