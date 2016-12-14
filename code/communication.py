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

class TuringAgent(CommunicationAgent):
    def __init__(self, unique_id, model, tape_states, num_tokens):
        Agent.__init__(self, unique_id, model)
        self.state = 0
        self.unique_id = unique_id
        self.scores = []
        self.decision = NO_ACTION
        self.tape_states = tape_states
        self.num_tokens = num_tokens

        self.genRuleTable(tape_states, num_tokens)
        self.genActionMap(num_tokens)

    def genRuleTable(self, agent_states, num_tokens):
        self.rule_table = {} # keys will be current state and token being read, mapping to what to write to the tape, where to move, and what to change current state to
        state_token_pairs = itertools.product(range(agent_states), range(num_tokens))
        for state_token_pair in state_token_pairs:
            change_state = (COOPERATE if random.random() < .5 else DEFECT) if random.random() < .3 else random.randrange(agent_states) # roll to either change states to C/D or another state
            self.rule_table[state_token_pair] = (random.randrange(agent_states), random.choice([-1, 0, 1]), change_state) # each tuple in the dictionary is (token to write to tape, move l/r or stay put, state to change to)

    def genActionMap(self, num_tokens):
        self.action_map = {-2: 0, -1: 0}
        for state in range(self.tape_states): #create map from all states to tokens to send
            self.action_map[state] = random.randint(1, num_tokens - 1)

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

class TuringModel(CommunicationModel):
    def __init__(self, N=50, max_chat_length=20, tape_states=4, num_tokens=4, tape_length = 10):
        """ Create a CC model with given parameters

        Args:
            N (int): number of agents in the model
            max_chat_length (int): Maximum number of communications allowed
            fsm_size (int): Number of states in agents' tape
            num_tokens (int): Number of communication tokens allowed, including the null token
        """
        
        self.num_agents = N
        self.max_chat_length = max_chat_length
        self.tape_states = tape_states
        self.num_tokens = num_tokens
        self.tape_length = tape_length
        
        self.total_cooperations = []
        self.total_defections = []
        self.single_gen_cooperations = 0
        self.single_gen_defections = 0
        self.total_chats = []
        self.single_gen_chats = []
        self.total_proportions_cooperate = []
        self.total_proportion_defect = []
        self.tape = [random.randrange(self.tape_states) for i in range(self.tape_length)]
        self.agents = []
        
        for i in range(self.num_agents):
            agent = TuringAgent(i, self, tape_states, num_tokens)
            self.agents.append(agent)
    
    def generate_new_population(self):
        new_population = []
        for i in range(self.num_agents):

            agent1, agent2 = random.sample(self.agents, 2)

            better_agent = agent1 if np.mean(agent1.scores) > np.mean(agent2.scores) else agent2
            new_rule_table = copy.deepcopy(better_agent.rule_table)
            new_action_map = copy.deepcopy(better_agent.action_map)
            
            mutate_flip = random.random() < 0.5 # Roll for mutation
            mutate_action = random.random() < 0.5 # Roll for mutation type

            if mutate_flip: # roll for whether or not to mutate
                if mutate_action:
                    new_action_map[random.randrange(self.tape_states)] = random.randint(1, self.num_tokens - 1)
                else:
                    change_state = (COOPERATE if random.random() < .5 else DEFECT) if random.random() < .3 else random.randrange(self.tape_states) # roll to either change states to C/D or another state
                    new_rule_table[(random.randrange(self.tape_states), random.randrange(self.num_tokens))] = (random.randrange(self.tape_states), random.choice([-1, 0, 1]), change_state)

            
            # Create new agent with better properties and set attributes
            new_agent = TuringAgent(i, self, self.tape_states, self.num_tokens)
            new_agent.rule_table = new_rule_table
            new_agent.action_map = new_action_map

            new_population.append(new_agent)
        self.agents = new_population
    def play(self, agent1, agent2):
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
        
        agent1_pos = random.randrange(self.tape_length) # set agents on the tape
        agent2_pos = random.randrange(self.tape_length)

        while chat_length < self.max_chat_length:
            # general todo:
            # place each agent on the tape at either random locations or specified positions, tbd but leaning towards random locations, this should actually be done before the while loop
            # have agents read the tape value for their current position, don't need to create an agent method for choose_action unless really feeling a need to modularize
            # agents send each other a token
            # agents then pass read tape value and state through their rule table, edit the tape, change their position on the tape, send a token, and change their state
            # now realizing that I have to add tokens to creating agents and generating a new population - done
            # have to determine how to handle both agents trying to edit the same position on the tape at the same time
            # have to handle agents trying to move left or right off the edge of the turing tape, either prevent their movement or wrap around the ends of the tape - done, wrapped
            # of course, stop agents if both tokens sent are 0
            agent1_token = agent1.action_map[self.tape[agent1_pos]] if agent1.decision == NO_ACTION else 0 # agents' tokens are found in the action map, based on the tape input at the agents' position
            agent2_token = agent2.action_map[self.tape[agent2_pos]] if agent2.decision == NO_ACTION else 0

            if agent1_token == 0 and agent2_token == 0: # end the run if both tokens are 0
                break

            if agent1.decision == NO_ACTION:
                tape_state1, move1, change_state1 = agent1.rule_table[(agent1.state, agent2_token)] # pass agent current state and token from other agent into agent's rule table

                self.tape[agent1_pos] = tape_state1 # agents writing to tape

                agent1_pos += move1 # agents move their position, either -1, 0, or 1

                agent1.state = change_state1 # agents then change state

                if agent1.state == COOPERATE:
                    agent1.decision = COOPERATE
                elif agent1.state == DEFECT:
                    agent1.decision = DEFECT

                if agent1_pos < 0: # ensuring that agent position remains on the tape, wrapping around the ends
                    agent1_pos = self.tape_length - 1
                elif agent1_pos >= self.tape_length:
                    agent1_pos = 0

            if agent2.decision == NO_ACTION:
                tape_state2, move2, change_state2 = agent2.rule_table[(agent2.state, agent1_token)]
                 
                self.tape[agent2_pos] = tape_state2

                agent2_pos += move2

                agent2.state = change_state2

                if agent2.state == COOPERATE:
                    agent2.decision = COOPERATE
                elif agent2.state == DEFECT:
                    agent2.decision = DEFECT

                if agent2_pos < 0:
                    agent2_pos = self.tape_length - 1
                elif agent2_pos >= self.tape_length:
                    agent2_pos = 0

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

