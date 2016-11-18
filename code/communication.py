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
payout = {(COOPERATE,COOPERATE):(3,3), (COOPERATE,DEFECT):(0,5), (COOPERATE,NO_ACTION):(2,-5), (DEFECT,COOPERATE):(5,0), (DEFECT,DEFECT):(1,1), (DEFECT,NO_ACTION):(2,-5), (NO_ACTION,NO_ACTION):(-5,-5), (NO_ACTION,COOPERATE):(-5,2), (NO_ACTION,DEFECT):(-5,2)}

    
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
            if (flip < 0.5):
                self.action_map[state] = random.randint(1, num_tokens-1)
            else: 
                self.action_map[state] = random.choice([COOPERATE, DEFECT])

        #map from tuple (current state, received communication) to the next state
        self.transition_table = {}
        states = range(fsm_size)
        tokens = range(num_tokens)

        state_token_pairs = itertools.product(states, tokens)
        for pair in state_token_pairs:
            self.transition_table[pair] = random.randrange(fsm_size)

    def choose_action(self):
        # If decision is already made, return 0
        if (self.decision != NO_ACTION):
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
        self.total_proportions_cooperate = []
        self.total_proportion_defect = []
        
        self.agents = []
        
        for i in range(self.num_agents):
            agent = CommunicationAgent(i, self, fsm_size, num_tokens)
            self.agents.append(agent)
 
    def step(self):
        self.reset_agents()
        self.selection()
    
    def selection(self):
        self.single_gen_cooperations = 0
        self.single_gen_defections = 0
        self.single_gen_no_actions = 0
        self.single_gen_chats = []

        pairings = list(itertools.combinations(self.agents, 2))
        num_games = len(pairings)
        for pair in pairings:

            self.play(pair[0], pair[1])
        
        self.total_cooperations.append(self.single_gen_cooperations)
        self.total_defections.append(self.single_gen_defections)
        self.total_chats.append(np.mean(self.single_gen_chats))
        # print(self.single_gen_defections+self.single_gen_cooperations)
        self.total_proportions_cooperate.append(self.single_gen_cooperations / num_games)
        self.total_proportion_defect.append(self.single_gen_defections / num_games)
        
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
            better_agent = agent1 if np.mean(agent1.scores) > np.mean(agent2.scores) else agent2

            new_action_map = copy.deepcopy(better_agent.action_map)
            new_transition_table = copy.deepcopy(better_agent.transition_table)
            
            if random.random() < .5: # roll for whether or not to mutate
                if random.random() < .5: # roll for mutation type (change action map vs transition table)
                    if random.random() < .5: # roll for how to set new action map value (same as in agent's gen_automata function)
                        new_action_map[random.randrange(self.fsm_size)] = random.randint(1, self.num_tokens - 1)
                    else: 
                        new_action_map[random.randrange(self.fsm_size)] = random.choice([COOPERATE, DEFECT])
                else:
                    new_transition_table[random.choice(list(new_transition_table.keys()))] = random.randrange(self.fsm_size)
            new_agent = CommunicationAgent(better_agent.unique_id, self, self.fsm_size, self.num_tokens)
            new_agent.transition_table = new_transition_table
            new_agent.action_map = new_action_map
            new_population.append(new_agent)
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
        scores = payout[(agent1.decision, agent2.decision)]
        # print("Agent 1: {} Agent 2: {}  |  Scores: {} {} ".format(agent1.decision, agent2.decision, scores[0], scores[1])) 
        if agent1.decision == COOPERATE and agent2.decision == COOPERATE:
            self.single_gen_cooperations += 1
        elif agent1.decision == DEFECT and agent2.decision == DEFECT:
            self.single_gen_defections += 1
        elif agent1.decision == NO_ACTION or agent2.decision == NO_ACTION:
            self.single_gen_no_actions +=1

        agent1.scores.append(agent1_score)
        agent2.scores.append(agent2_score)
        # return score of agents as a tuple (agent1_score, agent2_score)
    
    def reset_agents(self):
        for agent in self.agents:
            agent.reset()


if __name__ == '__main__':
    communicationModel = CommunicationModel(50, 10, 4, 4)
    for i in tqdm(range(1000)):
        communicationModel.step()

    # for agent in communicationModel.agents:
        # print(np.mean(agent.scores))
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

    # print('Proportions array')
    # print(communicationModel.total_proportions)
    plt.subplot(2, 1, 1)
    plt.plot(communicationModel.total_proportions_cooperate)
    # plt.plot(communicationModel.total_proportion_defect)
    plt.title('Proportion of cooperate / defect')

    # print('Communications array')
    # print(communicationModel.total_chats)
    plt.subplot(2, 1, 2)
    plt.plot(communicationModel.total_chats)
    plt.title('Chats')
    plt.show()