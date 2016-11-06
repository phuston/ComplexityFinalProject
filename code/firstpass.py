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
	def __init__(self, unique_id, model):
		Agent.__init__(self, unique_id, model)
		self.age = random.randint(18,87)
		degredation_age = 37
		max_age = 100
		# self.ability = random.random()**4 * (((min(abs((max_age+degredation_age)-self.age)),max_age))/max_age)		#based on formula A_b on pg. 354
		self.ability = 1
		self.attitude = random.random()**3 		# based on A_t on pg. 354


class WalkingModel(Model):
	def __init__(self, N, width, height):
		self.num_agents = N
		self.schedule = RandomActivation(self)
		self.grid = MultiGrid(width, height, True)
		self.running = True
		
		# create a grid with travel(grocery, social areas), home, and work locations
		self.allLocations = {}
		num_travel = int (self.num_agents / 10) 		# number of travel locations
		num_work = int (self.num_agents / 5)		
		self.travelLocs = [(random.randint(0, width), random.randint(0, height)) for i in range(num_travel)]
		self.workLocs = [(random.randint(0, width), random.randint(0, height)) for i in range(num_work)]
		for travel in self.travelLocs:
			self.allLocations[travel]= 'travel'

		for work in self.workLocs:
			while (work[0], work[1]) not in self.allLocations.keys():
				self.allLocations[work] = 'work'

		for i in range(self.num_agents):
			homeX, homeY = random.randint(0,width), random.randint(0,height)
			while (homeX, homeY) in self.allLocations.keys():
				homeX, homeY = random.randint(0,width), random.randint(0,height)

		 	self.allLocations[(homeX, homeY)] = 'home'

			agent = WalkingAgent(i, self)
			# agent.workLocation = workLoc
			self.schedule.add(agent)
			# self.grid.place_agent(agent, homeLoc)

		homeCount = sum(loc == 'home' for loc in self.allLocations.values())
		workCount = sum(loc == 'work' for loc in self.allLocations.values())
		travelCount = sum(loc == 'travel' for loc in self.allLocations.values())

		for key, value in self.allLocations.items():
			print(key, value)
		print homeCount, workCount, travelCount
			# if self.allLocations[i] == 'work':
				# print self.allLocations.value
		# print(self.allLocations)


if __name__ == "__main__":		
	# place agents in home locations
	model = WalkingModel(50, 10, 10)