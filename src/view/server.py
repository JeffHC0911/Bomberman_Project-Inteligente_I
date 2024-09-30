from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model.model import BombermanModel
from model.agents import Bomberman, Enemy, Rock, Metal, Path

def agent_portrayal(agent):
    if isinstance(agent, Bomberman):
        portrayal = {"Shape": "resources/assets/bomberman.png", "Filled": "true", "Layer": 0, "r": 0.5}
    elif isinstance(agent, Enemy):
        portrayal = {"Shape": "circle", "Color": "red", "Filled": "true", "Layer": 0, "r": 0.5}
    elif isinstance(agent, Rock):
        portrayal = {"Shape": "resources/assets/pared.png", "Filled": "true", "Layer": 0, "w": 1, "h": 1}
    elif isinstance(agent, Metal):
        portrayal = {"Shape": "resources/assets/metal.png", "Color": "black", "Filled": "true", "Layer": 0, "w": 1, "h": 1}
    elif isinstance(agent, Path):
        portrayal = {"Shape": "rect", "Color": "green", "Filled": "true", "Layer": 0, "w": 1, "h": 1}
    return portrayal

grid = CanvasGrid(agent_portrayal, 7, 4, 350, 250)  # Ajusta el tamaño según tu mapa

server = ModularServer(
    BombermanModel, 
    [grid], 
    "Bomberman AI", 
    {
        "width": 7, 
        "height": 4, 
        "num_bombers": 0, 
        "num_enemies": 0, 
        "map_file": "resources/maps/map2.txt"
    }
)
server.port = 8521  # Puerto predeterminado para el servidor de Mesa
