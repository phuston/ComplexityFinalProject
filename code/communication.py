"""communication.py: Implementation of the agent-based model described in Communication and Cooperation - Miller et. al"""

__author__      = "Patrick Huston, Meg McCauley, Andrew Pan"

import random, copy, itertools
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from mesa import Agent, Model

# Final actions
COOPERATE = -1
DEFECT = -2
NO_ACTION = -3

# Payout mapping
payout = {(COOPERATE,COOPERATE):(3,3), (COOPERATE,DEFECT):(0,5), (COOPERATE,NO_ACTION):(2,-5), (DEFECT,COOPERATE):(5,0), (DEFECT,DEFECT):(1,1), (DEFECT,NO_ACTION):(2,-5), (NO_ACTION,NO_ACTION):(-5,-5), (NO_ACTION,COOPERATE):(-5,2), (NO_ACTION,DEFECT):(-5,2)}

class CommunicationAgent(Agent):
    """ 
    Represents an agent in the agent-based model investigated in 'Communication and Cooperation' - Miller, et. al

    Holds an action map and transition table to define automata
    """
    
    def __init__(self, unique_id, model, fsm_size, num_tokens):
        Agent.__init__(self, unique_id, model)
        self.state = 0
        self.unique_id = unique_id
        self.scores = []
        self.decision = NO_ACTION

        self.gen_automata(fsm_size, num_tokens)
        
    def gen_automata(self, fsm_size, num_tokens):
        """ Generates action map and transition table to describe agent's automata

        Creates an action map - map of state : action (token to send or final move)
        Creates transition table - map of (state, token) : new state

        Args:
            fsm_size (int): Number of states in automata
            num_tokens (int): Number of tokens allowed in communication
        """

        # Create action map
        self.action_map = {}
        for state in range(fsm_size):
            flip = random.random()
            if (flip < 0.5 or state == 0):
                # .5 probability of choosing a token to send
                self.action_map[state] = random.randint(1, num_tokens-1)
            else: 
                # .5 probability of choosing cooperate/defect
                self.action_map[state] = random.choice([COOPERATE, DEFECT])

        # Create transition table
        self.transition_table = {}
        states = range(fsm_size)
        tokens = range(num_tokens)

        state_token_pairs = itertools.product(states, tokens)
        for state_token_pair in state_token_pairs:
            self.transition_table[state_token_pair] = random.randrange(fsm_size)

    def choose_action(self):
        """ Choose agent's action (token or decision) based on current state

        If agent has already made a decision, send a 0 token
        If agent's new state represents choosing an action, set decision and send 0 token
        Else, send return communication token specified by current state
        """

        if (self.decision != NO_ACTION):
            return 0

        elif(self.action_map[self.state] == COOPERATE) or (self.action_map[self.state] == DEFECT):
            self.decision = self.action_map[self.state]
            return 0

        else:
            return self.action_map[self.state]
            
    def handle_token(self, token):
        """Reads in and handles token sent by the other agent

        If a decision hasn't been made, agent moves to next state defined
        in the transition map.

        Args:
            token (int): token sent by opponent
        """

        if (self.decision != COOPERATE and self.decision != DEFECT):
            self.set_state(self.transition_table[(self.state, token)])
    
    def reset(self):
        """ Reset the agent's parameters """ 

        self.state = 0
        self.scores = []
        self.decision = NO_ACTION

    def get_state(self):
        """ Return agent's automaton state """
        return self.state
        
    def set_state(self, state):
        """ Set agent's state """
        self.state = state



