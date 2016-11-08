from __future__ import division  # Make meg's python 2 think it's python 3
import random
import pandas

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import matplotlib.pyplot as plt
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner


class WalkingAgent(Agent):
	def __init__(self, unique_id, model, homeLoc, workLoc):
		Agent.__init__(self, unique_id, model)
		self.age = random.randint(18,87)
		degredation_age = 37
		max_age = 100
		# self.ability = random.random()**4 * (((min(abs((max_age+degredation_age)-self.age)),max_age))/max_age)		#based on formula A_b on pg. 354
		self.ability = 1
		self.attitude = random.random()**3 		# based on A_t on pg. 354
		self.home = homeLoc
		self.work = workLoc


class WalkingModel(Model):
	def __init__(self, N, width, height):
		self.num_agents = N
		self.schedule = RandomActivation(self)
		self.grid = MultiGrid(width, height, True)
		self.running = True
		
		# create a grid with travel(grocery, social areas), home, and work locations
		# self.allLocations = {}
		num_travel = int (self.num_agents / 10) 		# number of travel locations
		num_work = int (self.num_agents / 5)		
		self.travelLocs = [(random.randint(0, width-1), random.randint(0, height-1)) for i in range(num_travel)]
		self.workLocs = [(random.randint(0, width-1), random.randint(0, height-1)) for i in range(num_work)]

		self.homeLocs = []
		for i in range(self.num_agents):
			homeX, homeY = random.randint(0,width-1), random.randint(0,height-1)
			while (homeX, homeY) in self.workLocs or (homeX, homeY) in self.travelLocs:		# "reroll" the home location if it already exists
				homeX, homeY = random.randint(0,width-1), random.randint(0,height-1)

			self.homeLocs.append((homeX, homeY))

			agent = WalkingAgent(i, self, self.homeLocs[i], random.choice(self.workLocs))
			self.schedule.add(agent)
			self.grid.place_agent(agent, agent.home)

		## displaying how many of each location there are
		# homeCount = len(self.homeLocs)
		# workCount = len(self.workLocs)
		# travelCount = len(self.travelLocs)
		# print(homeCount, workCount, travelCount)


if __name__ == "__main__":		
	# place agents in home locations
	model = WalkingModel(50, 10, 10)

	import numpy as np
	agent_counts = np.zeros((model.grid.width, model.grid.height))
	for cell in model.grid.coord_iter():
		cell_content, x, y = cell
		agent_count = len(cell_content)
		agent_counts[x][y]= agent_count
	plt.imshow(agent_counts, interpolation="nearest")
	plt.colorbar()
	plt.show()