from mesa import Agent
from model.agents.wildcard import Wildcard
import random

class Rock(Agent):
    def __init__(self, unique_id, model, is_exit=False):
        super().__init__(unique_id, model)
        self.is_exit = is_exit
        self.comodin_asociado = None  # Referencia al comodín asociado
