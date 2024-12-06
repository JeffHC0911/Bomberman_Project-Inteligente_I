import os
import tkinter as tk
from tkinter import filedialog
from mesa.visualization.ModularVisualization import ModularServer
from models.model import model
from agents.bomberman import bomberman
from agents.metal import metal
from agents.salida import salida
from agents.grass import grass
from agents.rock import rock
from agents.enemy import enemy
from agents.bomb import bomb
from agents.item import item
from agents.explosion import explosion
from mesa.visualization.modules import CanvasGrid
from mesa.visualization import Choice
from utils.load import load

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
MAP_DIR = "maps/"
DEFAULT_ALGORITHM = "BFS"
DEFAULT_PRIORITY = "← ↑ → ↓"
DEFAULT_HEURISTIC = "Manhattan"

def get_map_file_path():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        initialdir=MAP_DIR, title="Seleccione un archivo de mapa", filetypes=[("Text Files", "*.txt")]
    )


def load_map_dimensions(file_path):
    if not file_path:
        print("No se seleccionó ningún archivo de mapa.")
        exit()
    map_file_name = os.path.basename(file_path)
    width, height = load.get_map_dimensions(f"{MAP_DIR}/{map_file_name}")
    rocks = load.get_rock_positions(file_path)
    return map_file_name, width, height, rocks

map_file_path = get_map_file_path()
map_file_name, width, height, rocks = load_map_dimensions(map_file_path)

def create_simulation_params(width, height, map_file_name):
    return {
        "number_of_agents": 1,
        "width": width,
        "height": height,
        "map_file": map_file_name,
        "algorithm": Choice(
            name='Método de búsqueda',
            description="Seleccione el método de búsqueda para llegar a la meta",
            choices=["BFS", "DFS", "UC", "A*", "Hill Climbing", "Beam Search", "MinMax1", "MinMax2"],
            value=DEFAULT_ALGORITHM
        ),
        "priority": Choice(
            name='Prioridad de búsqueda',
            description="Seleccione el orden de prioridad de búsqueda que tendrá el agente",
            choices=[
                "→ ↓ ↑ ←", "→ ↑ ← ↓", "↑ → ← ↓", "↑ ← ↓ →", 
                "↓ ↑ → ←", "↓ ← → ↑", "← → ↓ ↑", "← ↓ ↑ →",
                "← ↑ → ↓"
            ],
            value=DEFAULT_PRIORITY
        ),
        "heuristic": Choice(
            name='Heuristica',
            description="Selecciona la heuristica para algoritmos informados",
            choices= ["Manhattan", "Euclidiana"],
            value=DEFAULT_HEURISTIC
        ),
        "goal_pos": Choice(
            name = "Posición de la meta",
            description= "Selecciona en que lugar se va a encontrar la meta",
            choices = rocks + ["Aleatorio"],
            value = "Aleatorio"
        ),
        "difficulty": Choice(
            name = "Escoger dificultad",
            description="Se escoge el nivel de dificultad de juego",
            choices= [1, 2, 3],
            value = 1
        )
    }


def agent_portrayal(agent):
    portrayal_map = {
        metal: {"Shape": "images/metal2.png", "Layer": 3, "w": 1, "h": 1,},
        rock: lambda a: {"Shape": "images/pared.png", "Layer": 1, "w": 1, "h": 1, "text": a.label},
        bomberman: {"Shape": "images/bomberman.png", "Layer": 1,},
        enemy: {"Shape": "images/enemigo.png", "Layer": 1},
        salida: {"Shape": "images/salida.png", "Layer": 1, "w": 1, "h": 1},
        bomb: {"Shape": "images/bomba.png", "Layer": 1, "w": 1, "h": 1},
        item: {"Shape": "images/comodin.png", "Layer":1, "w":1, "h":1},
        explosion : {"Shape": "images/explosion.png", "Layer": 2, "w": 1, "h": 1},
        grass: lambda a: {
            "Shape": "images/camino1.png",
            "Layer": 1, "w": 1, "h": 1, "text": a.label, "text_color": "black",
        }
    }

    agent_type = type(agent)
    if agent_type in portrayal_map:
        portrayal = portrayal_map[agent_type]
        return portrayal(agent) if callable(portrayal) else portrayal

grid = CanvasGrid(agent_portrayal, width, height, CANVAS_WIDTH, CANVAS_HEIGHT)
simulation_params = create_simulation_params(width, height, map_file_name)
server = ModularServer(model, [grid], "Bomberman", model_params=simulation_params)
server.port = 8521
server.launch()

