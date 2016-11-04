import random

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
# from mesa.datacollection import DataCollector
    
class MoneyAgent(Agent):
    def __init__(self, unique_id, model):
        Agent.__init__(self, unique_id,model)
        self.wealth = 1
    def step(self):
        print self.unique_id

class MoneyModel(Model):
    def __init__(self, N):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        
        for i in range(self.num_agents):
            self.schedule.add(MoneyAgent(i, self))
        
    def step(self):
        self.schedule.step()
        
empty_model = MoneyModel(10)
empty_model.step()