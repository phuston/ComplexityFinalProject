import random

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
# from mesa.datacollection import DataCollector

COOPERATE = -1
DEFECT = -2
NO_ACTION = -3
    
class CommunicationAgent(Agent):
    
    def __init__(self, unique_id, model, fsm_size, num_tokens):
        Agent.__init__(self, unique_id, model)
        self.state = 0
        self.unique_id = unique_id
        self.fsm_size = fsm_size
        self.num_tokens = num_tokens
        self.scores = []
        self.decision = None

        self.gen_automata(fsm_size, num_tokens)
        
    def gen_automata(self, fsm_size, num_tokens):
        #map current state to action; 50% chance of choosing a token to send, 50% of choosing cooperate/defect
        self.action_map = {}
        for state in range(fsm_size):
            flip = random.random()
            if (flip < 0.5):
                action_map[state] = random.randint(1, num_tokens)
            else: 
                action_map[state] = random.choice([COOPERATE, DEFECT])

        #map from tuple (current state, received communication) to the next state
        self.transition_table = dict.fromkeys([(state, received_token) for state in range(fsm_size) for received_token in range(num_tokens)])
        for pair in transition_table.keys():
            transition_table[pair] = random.randrange(fsm_size)
            
        print(action_map)
        print(transition_table)

    def choose_action(self):
        # If decision is already made, return 0
        if decision:
            return 0
        # Check to see if current state leads to a decision
        else if (self.action_map[self.state] == COOPERATE) or (self.action_map[self.state] == DEFECT):
            self.decision = self.action_map[self.state]
            return 0
        # Else, return token specified by current state
        else:
            return self.action_map[self.state]
            
    def handle_token(self, token):
        #takes in receiving token and selects next state
        # If a decision hasn't been made, we move to the next state
        if (self.decision != None):
            self.set_state(self.transition_table[(self.state, token)])
    
    def reset_scores(self):
        self.scores = []

    def get_state(self):
        return self.state
        
    def set_state(self, state):
        self.state = state
    
    def step(self):
        print(self.unique_id)

class CommunicationModel(Model):
    
    payout = {(COOPERATE,COOPERATE):(3,3), (COOPERATE,DEFECT):(0,5), (COOPERATE,NO_ACTION):(2,-5), (COOPERATE,NO_ACTION):(2,-5), (DEFECT,COOPERATE):(5,0), (DEFECT,DEFECT):(1,1), (DEFECT,NO_ACTION):(2,-5), (NO_ACTION,NO_ACTION):(-5,-5), (NO_ACTION,COOPERATE):(-5,2), (NO_ACTION,DEFECT):(-5,2)}
    
    def __init__(self, N, max_chat, fsm_size, num_tokens):      #fsm_size is number of states, num_tokens is complexity of language
        
        # TODO: Create agents
        # TODO: take in params - max_chat, fsm_size, num_tokens
        
        self.num_agents = N
        self.max_chat = max_chat
        self.fsm_size = fsm_size
        self.num_tokens = num_tokens
        # self.schedule = RandomActivation(self)
        
        self.agents = []
        
        for i in range(self.num_agents):
            agent = CommunicationAgent(i, self, fsm_size, num_tokens)
            # self.schedule.add(agent)
            self.agents.append(agent)

    def run_one_round(self, agent1, agent2):
        pass
 
    def step(self):
        # self.schedule.step()
        pass
        
        
        
        #reset all agents' automata to state 1 and score to 0
        #play all agents against each other
        #agent keeps track of its score
    
    def selection(self):
        #choose two agents to PLAY
        for agent1 in self.agents:
            for agent2 in self.agents:
                if agent1 != agent2:
                    self.play(agent1, agent2)
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
                    if random.random() < .5: # roll for how to set new action map value (same as in agent's gen_automata function)
                        better_agent.action_map[random.randrange(self.fsm_size)] = random.randint(1, num_tokens)
                    else: 
                        better_agent.action_map[random.randrange(self.fsm_size)] = random.choice([COOPERATE, DEFECT])
                else:
                    better_agent.transition_table[random.choice(better_agent.transition_table.keys())] = random.randrange(fsm_size)
            new_population.append(better_agent)
        self.agents = new_population

    def play(agent1, agent2):
        chat_count = 0
        while chat_count < num_chat :
            #still talking
            agent1_token = agent1.choose_action()
            agent2_token = agent2.choose_action()
            
            agent1.handle_token(agent2_token)
            agent2.handle_token(agent1_token)
            
            
            #both have chosen an action
            if (agent1_token == 0) && (agent2_token == 0):
                # FIGHT
            chat_count += 1
        agent1.scores.append(agent1_score)
        agent2.scores.append(agent2_score)
        # return score of agents as a tuple (agent1_score, agent2_score)
    
    def reset_agents(self):
        for agent in agents:
            agent.set_state(0)
            agent.reset_scores()


if __name__ == '__main__':
    communicationModel = CommunicationModel(1, 3, 3, 3)