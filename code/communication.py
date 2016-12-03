"""communication.py: Implementation of the agent-based model described in Communication and Cooperation - Miller et. al"""

__author__      = "Patrick Huston, Meg McCauley, Andrew Pan"

import random, copy, itertools
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from mesa import Agent, Model
# import logging

# logging.basicConfig(filename='output.log',level=logging.DEBUG)
# with open('output.log', 'w'):
#     pass

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
    
    def __init__(self, N=50, max_chat_length=20, fsm_size=4, num_tokens=2):
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
        
        # logging.debug("GENERATING_POPULATION")
        
        new_population = []
        for i in range(self.num_agents):

            # logging.debug("Begin-Selection {}".format(i))
            agent1, agent2 = random.sample(self.agents, 2)
            # logging.debug("Agent1 ID:    {}   Agent2 ID:    {}".format(agent1.unique_id, agent2.unique_id))
            # logging.debug("Agent1 Score: {}   Agent2 Score: {}".format(np.mean(agent1.scores), np.mean(agent2.scores)))

            better_agent = agent1 if np.mean(agent1.scores) > np.mean(agent2.scores) else agent2
            
            # logging.debug("Winning Agent: {}".format(better_agent.unique_id))


            # Copy automata elements from better agent
            new_action_map = copy.deepcopy(better_agent.action_map)
            new_transition_table = copy.deepcopy(better_agent.transition_table)
            
            mutate_flip = random.random() < 0.5 # Roll for mutation
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
            # logging.debug('New Agent Transition Table: {}'.format(new_transition_table))
            # logging.debug('New Agent Action Map: {}'.format(new_action_map))
            new_agent = CommunicationAgent(i, self, self.fsm_size, self.num_tokens)
            new_agent.transition_table = new_transition_table
            new_agent.action_map = new_action_map

            new_population.append(new_agent)
            # logging.debug("End-Selection {}\n".format(i))


        self.agents = new_population
        
        # logging.debug("END_GENERATION\n")

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
        # logging.debug('COMMUNICATION START')
        # logging.debug('Agent1 Transition Table: {}'.format(agent1.transition_table))
        # logging.debug('Agent1 Action Map: {}\n'.format(agent1.action_map))
        # logging.debug('Agent2 Transition Table: {}'.format(agent2.transition_table))
        # logging.debug('Agent2 Action Map: {}\n'.format(agent2.action_map))
        while chat_length < self.max_chat_length:

            # Choose actions for agent1 and agent2
            agent1_token = agent1.choose_action()
            agent2_token = agent2.choose_action()
            
            # Both agents have decided - break
            if (agent1_token == 0 and agent2_token == 0):
                # logging.debug('Communication Finished\nAgent1 State: {} | Agent2 State: {}'.format(agent1.state, agent2.state))
                break
            
            # logging.debug('Agent1 State: {} Token Sent: {}   |   Agent2 State: {}  Token Sent: {}'.format(agent1.state, agent1_token, agent2.state, agent2_token))
            # Agents handle tokens 
            agent1.handle_token(agent2_token)
            agent2.handle_token(agent1_token)
            chat_length += 1
        # logging.debug('Chat length: {}'.format(chat_length))
        # logging.debug('END COMMUNICATION\n')
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

if __name__ == '__main__':

    fsm_sizes = range(2, 8)
    token_exps = range(2, 8)

    for fsm_size in fsm_sizes:
        for num_tokens in token_exps:
            communicationModel = CommunicationModel(fsm_size=fsm_size, num_tokens=num_tokens)
            print("Running model... fsm_size: {}, num_tokens: {}".format(fsm_size, num_tokens))
            for i in tqdm(range(5000)):
                communicationModel.step()

            fig = plt.figure()
            fig.suptitle("Cooperation Emergence - {} States, {} Tokens".format(fsm_size, num_tokens), fontsize=14, fontweight='bold')

            # Plot proportion of mutual cooperative games
            coop_ax = fig.add_subplot(211)
            coop_ax.plot(communicationModel.total_proportions_cooperate)
            coop_ax.set_title('Proportion of Mutually Cooperative Games')
            coop_ax.set_xlabel('Generation')
            coop_ax.set_ylabel('Proportion of MutualCoop Games')

            # Plot average chat length for each game
            chat_ax = fig.add_subplot(212)
            chat_ax.plot(communicationModel.total_chats)
            chat_ax.set_title('Average Chat Length')
            chat_ax.set_xlabel('Generation')
            chat_ax.set_ylabel('Average Chat Length (Tokens)')
    plt.show()

    # communicationModel = CommunicationModel(fsm_size=fsm_size, num_tokens=num_tokens)
    # print("Running model... fsm_size: {}, num_tokens: {}".format(fsm_size, num_tokens))
    # for i in tqdm(range(100)):
    #     communicationModel.step()

    # fig = plt.figure()
    # fig.suptitle("Cooperation Emergence - {} States, {} Tokens".format(fsm_size, num_tokens), fontsize=14, fontweight='bold')

    # # Plot proportion of mutual cooperative games
    # coop_ax = fig.add_subplot(211)
    # coop_ax.plot(communicationModel.total_proportions_cooperate)
    # coop_ax.set_title('Proportion of Mutually Cooperative Games')
    # coop_ax.set_xlabel('Generation')
    # coop_ax.set_ylabel('Proportion of MutualCoop Games')

    # # Plot average chat length for each game
    # chat_ax = fig.add_subplot(212)
    # chat_ax.plot(communicationModel.total_chats)
    # chat_ax.set_title('Average Chat Length')
    # chat_ax.set_xlabel('Generation')
    # chat_ax.set_ylabel('Average Chat Length (Tokens)')

    # communicationModel = CommunicationModel(N=50, fsm_size=4, num_tokens=2)
    # for i in tqdm(range(5000)):
    #     # logging.debug('Generation Number {}'.format(i))
    #     communicationModel.step()

    # # Plot proportion of mutual cooperative games
    # plt.subplot(2, 1, 1)
    # plt.plot(communicationModel.total_proportions_cooperate)
    # plt.title('Proportion of cooperate / defect')

    # # Plot average chat length for each game
    # plt.subplot(2, 1, 2)
    # plt.plot(communicationModel.total_chats)
    # plt.title('Chats')
    # plt.show()