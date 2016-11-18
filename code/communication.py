import random, copy, itertools
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
# from mesa.datacollection import DataCollector

COOPERATE = -1
DEFECT = -2
NO_ACTION = -3
payout = {(COOPERATE,COOPERATE):(5,5), (COOPERATE,DEFECT):(0,5), (COOPERATE,NO_ACTION):(2,-5), (COOPERATE,NO_ACTION):(2,-5), (DEFECT,COOPERATE):(5,0), (DEFECT,DEFECT):(1,1), (DEFECT,NO_ACTION):(2,-5), (NO_ACTION,NO_ACTION):(-5,-5), (NO_ACTION,COOPERATE):(-5,2), (NO_ACTION,DEFECT):(-5,2)}

    
class CommunicationAgent(Agent):
    
    def __init__(self, unique_id, model, fsm_size, num_tokens):
        Agent.__init__(self, unique_id, model)
        self.state = 0
        self.unique_id = unique_id
        self.fsm_size = fsm_size
        self.num_tokens = num_tokens
        self.scores = []
        self.decision = NO_ACTION

        self.gen_automata(fsm_size, num_tokens)
        
    def gen_automata(self, fsm_size, num_tokens):
        #map current state to action; 50% chance of choosing a token to send, 50% of choosing cooperate/defect
        self.action_map = {}
        for state in range(fsm_size):
            flip = random.random()
            if (flip < 0.8):
                self.action_map[state] = random.randint(1, num_tokens-1)
            else: 
                self.action_map[state] = random.choice([COOPERATE, DEFECT])

        #map from tuple (current state, received communication) to the next state
        self.transition_table = dict.fromkeys([(state, received_token) for state in range(fsm_size) for received_token in range(num_tokens)])
        for pair in self.transition_table.keys():
            self.transition_table[pair] = random.randrange(fsm_size)

    def choose_action(self):
        # If decision is already made, return 0
        if (self.decision == COOPERATE) or (self.decision == DEFECT):
            return 0
        # Check to see if current state leads to a decision
        elif(self.action_map[self.state] == COOPERATE) or (self.action_map[self.state] == DEFECT):
            self.decision = self.action_map[self.state]
            return 0
        # Else, return token specified by current state
        else:
            return self.action_map[self.state]
            
    def handle_token(self, token):
        #takes in receiving token and selects next state
        # If a decision hasn't been made, we move to the next state
        if (self.decision != NO_ACTION):
            self.set_state(self.transition_table[(self.state, token)])
    
    def reset(self):
        self.state = 0
        self.scores = []
        self.decision = NO_ACTION

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
        
        self.total_cooperations = []
        self.total_defections = []
        self.single_gen_cooperations = 0
        self.single_gen_defections = 0
        self.total_chats = []
        self.single_gen_chats = []
        self.total_proportions = []
        self.single_gen_transition_mutations = 0
        self.total_transition_muations = []
        self.single_gen_action_mutations = 0
        self.total_action_muations = []
        
        self.agents = []
        
        for i in range(self.num_agents):
            agent = CommunicationAgent(i, self, fsm_size, num_tokens)
            self.agents.append(agent)

    def run_one_round(self, agent1, agent2):
        pass
 
    def step(self):
        self.reset_agents()
        self.selection()
    
    def selection(self):
        self.single_gen_cooperations = 0
        self.single_gen_defections = 0
        self.single_gen_chats = []
        self.single_gen_transition_mutations = 0
        self.single_gen_action_mutations = 0

        pairings = list(itertools.combinations(self.agents, 2))
        for pair in pairings:
            self.play(pair[0], pair[1])
        # pairings = Set
        
        #choose two agents to PLAY
        # for agent1 in self.agents:
        #     for agent2 in self.agents:
        #         if agent1 != agent2:
        #             self.play(agent1, agent2)
        
        self.total_cooperations.append(self.single_gen_cooperations)
        self.total_defections.append(self.single_gen_defections)
        self.total_chats.append(np.mean(self.single_gen_chats))
        self.total_proportions.append(self.single_gen_cooperations / (self.single_gen_defections + self.single_gen_cooperations))
        
        #better average scoring agent is placed into the new pool with a 50% probability that it will be mutated
            #if it is mutated, 1) 50% chance that a random action_map state is changed (using the same 50/50 in gen_automata)
                #or 2) 50% chance that a random transition_map state is changed
        #RUN THIS SELECTION N TIMES for each agent; results in a new population of size N; run the step function again with this new population
        new_population = []
        for i in range(self.num_agents):
            agent1 = random.choice(self.agents)
            agent2 = random.choice(self.agents)
            while(agent1 == agent2):
                agent2 = random.choice(self.agents)
            better_agent = agent1 if sum(agent1.scores) > sum(agent2.scores) else agent2
            
            if random.random() < .5: # roll for whether or not to mutate
                if random.random() < .5: # roll for mutation type (change action map vs transition table)
                    self.single_gen_action_mutations += 1
                    if random.random() < .8: # roll for how to set new action map value (same as in agent's gen_automata function)
                        better_agent.action_map[random.randrange(self.fsm_size)] = random.randint(1, self.num_tokens - 1)
                    else: 
                        better_agent.action_map[random.randrange(self.fsm_size)] = random.choice([COOPERATE, DEFECT])
                else:
                    self.single_gen_transition_mutations += 1
                    better_agent.transition_table[random.choice(list(better_agent.transition_table.keys()))] = random.randrange(self.fsm_size)
            new_agent = CommunicationAgent(better_agent.unique_id, self, self.fsm_size, self.num_tokens)
            new_agent.transition_table = copy.copy(better_agent.transition_table)
            new_agent.action_map = copy.copy(better_agent.action_map)
            new_population.append(new_agent)
            # new_population.append(copy.deepcopy(better_agent))
        self.total_transition_muations.append(self.single_gen_transition_mutations)
        self.total_action_muations.append(self.single_gen_action_mutations)
        self.agents = new_population

    def play(self, agent1, agent2):
        chat_count = 0
        while chat_count < self.max_chat:
            #still talking
            agent1_token = agent1.choose_action()
            agent2_token = agent2.choose_action()
            
            if (agent1_token == 0 and agent2_token == 0):
                break
            
            agent1.handle_token(agent2_token)
            agent2.handle_token(agent1_token)
            
            chat_count += 1
        self.single_gen_chats.append(chat_count)
        agent1_score, agent2_score = payout[(agent1.decision, agent2.decision)]
        if agent1.decision == COOPERATE and agent2.decision == COOPERATE:
            self.single_gen_cooperations += 1
        elif agent1.decision == DEFECT or agent2.decision == DEFECT:
            self.single_gen_defections += 1
        agent1.scores.append(agent1_score)
        agent2.scores.append(agent2_score)
        # return score of agents as a tuple (agent1_score, agent2_score)
    
    def reset_agents(self):
        for agent in self.agents:
            agent.reset()


if __name__ == '__main__':
    communicationModel = CommunicationModel(50, 4, 4, 2)
    for i in tqdm(range(5000)):
        communicationModel.step()
    for agent in communicationModel.agents:
        print(np.mean(agent.scores))
    # print('Cooperations array')
    # print(communicationModel.total_cooperations)
    # plt.plot(communicationModel.total_cooperations)
    # plt.title('Cooperations')
    # plt.show()
    # print('Defections array')
    # print(communicationModel.total_defections)
    # plt.plot(communicationModel.total_defections)
    # plt.title('Defections')
    # plt.show()

    print('Proportions array')
    print(communicationModel.total_proportions)
    plt.plot(communicationModel.total_proportions)
    plt.title('Proportion of mutual cooperations')
    plt.show()

    print('Communications array')
    print(communicationModel.total_chats)
    plt.plot(communicationModel.total_chats)
    plt.title('Chats')
    plt.show()
    
    plt.plot(communicationModel.total_action_muations)
    plt.title('Action map mutations')
    plt.show()
    
    plt.plot(communicationModel.total_transition_muations)
    plt.title('Transition table mutations')
    plt.show()