import random

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
# from mesa.datacollection import DataCollector

COOPERATE = -1
DEFECT = -2
    
class CommunicationAgent(Agent):
    
    def __init__(self, unique_id, model, fsm_size, num_tokens):
        Agent.__init__(self, unique_id, model)
        # self.state = state
        self.unique_id = unique_id
        self.fsm_size = fsm_size
        self.num_tokens = num_tokens
        
        self.gen_automata(fsm_size, num_tokens)
        
    def gen_automata(self, fsm_size, num_tokens):
        #map current state to action; 50% chance of choosing a token to send, 50% of choosing cooperate/defect
        action_map = {}
        # decision_flag = 0
        for state in range(fsm_size):
            flip = random.random()
            if (flip < 0.5):
                action_map[state] = random.randint(1, num_tokens)
            else: 
                action_map[state] = random.choice([COOPERATE, DEFECT])

        #map from tuple (current state, received communication) to the next state
        transition_table = dict.fromkeys([(state, received_token) for state in range(fsm_size) for received_token in range(num_tokens)])
        for pair in transition_table.keys():
            transition_table[pair] = random.randint(1, fsm_size)
            
        print(action_map)
        print(transition_table)

    def get_state(self):
        return self.state
        
    def set_state(self, state):
        self.state = state
    
    def step(self):
        print(self.unique_id)

class CommunicationModel(Model):
    def __init__(self, N, max_chat, fsm_size, num_tokens):      #fsm_size is number of states, num_tokens is complexity of language
        
        # TODO: Create agents
        # TODO: take in params - max_chat, fsm_size, num_tokens
        
        self.num_agents = N
        self.max_chat = max_chat
        self.fsm_size = fsm_size
        self.num_tokens = num_tokens
        self.schedule = RandomActivation(self)
        
        for i in range(self.num_agents):
            self.schedule.add(CommunicationAgent(i, self, fsm_size, num_tokens))

    def run_one_round(self, agent1, agent2):
        # if agent1.state && agent2.state == 0:
            # run
        pass
 
    def step(self):
        self.schedule.step()

if __name__ == '__main__':
    communicationModel = CommunicationModel(1, 3, 3, 3)