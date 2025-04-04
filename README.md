<div align="center">
  <h1>🎲 PyCatan Simulation & Genetic Optimization</h1>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="100" alt="python logo" />
</div>

---

## 🔍 Overview

This repository hosts a Python-based simulator for the board game **Settlers of Catan** (PyCatan). Originally designed for testing AI agents in a simulated Catan environment, this project has been extended with a **Genetic Algorithm** (using DEAP) to automatically evolve and determine which agent performs best. The simulation leverages multi-core concurrency to evaluate numerous matches in parallel for faster fitness evaluation.

---

## 🚀 Getting Started

### 🛠 Prerequisites

- **Python 3.6+**  
  Ensure you have Python installed on your machine.
- **Dependencies:**  
  The project uses several external libraries:
  - **DEAP** – for genetic algorithm functionalities.
  - **NumPy** – for numerical operations.
  - **Multiprocessing** – for concurrent simulation runs.

### 📥 Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/brivaro/GeneticAlgorithmPyCatan
   cd GeneticAlgorithmPyCatan
   ```

2. **Install Dependencies:**  
   Create a virtual environment (optional but recommended) and install the required packages (you can use conda):
   ```bash
   python -m venv venv
   source venv/bin/activate    # On macOS/Linux
   venv\Scripts\activate       # On Windows
   pip install -r requirements.txt
   ```

3. **Requirements File:**  
   Your `requirements.txt` should include the following:
   ```txt
   deap==1.3.1
   numpy==1.23.5
   ```
   These packages cover the genetic algorithm functionalities and numerical operations used in the simulation.

---

## 🎭 Adding or Modifying Agents

1. Navigate to the `Agents` folder.
2. Add your custom agent module or Python file in this folder.
3. Ensure your agent class is correctly defined (with an appropriate interface) so it can be imported and used in simulations.

---

## 🎮 Running the Simulator & Genetic Optimizer

1. **Execute the Main Script:**
   ```bash
   python catan.py
   ```
2. The genetic algorithm will run for a specified number of generations (default settings in `catan.py`), simulating several matches per evaluation. Multi-core processing is used to speed up the fitness evaluation.

3. **Output Details:**
   - **Best Individual:**  
     The optimized probability vector for agent selection.
   - **Optimized Distribution:**  
     The evolved distribution that maximizes the win rate of the optimized agent.
   - **Fitness Value:**  
     Number of wins in simulated games.
   - **Logbook:**  
     A CSV log (`evolution_log.csv`) detailing the evolution progress.

---

## 📊 Results

- **Console Output:**  
  Real-time statistics on each generation (average, min, and max fitness) and a summary when an optimal solution is found.
- **Logbook:**  
  Detailed evolution statistics stored in `evolution_log.csv`.
- **Agent Distribution:**  
  The best evolved probability vector determines which agent is selected for the simulated matches, maximizing win rate.

---

## 📝 Optimization Report

**Informe sobre la Optimización de Agentes en Catan con Algoritmos Genéticos**

1. **Código fuente del algoritmo genético y scripts de pruebas**  
   El código implementa un algoritmo genético para optimizar la selección de agentes en el juego de Catan. Utiliza la biblioteca DEAP para la evolución de individuos, donde cada individuo representa una distribución de probabilidades sobre los agentes. Se simulan partidas y se evalúa la frecuencia de victorias del agente optimizado para determinar su fitness.

2. **Logbook o registro de resultados**  
   Se ha registrado la evolución del fitness a lo largo de las generaciones en el archivo `evolution_log.csv`, que contiene los siguientes datos por generación:

   | Generación | Evaluaciones | Fitness Promedio | Fitness Mínimo | Fitness Máximo |
   |------------|--------------|------------------|----------------|----------------|
   | 0          | 50           | 4                | 1              | 8              |
   | 1          | 40           | 5.4              | 3              | 8              |
   | 2          | 41           | 5.8              | 3              | 9              |
   | 3          | 33           | 6.1              | 4              | 9              |
   | 4          | 38           | 6.0              | 4              | 8              |
   | 5          | 47           | 5.9              | 4              | 9              |

   El tiempo total de ejecución del algoritmo fue de **680.53 segundos**.

3. **Mejor individuo encontrado**  
   El mejor individuo encontrado tiene la siguiente distribución de probabilidades normalizada para la selección de agentes:

   > [0.1123, 0.0850, 0.1073, 0.1483, 0.0052, 0.0771, 0.1052, 0.1767, 0.1075, 0.0753]

   Este individuo obtuvo un fitness de **9 victorias en 10 simulaciones**, lo que sugiere que tiene una alta tasa de éxito en las partidas.

4. **Explicación de los hiperparámetros y su impacto en el rendimiento**

   | Hiperparámetro                              | Valor | Impacto                                                                 |
   |---------------------------------------------|-------|-------------------------------------------------------------------------|
   | POP_SIZE (Tamaño de población)              | 50    | Un tamaño moderado permite diversidad sin un costo computacional excesivo. |
   | N_GEN (Número de generaciones)              | 5     | Aumentar este valor podría permitir más refinamiento, pero con mayor costo de tiempo. |
   | CXPB (Probabilidad de cruce)                | 0.8   | Un valor alto fomenta la exploración de combinaciones, evitando el estancamiento. |
   | MUTPB (Probabilidad de mutación)            | 0.2   | Introduce variabilidad para evitar convergencia prematura.               |
   | N_SIM (Número de simulaciones por evaluación de fitness) | 10    | Un número bajo acelera la ejecución, pero puede generar más ruido en la evaluación.  |

**Conclusión:**  
El algoritmo encontró una solución óptima en "relativamente poco tiempo" (en mi PC de 9 años), alcanzando **9 victorias en 10 simulaciones**. Incrementar el número de generaciones o partidas simuladas podría afinar aún más la optimización, aunque con un mayor costo computacional.

Adjunto código fuente (`catan.py`) y el logbook (`evolution_log.csv`) a la entrega.

---

## 🤝 Contributing

Contributions to enhance the simulation, add new agents, or improve the genetic algorithm are welcome! Feel free to fork the repository and submit pull requests with your improvements.

---

Happy simulating and evolving your Catan strategies! 🚀


---
---
---

# Catan Simulation in Python

A Settlers of Catan simulator for AI agents written in Python.

## Overview

This repository contains a Python-based simulator for the board game Settlers of Catan. It is designed to test and refine AI agents in a simulated environment. Users can execute predefined agents, as well as introduce their own custom agents into the game.

## Getting Started

### Prerequisites

Ensure you have Python installed on your machine. The simulation is compatible with Python 3.x.

### Adding Your Agents

1. Navigate to the `Agents` folder.
2. Place your custom agent module or Python file in this folder.
3. Ensure your agent class is correctly defined within the module.

### Running the Simulator

To run the simulator, use the `main` module. Specify the agents to be executed and the number of games to be played. Each agent should be referenced by the module or file name, followed by a dot, and then the class name (e.g., `MyModule.MyClass`).

### Results

After each game, the result is displayed in the console and the game trace is saved in JSON format in the `Traces` folder.

## Visualizing Results

To visualize game results:
1. Open the `index.html` file located in the `Visualizer` folder.
2. Load a JSON trace file by clicking on the three-dot icon located in the controls below the right side of the Catan board.

<img src="assets/visualizer_screenshot.png" width="900" alt="Screenshot of the visualizer">


## Contributing

Contributions to the Catan Simulation in Python are welcome! Please feel free to make changes and submit pull requests.
