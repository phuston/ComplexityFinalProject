from __future__ import division         #make meg's python 2 think it's python 3
import random
import pandas

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import matplotlib.pyplot as plt
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum( xi * (N-i) for i,xi in enumerate(x) ) / (N*sum(x))
    return (1 + (1/N) - 2*B)
    
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
        self.running = True
        
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)
            
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            model_reporters= {'Gini': compute_gini},
            agent_reporters= {'Wealth': lambda a: a.wealth})
        
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        

model = MoneyModel(50, 10, 10)
for i in range(100):
    model.step()

# Show a 2x2 grid where colors show number of agents present in each square
import numpy as np
agent_counts = np.zeros((model.grid.width, model.grid.height))
for cell in model.grid.coord_iter():
    cell_content, x, y = cell
    agent_count = len(cell_content)
    agent_counts[x][y]= agent_count
plt.imshow(agent_counts, interpolation="nearest")
plt.colorbar()

# Show the Gini Wealth Distribution
gini = model.datacollector.get_model_vars_dataframe()
gini.plot()
plt.show()

# Show all agents wealth as a histogram
agent_wealth = model.datacollector.get_agent_vars_dataframe()
agent_wealth.head()
end_wealth = agent_wealth.xs(99, level="Step")["Wealth"]
end_wealth.hist(bins=range(agent_wealth.Wealth.max()+1))
plt.show()

# Show a single agent's wealth over each time step
one_agent_wealth = agent_wealth.xs(14, level="AgentID")
one_agent_wealth.Wealth.plot()
plt.show()

# Use BatchRunner to run multiple instantiations at the same time
parameters = {"width" : 10,
                "height" : 10,
                "N": range(10, 500, 10)}
batch_run = BatchRunner(MoneyModel,
                        parameters,
                        iterations=5,
                        max_steps=100,
                        model_reporters={"Gini": compute_gini})
batch_run_all()
# show BatchRunner data as a scatter plot
run_data = batch_run.get_model_vars_dataframe()
run_data.head()
plt.scatter(run_data.N, run_data.Gini)
plt.show()