class CommunicationModel(Model):
    """ 
    Represents agent-based model investigated in 'Communication and Cooperation' - Miller, et. al
    """
    
    def __init__(self, N=50, max_chat_length=20, fsm_size=4, num_tokens=2, mutation_rate=0.5, num_agents_compared=2):
        """ Create a CC model with given parameters

        Args:
            N (int): number of agents in the model
            max_chat_length (int): Maximum number of communications allowed
            fsm_size (int): Number of states in agents' automata
            num_tokens (int): Number of communication tokens allowed
        """
        
        self.num_agents = N
        self.max_chat_length = max_chat_length
        self.fsm_size = fsm_size
        self.num_tokens = num_tokens
        self.mutation_rate = mutation_rate
        self.num_agents_compared = num_agents_compared
        
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
        self.run_generation()
    
    def run_generation(self):
        """ Runs one generation of model

        First, plays all agents against each other in single-shot PD game
        Next, generates new population of same size as described in C+C
        """
 
        self.single_gen_cooperations = 0
        self.single_gen_defections = 0
        self.single_gen_no_actions = 0
        self.single_gen_chats = []

        # Generate all pairings of agents to play
        pairings = list(itertools.combinations(self.agents, 2))
        num_games = len(pairings)

        for pair in pairings:
            self.play(pair[0], pair[1])
        
        self.total_cooperations.append(self.single_gen_cooperations)
        self.total_defections.append(self.single_gen_defections)
        self.total_chats.append(np.mean(self.single_gen_chats))
        self.total_proportions_cooperate.append(self.single_gen_cooperations / num_games)
        self.total_proportion_defect.append(self.single_gen_defections / num_games)

        self.generate_new_population()

    def generate_new_population(self): 
        """ Generates a new population of the same size with random mutations

        Runs a tournament-style selection with replacement to generate a new population of agents
        Fitter of 2 agents selected has a 50% chance of mutation to either its action map or transition table
        """
        
        new_population = []
        agents_list = []
        high_score = 0
        for i in range(self.num_agents):

            agents_list = random.sample(self.agents, self.num_agents_compared)

            # better_agent = agent1 if np.mean(agent1.scores) > np.mean(agent2.scores) else agent2
            for each_agent in agents_list:
                if np.mean(each_agent.scores) > high_score:
                    better_agent = each_agent
                else:
                    better_agent = agents_list[0]       ## pretty lame way of making sure at least one agent is the "best"

            # Copy automata elements from better agent
            new_action_map = copy.deepcopy(better_agent.action_map)
            new_transition_table = copy.deepcopy(better_agent.transition_table)
            
            mutate_flip = random.random() < self.mutation_rate # Roll for mutation
            mutate_action = random.random() < 0.5 # Roll for mutation type - action map vs transition table

            if mutate_flip: # roll for whether or not to mutate
                if mutate_action: # roll for mutation type (change action map vs transition table)
                    stateChoice = random.randrange(self.fsm_size)
                    if random.random() < .5 or stateChoice == 0: # Roll for how to set new action map value
                        new_action_map[stateChoice] = random.randint(1, self.num_tokens - 1)
                    else: 
                        new_action_map[stateChoice] = random.choice([COOPERATE, DEFECT])
                else:
                    new_transition_table[random.choice(list(new_transition_table.keys()))] = random.randrange(self.fsm_size)
            
            # Create new agent with better properties and set attributes
            new_agent = CommunicationAgent(i, self, self.fsm_size, self.num_tokens)
            new_agent.transition_table = new_transition_table
            new_agent.action_map = new_action_map

            new_population.append(new_agent)


        self.agents = new_population

    def play(self, agent1, agent2):
        """ Plays two agents against each other in a single-shot prisoner's dilemma

        Args:
            agent1 (CommunicationAgent): Agent 1 in the game
            agent2 (CommunicationAgent): Agent 2 in the game
        """

        chat_length = 0
        agent1.state = 0
        agent1.decision = NO_ACTION
        agent2.state = 0
        agent2.decision = NO_ACTION
        while chat_length < self.max_chat_length:

            # Choose actions for agent1 and agent2
            agent1_token = agent1.choose_action()
            agent2_token = agent2.choose_action()
            
            # Both agents have decided - break
            if (agent1_token == 0 and agent2_token == 0):
                break
            
            # Agents handle tokens 
            agent1.handle_token(agent2_token)
            agent2.handle_token(agent1_token)
            chat_length += 1
        self.single_gen_chats.append(chat_length)

        # Compute scores using payout dictionaryff
        agent1_score, agent2_score = payout[(agent1.decision, agent2.decision)]

        agent1.scores.append(agent1_score)
        agent2.scores.append(agent2_score)

        # Record scores for statistics
        if agent1.decision == COOPERATE and agent2.decision == COOPERATE:
            self.single_gen_cooperations += 1
        elif agent1.decision == DEFECT and agent2.decision == DEFECT:
            self.single_gen_defections += 1
        elif agent1.decision == NO_ACTION or agent2.decision == NO_ACTION:
            self.single_gen_no_actions +=1
    
    def reset_agents(self):
        for agent in self.agents:
            agent.reset()

def sweep_mutation(iterations):
    # Run sweep of mutation rates
    mutation_rates = np.arange(0,0.5,0.1)
    cooperative_gens_counts = []

    for mutation_rate in mutation_rates:
        communicationModel = CommunicationModel(mutation_rate=mutation_rate)
        num_cooperative_gens = 0
        for i in tqdm(range(iterations)):
            communicationModel.step()
            if communicationModel.total_proportions_cooperate[-1] > .1 and i > 100:
                num_cooperative_gens += 1
        cooperative_gens_counts.append(num_cooperative_gens)

    fig = plt.figure()
    fig.suptitle("Level of Cooperation vs. Agent Mutation Rate", fontsize=14, fontweight='bold')

    axis = fig.add_subplot(111)
    axis.plot(mutation_rates, cooperative_gens_counts)
    axis.set_xlabel('Mutation Rate')
    axis.set_ylabel('Rate of Cooperative Generations per 1000 Generations')
    plt.show()

def sweep_agent_comparison(iterations):
    # Run sweep of number of agents compared
    num_agents_compared = np.arange(2,3,1)
    cooperative_gens_counts = []

    for num_agents in num_agents_compared:
        communicationModel = CommunicationModel(num_agents_compared=num_agents)
        num_cooperative_gens = 0
        for i in tqdm(range(iterations)):
            communicationModel.step()
            if communicationModel.total_proportions_cooperate[-1] > .1 and i > 100:
                num_cooperative_gens += 1
        cooperative_gens_counts.append(num_cooperative_gens)

    fig = plt.figure()
    fig.suptitle("Level of Cooperation vs. Number of Agents Compared", fontsize=14, fontweight='bold')

    axis = fig.add_subplot(111)
    axis.plot(num_agents_compared, cooperative_gens_counts)
    axis.set_xlabel('Number of Agents Compared')
    axis.set_ylabel('Rate of Cooperative Generations per 1000 Generations')
    plt.show()

if __name__ == '__main__':
    # sweep_mutation(5000)
    sweep_agent_comparison(1000)