if __name__ == '__main__':

    fsm_sizes = range(2, 8)
    token_exps = range(2, 8)

    for fsm_size in fsm_sizes:
        for num_tokens in token_exps:
            turingModel = TuringModel(tape_states=fsm_size, num_tokens=num_tokens)
            print("Running model... fsm_size: {}, num_tokens: {}".format(fsm_size, num_tokens))
            for i in tqdm(range(1000)):
                turingModel.step()

            fig = plt.figure()
            fig.suptitle("Cooperation Emergence - {} States, {} Tokens".format(fsm_size, num_tokens), fontsize=14, fontweight='bold')

            # Plot proportion of mutual cooperative games
            coop_ax = fig.add_subplot(211)
            coop_ax.plot(turingModel.total_proportions_cooperate)
            coop_ax.set_title('Proportion of Mutually Cooperative Games')
            coop_ax.set_xlabel('Generation')
            coop_ax.set_ylabel('Proportion of MutualCoop Games')

            # Plot average chat length for each game
            chat_ax = fig.add_subplot(212)
            chat_ax.plot(turingModel.total_chats)
            chat_ax.set_title('Average Chat Length')
            chat_ax.set_xlabel('Generation')
            chat_ax.set_ylabel('Average Chat Length (Tokens)')
    plt.show()
    # fsm_sizes = range(2, 8)
    # token_exps = range(2, 8)

    # cooperative_gens = {}
    # for i in range(2, 8):
    #     for j in range(2, 8):
    #         cooperative_gens[(i, j)] = 0
    # for fsm_size in fsm_sizes:
    #     for num_tokens in token_exps:
    #         communicationModel = CommunicationModel(fsm_size=fsm_size, num_tokens=num_tokens)
    #         print("Running model... fsm_size: {}, num_tokens: {}".format(fsm_size, num_tokens))
    #         for i in tqdm(range(20000)):
    #             communicationModel.step()
    #             if communicationModel.total_proportions_cooperate[-1] > .3 and i > 100:
    #                 cooperative_gens[(fsm_size, num_tokens)] += 1

    #         fig = plt.figure()
    #         fig.suptitle("Cooperation Emergence - {} States, {} Tokens".format(fsm_size, num_tokens), fontsize=14, fontweight='bold')

    #         # Plot proportion of mutual cooperative games
    #         coop_ax = fig.add_subplot(211)
    #         coop_ax.plot(communicationModel.total_proportions_cooperate)
    #         coop_ax.set_title('Proportion of Mutually Cooperative Games')
    #         coop_ax.set_xlabel('Generation')
    #         coop_ax.set_ylabel('Proportion of MutualCoop Games')

    #         # Plot average chat length for each game
    #         chat_ax = fig.add_subplot(212)
    #         chat_ax.plot(communicationModel.total_chats)
    #         chat_ax.set_title('Average Chat Length')
    #         chat_ax.set_xlabel('Generation')
    #         chat_ax.set_ylabel('Average Chat Length (Tokens)')
    # plt.show()

    # cooperative_gens_states = [cooperative_gens[(state, 4)] for state in range(2, 8)]
    # cooperative_gens_tokens = [cooperative_gens[(4, tokens)] for tokens in range(2, 8)]

    # generations_fig = plt.figure()
    # generations_fig.suptitle('Cooperative Generations with Varying Automata States and Token Counts')

    # generations_states = generations_fig.add_subplot(211)
    # generations_states.plot(range(2, 8), cooperative_gens_states)
    # generation_states.set_xlabel('Automata State Size')
    # generation_states.set_ylabel('Number of Cooperative Generations')
    # generations_states.plot()

    # generations_tokens = generations_fig.add_subplot(212)
    # generations_tokens.plot(range(2, 8), cooperative_gens_tokens)
    # generations_tokens.set_xlabel('Number of Tokens')
    # generations_tokens.set_ylabel('Number of Cooperative Generations')
    # generations_tokens.plot()
    # plt.show()

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

    turingModel = TuringModel(N=50, tape_states=4, num_tokens=4)
    for i in tqdm(range(1000)):
    #     # logging.debug('Generation Number {}'.format(i))
        turingModel.step()

    # Plot proportion of mutual cooperative games
    plt.subplot(2, 1, 1)
    plt.plot(turingModel.total_proportions_cooperate)
    plt.title('Proportion of cooperate / defect')

    # Plot average chat length for each game
    plt.subplot(2, 1, 2)
    plt.plot(turingModel.total_chats)
    plt.title('Chats')
    plt.show()