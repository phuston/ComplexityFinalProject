import random

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import matplotlib.pyplot as plt
# from mesa.datacollection import DataCollector
    
class MoneyAgent(Agent):
    def __init__(self, unique_id, model):
        Agent.__init__(self, unique_id,model)
        self.wealth = 1
    
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
    
    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = random.choice(cellmates)
            other.wealth += 1
            self.wealth -= 1
    
    def step(self):
        self.move()
        if self.wealth > 0:
            self.give_money()

class MoneyModel(Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, True)
        
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)
            
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        
    def step(self):
        self.schedule.step()
        
## from MoneyModel import MoneyModel
# empty_model = MoneyModel(10)
# empty_model.step()

# agent_wealth = [a.wealth for a in empty_model.schedule.agents]
# plt.hist(agent_wealth)
# plt.show()
# print agent_wealth

model = MoneyModel(50, 10, 10)
for i in range(20):
    model.step()

import numpy as np
agent_counts = np.zeros((model.grid.width, model.grid.height))
for cell in model.grid.coord_iter():
    cell_content, x, y = cell
    agent_count = len(cell_content)
    agent_counts[x][y]= agent_count
plt.imshow(agent_counts, interpolation="nearest")
plt.colorbar()
plt.show()