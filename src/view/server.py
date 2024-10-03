import os
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization import Slider, StaticText, ChartModule, Choice
from model.model import BombermanModel
from model.agents import Bomberman, Enemy, Rock, Metal, Path, Meta

def agent_portrayal(agent):
    if isinstance(agent, Bomberman):
        return {"Shape": "resources/assets/bomberman.png", "Layer": 2, "scale": 0.9}
    elif isinstance(agent, Enemy):
        return {"Shape": "circle", "Color": "red", "Filled": "true", "Layer": 2, "r": 0.5}
    elif isinstance(agent, Rock):
        return {"Shape": "resources/assets/pared.png", "Layer": 1, "scale": 0.9}
    elif isinstance(agent, Metal):
        return {"Shape": "resources/assets/metal.png", "Layer": 1, "scale": 0.9}
    elif isinstance(agent, Meta):
        return {"Shape": "resources/assets/exit.png", "Layer": 1, "scale": 0.9}
    elif isinstance(agent, Path):
        return {"Shape": "rect", "Color": "green", "Filled": "true", "Layer": 0, "w": 1, "h": 1}
    return {}

def get_map_files():
    map_dir = "resources/maps/"
    return [f for f in os.listdir(map_dir) if f.endswith('.txt')]

map_files = get_map_files()
default_map = map_files[0] if map_files else "map1.txt"

# Función para obtener dimensiones del mapa
def get_map_dimensions(map_file):
    with open(os.path.join("resources/maps/", map_file), 'r') as f:
        lines = f.readlines()
        height = len(lines)
        width = len(lines[0].strip())
    return width, height

# Obtener dimensiones del mapa por defecto
default_width, default_height = get_map_dimensions(default_map)

grid = CanvasGrid(agent_portrayal, 7, 4, 400, 400)  # Ajusta el tamaño según tu mapa

server = ModularServer(
    BombermanModel, 
    [grid], 
    "Bomberman AI", 
    {
        "width": 7, 
        "height": 4, 
        "num_bombers": 0, 
        "num_enemies": 0, 
        "map_file": Choice(name='Seleccionar mapa', value='resources/maps/map1.txt', choices=['resources/maps/map1.txt', 'resources/maps/map2.txt'], description='Seleccionar mapa'),
    }
)

server.port = 8521  # Puerto predeterminado para el servidor de Mesa
