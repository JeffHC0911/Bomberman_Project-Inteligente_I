import os
import tkinter as tk
from tkinter import filedialog
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization import Choice
from model.model import BombermanModel
from model.agents.bomberman import Bomberman
from model.agents.enemy import Enemy
from model.agents.rock import Rock
from model.agents.metal import Metal
from model.agents.path import Path
from model.agents.meta import Meta
from model.agents.bomb import Bomb
from model.agents.explosion import Explosion

# Función para cargar el archivo del mapa utilizando tkinter
def get_map_file_path():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        initialdir="resources/maps/", title="Elige un mapa", filetypes=[("Text Files", "*.txt")]
    )

# Función para obtener las dimensiones del mapa
def get_map_dimensions(map_file):
    with open(map_file, "r") as f:
        lines = f.readlines()
        height = len(lines)  # Número de líneas es la altura
        width = len(lines[0].strip().split(",")) if height > 0 else 0  # Longitud de la primera línea es el ancho
    return width, height

# Función para cargar el mapa y obtener las dimensiones
def load_map_dimensions():
    map_file_path = get_map_file_path()
    if not map_file_path:
        print("No se seleccionó ningún archivo de mapa.")
        exit()
    width, height = get_map_dimensions(map_file_path)
    return map_file_path, width, height

# Definir la representación de los agentes
def agent_portrayal(agent):
    portrayal = {}
    if isinstance(agent, Bomberman):
        portrayal = {"Shape": "resources/assets/bomberman.png", "Layer": 2, "scale": 1}
    elif isinstance(agent, Enemy):
         portrayal = {"Shape": "resources/assets/enemigo.png", "Layer": 2, "scale": 1}
    elif isinstance(agent, Rock):
        portrayal = {"Shape": "resources/assets/pared.png", "Layer": 1, "scale": 1}
    elif isinstance(agent, Metal):
        portrayal = {"Shape": "resources/assets/metal2.png", "Layer": 1, "scale": 1}
    elif isinstance(agent, Meta):
        portrayal = {"Shape": "resources/assets/salida.png", "Layer": 1, "scale": 1}
    elif isinstance(agent, Path):
        portrayal = {"Shape": "resources/assets/camino1.png", "Layer": 1, "scale": 1}
        portrayal["text"] = str(agent.label) if agent.label is not None else ""
        portrayal["text_color"] = "black"
    elif isinstance(agent, Bomb):
        portrayal = {"Shape": "resources/assets/bomba.png", "Layer": 1, "scale": 1}
    elif isinstance(agent, Explosion):
        portrayal = {"Shape": "resources/assets/explosion.png", "Layer": 1, "scale": 1}
    return portrayal

# Cargar el mapa por defecto y obtener sus dimensiones
default_map_file_path, default_width, default_height = load_map_dimensions()

# Inicializar la grilla con el mapa por defecto
grid = CanvasGrid(agent_portrayal, default_width, default_height, 500, 500)

# Configurar el servidor
server = ModularServer(
    BombermanModel,
    [grid],
    "Bomberman AI",
    {
        "width": default_width,
        "height": default_height,
        "num_bombers": 0,
        "num_enemies": 1,
        "algorithm": Choice(name='Seleccionar algoritmo', value='A*', choices=['BFS', 'DFS', 'UCS', 'HCS', 'A*', 'BS'], description='Seleccionar algoritmo de búsqueda'),
        "priority": Choice(name='Seleccionar prioridad', value='Izq Arr Der Aba', choices=["Der Aba Arr Izq", "Der Arr Izq Aba", "Arr Der Izq Aba", "Izq Der Aba Arr", "Izq Arr Der Aba"], description='Seleccionar prioridad de movimiento'),
        "heuristic": Choice(name='Seleccionar heuristica', value='Manhattan', choices=['Manhattan', 'Euclidean'], description='Seleccionar heurística '),
        "map_file": default_map_file_path
    }
)

server.port = 8522  # Puerto predeterminado para el servidor de Mesa