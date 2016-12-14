### An Investigation into the Emergence of Cooperation through Communication
Patrick Huston, Meg McCauley, Andrew Pan | Fall 2016
Updated December 14th, 2016


#### Abstract
Cooperation is a phenomenon present in many aspects of life across many organisms, but the reasons cooperation happen do not always make sense. Even among less ‘advanced’ organisms in the world, we see evidence of individuals helping each other out for their mutual good even if one would benefit more from focusing on themselves. The world is a harsh place, and this behavior is not necessarily encoded directly in genes, so why and how does this happen? What conditions are necessary to create a system where cooperation emerges, even when the setup would tend towards selfishness? Is communication the key? In this project, we aim to address some of these questions in the context of an agent-based model with a communication framework, in addition to our main motivating question: Can mutual cooperation develop and exist at high levels within a system that offers no immediate or intuitive benefit for members to cooperate? What factors might be influential in creating these conditions?


To address some of these questions, we developed a model to gain insight into how communication affects the behavior of agents in an agent-based model. This model tests the ability and willingness of agents to cooperate through play of a prisoner's dilemma game. The impetus for this idea comes from experiments in this space by Miller, Butts, and Rode. Through the replication of Miller et. al’s model, we create a model that demonstrates emergent generations of mutual cooperation through agent communication. This resulting cooperation contradicts our expectation based on the the prisoner's dilemma ruleset, which encourages defection for maximum individual payoff. 


#### Experimentation
Based on the motivating questions discussed in the abstract, we implemented and  experimented with a model to determine whether or not communication and mutual cooperation emerged in a system that naturally tends towards mutual defection. In order to answer these questions, we replicated Miller et. al’s experiment which details agent-to-agent communication and decision making using an evolving prisoner's dilemma situation and communication between agents.


##### Model Setup
Our model is composed of a set number of agents, each of which contain an automaton that determine its actions and decisions during play. The automaton is composed of two parts. The first is a transition table, which maps an agent’s current state and the token they receive from the opposing player to a new state. The second part is an action map, which maps the agent’s current state to an action, either the sending of a token in the discrete set {1, 2, ... T} (where T is the number of allowed tokens), or deciding on an action (cooperate or defect), and sending the null token, 0. Together, these two structures define an agent’s behavior in the system. As in Miller et. al's model, our agents are able to communicate to each other using a series of tokens, as described above. Note that the tokens the agents are sending back and forth do not map to any particular values or meanings, so it is up to the agents to decode these tokens and make a decision based on the value of their opponent's token. The only message that is clear to both agents is the null token, which gets sent when the agent has locked in their final play of either cooperate or defect for the current round.




![Three-state and three-token automaton ](https://github.com/phuston/ComplexityFinalProject/blob/master/images/three_states.png "Three-state and three-token automaton")


*Figure 1: Diagram of a three-state and three-token automaton. The gray circles represent which state the agent is in, the arrows represent which state the agent will transition upon receipt of a certain token, and the blue squares indicate what token the agent will send from that state.*


In a single step of the model, all agents compete against all other agents in a single-shot prisoner’s dilemma and their scores are recorded. (Scoring will be discussed in a later section.) After all games have been played, the population goes through steps to evolve and create a new generation. In a tournament-style selection, two agents are randomly selected with replacement from the current population and the one with the higher score is chosen to move onto the next population pool. Next, this chosen agent is copied and there is a 50% chance that a single point in their state automaton is mutated. Since the automaton is comprised of a transition table and action map, one is selected at random with equal probability; there is a 50% chance that one of the states is randomly changed in the agent’s transition table or a 50% chance that one of the tokens that the agent can send from their action map is randomly changed, and the new agent is added to the next population. This concludes a single step of the model and creates a new generation of agents. The model is now ready to step again by having the new population of agents compete against each other. Note that this mechanism of evolution does not ensure that the “best” agent moves on to the next generation.


##### Scoring
The scoring mechanism is similar to many traditional implementations of the prisoner’s dilemma, with the addition of a strong negative impact for indecisive agents. On the whole, an agent on the individual level is primarily self-interested and motivated to tend towards defection. Choosing to cooperate is a risky decision that is easy to take advantage of, so selfishness is naturally the steady state of the system.


If both agents cooperate, they each get 3 points. If both agents defect, they each get 1 point. If one agent defects and the other cooperates, the defecting agent gets 5 points and the cooperating agent gets 0 points. When agents reach the time limit (referred to as the “chat limit”) but have not made a decision to either cooperate or defect, this is deemed “no action.” The punishment for “no action” is a deduction of 5 points from the unprepared agent(s).  If one agent is ready to make a decision (as indicated by their sending of a “done” token) but the other agent is not, the prepared agent gains 2 points while the unprepared agent has 5 points deducted.


| Agent 1             | Agent 2   | Payout 1 | Payout 2 |
|---------------------|-----------|----------|----------|
| Cooperate           | Cooperate | 3        | 3        |
| Defect              | Defect    | 1        | 1        |
| Defect              | Cooperate | 5        | 0        |
| Cooperate or defect | No action | 2        | -5       |
| No action           | No action | -5       | -5       |
*Table 1: Demonstrating the payouts of all resulting agent-to-agent interactions. The agents are interchangeable here.*


##### Results
Using this model, we ran the experiment with four allowed states and two communication tokens. The result from this experiment is the graph below that depicts the proportion of mutually cooperative games over 5000 generations. The plot shows the average conversation length (number of times the agents sent tokens back and forth before settling on a final decision to cooperate of defect) for the same generation. 


!["Cooperation..." punchline graph](https://github.com/phuston/ComplexityFinalProject/blob/master/graphs/4state2token.png "Proportion of mutually cooperative games through generations")


*Figure 2: Results from experiment replicating the results of Miller et. al, showing qualitative similarities in the behavior. See below for the figure created by Miller et. al.*


Note that each spike in cooperation is accompanied by a similar increase in the average conversation length for that generation. This highlights the connection between the ability of the agents to communicate, and the emergent phenomena of mutual cooperation.


Miller et. al ran a very similar experiment with four automaton states and two communication tokens, and the results reflect a very similar pattern. We used this as confirmation that our model was implemented correctly, and was producing the expected output. 


![Miller et. al punchline graph](https://github.com/phuston/ComplexityFinalProject/blob/master/images/generation_cooperation.png "Miller et. al punchline graph")


*Figure 3: Results from Miller et. al - Proportion of mutually cooperative games per generation over 5000 generations*


We ran the same experiment with a sweep of the parameters that determine the number of states in the agents’ automata and the number of tokens they could use to communicate. This resulted in a series of graphs that tended to exhibit the same behavior described above.  The population experienced very high levels of defection, but there were intermittent periods where the levels of both communication and cooperation spike to very high levels, only to return to high levels of defection again.  These spikes occurred a few times over the span of thousands of generations, but as the number of allowed states and tokens increased, both the number of spikes and the levels of cooperation increased as well. The results of one of these such experiments is shown below. Note that this setup has the parameters set at four automaton states and two communication tokens.


The existence of any amount of high cooperation in the prisoner’s dilemma is initially counterintuitive, as it is in each agent’s best interest to defect to avoid losing all points in the event that their opponent defects, and to maximize their points if their opponent cooperates. Upon further investigation, evolving strategies of agent behavior that compete against each other emerge. This complex interplay was described by Miller et. al. Initially, the dominant strategy is for all agents to defect. Eventually, agents emerge that communicate and cooperate in response to communication, but defect if the opposing agent doesn’t communicate. These communicating agents perform better than agents that only defect because they receive more points from cooperating with each other than they would get if they both defected, causing more of the communicating agents to be inserted into future generations.  However, the high levels of cooperation die out quickly because the communicating agents are easily taken advantage of by an agent that communicates but then defects, causing the population to revert back to high levels of defection.  These periods are short-lived because the fairly high levels of mutation cause agents to frequently change, and a single mutation to a communicating and cooperating agent could make it a communicating and defecting agent.


The amount of communication and cooperation increases as we allow more states and tokens to exist in the agents’ automata without changing the number of decision states, but we do not know why this occurs.  Miller et. al suggests that it is a result of the increased complexity of the agents’ language.  We investigate this behavior through extensions and characterizing the traits of the agents.


![Miller et. al punchline graph 2](https://github.com/phuston/ComplexityFinalProject/blob/master/images/4_token_graph.png "Miller et. al punchline graph 2")


*Figure 4: Cooperative epochs as a function of number of automaton states and number of communication tokens*


As an extension to the work done by Miller et. al, we further investigate the process by which agents move from one generation to the next in order to explore how to create higher levels of cooperation between agents. To do this, we ran the model while varying the mutation rate parameter used to determine the chance that the “better agent” selected mutates before being placed into the new population. Using the same standard setup of four automaton states and two communication tokens, we ran a sweep of the mutation rate from 0 to 0.7 with a step size of 0.1. We ran each experiment for 100,000 generations to smooth out irregularities, computed the average number of cooperative generations per 1,000 generations for each mutation rate, and plotted the two against each other. This graph is seen here: 


![Cooperation as a function of mutation graph 2](https://github.com/phuston/ComplexityFinalProject/blob/master/graphs/cooperationvsmutation.png "Cooperation as a function of mutation")


*Figure 5: Cooperation as a function of agent mutation rate*


From this graph, we can see that the mutation rate has a direct effect on the cooperation dynamics of the population of agents. At very low mutation rates, the original population isn’t able to mutate into communicating agents, and very little (or no) cooperation emerges. As the mutation rate increases, agents gain the ability to mutate their states into communicating and cooperating agents. This trend continues to the peak, after which the cooperation rates take a downward trajectory. A possible explanation of this is that with high mutation rates, as soon as agent develop into communicating and cooperating states, a chance of a destructive mutant emerging is much higher with a higher chance to mutate. As soon as a cooperative generation appears, it can be taken advantage of by a single ‘virus’ agent that learns to take advantage of the cooperation. The takeaway from this experiment is that the optimal mutation rate to encourage as much cooperation as possible lies somewhere in the domain of a 20% to 30% mutation rate between generations.


In addition, we extended the original model by changing the means of communication from finite state automata to Turing tapes.  The original selection method for agents and functions remains the same.  The only changes made were with regards to how agents communicate.  Each agent was changed to have their own internal rule table and action map, where the rule table prescribes what an agent should write to its position on the tape, which direction it moves, and what state it changes to based on its current state and input token from the agent it communicated with.  For each round of agents playing, two agents are placed on random locations of a Turing tape, and they are allowed to write to and move around the tape.  For each step of communication, the two agents send each other a token, based on what they read from the tape and the corresponding action from their action map.  The agents then write to the tape, move, and update their state unless they have already made a decision, in which case they stay in place and repeatedly send null tokens.


Our Turing tape model yields results that contrast with the results from our main experiment.  Namely, cooperative spikes in our Turing tape results do not seem to be strongly related to the number of states and tokens agents are allowed to have.  We have not sufficiently investigated the reasons for these results to draw any concrete conclusions for this behavior.  However, the graphs from the Turing tape show the relationship between cooperation and communication more distinctly than our original model, as the spikes in cooperation line up with visible spikes in communication.


!["Turing Tape Implementation" punchline graph 2](https://github.com/phuston/ComplexityFinalProject/blob/turing/graphs/turing4state4token.png "Turing Tape Four States Four Tokens")


*Figure 6: Results from a model implementation utilizing Turing tapes for communication, with four agent states and four communication tokens*


#### Conclusion
To reiterate, we create a model that assess cooperation between two agents playing a prisoner’s dilemma game depending on how much or how little they implement communication. Our model shows that despite agents receiving the best payout if they acted selfishly, agents occasionally tend towards cooperating with their communicating pairs. This answers our motivating question because it demonstrates that communication can result in unlikely situations, and as a result, agents can choose a mutually beneficial decision instead of acting only in their best interest.


#### Future Work
An additional experiment that we thought about but did not have time to implement in this project is experimentation with different “games” or general interactions between agents. This is inspired by the first parts of Miller et. al’s work describing and developing a general framework for this type of communication-injected agent-based model. Another possible extension is described by Miller et. al about agents being able to "tag" one another, that is, to determine who the other agent is based on some characteristic communicated when they send their information.


A final extension of our work would be to further investigate the mechanisms of selection to see how varying other parameters affect the characteristics of the population over time. One such parameter is the number of agents selected and compared out of each population when creating a new population. By default, two agents are selected, compared, and the better one moves on, but this is entirely variable. Selecting a higher number of agents to choose from would tend to create a fitter new population, which may affect the dynamics of the population over time. We implemented a sweep to test out the characteristics of communication and cooperation over time as a function of this selection number, but ultimately ran into the limitations of computational power and time. 


#### Annotated Bibliography

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Batty, Michael. "Building a Science of Cities." *Cities* 29 (2012): S9-S16. *ScienceDirect*. Web. 31 Oct. 2016. In this paper, the author argues that our understanding of cities is transformed by the influence of complexity science. This serves to review the background and history of city science by explaining how complexity science has challenged traditional notions of the characteristics of cities. The main argument made is that cities are more like organisms than they are machines.


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Batty, Michael. "The Size, Scale, and Shape of Cities." *Science* 319.5864 (2008): 769-71. Web. 31 Oct. 2016. This paper argues for a new kind of understanding of how cities work - a distinct move away from the historical rudimentary efforts to explain their development and growth in clean, compartmentalized rulesets. Instead, the author argues that cities exhibit many characteristics of living, complex systems - they are emergent, far from equilibrium, require enormous energy to maintain themselves, display patterns of inequality spawned by agglomeration and competition, and appear to be barely sustainable but paradoxically resilient networks. Thinking about cities through this new lens opens up an entire new world of city network analysis and research, and the author goes on to highlight some key findings that we are well familiar with - Schelling, Barbasi, and many more. The references include great resources on city modeling with agents, CAs, and much more.


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Miller, Butts, Rode. "Communication and Cooperation" SFI WORKING PAPER: 1998-04-037 (1998) In this paper, Miller, Butts, and Rode explored the construct of communication to the organization and operation of agent-based systems. The focus on the application of communication to a single-shot prisoner's dilemma scenario shows that a cooperative behavior emerges. Their naive hypothesis was that communication would not affect the behavior of the agents - that always defecting is the optimal behavior, but this is disproven in the results of the model, as a worldwide cooperative behavior emerges through a constantly evolving society.


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Miller, Moser. "Communication and Coordination" SFI WORKING PAPER: 2003-03-019 (2003) In this paper, Miller and Moser further explore applications of the agent-based communication framework described in "Communication and Cooperation," but applied to a coordination-based game, Stag Hunt. Through the development of a model that borrows many of the same structure and principles as in "Communication and Cooperation," Miller and Moser show that brief spikes of coordinated behavior occur when agents are allowed to communication, which directly defies the expectation of the stable state of Stag Hunt.


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Yang, Yong, and Ana V. Diez Roux. "A Spatial Agent-Based Model for the Simulation of Adults' Daily Walking Within a City." *American Journal of Preventive Medicine* 40.3 (2011): 353-61. *ScienceDirect*. Web. 31 Oct. 2016. This paper uses an agent-based approach to model walking behaviors of different agents. Each agent has characteristics including “age, SES, walking ability, attitude toward walking and a home location.” The goal of this paper is to use the model to determine if socio-economic status and environmental status affect the walking behavior of citizens. Two expansions upon this model, as outlined in the discussion are (1) including gender differences and (2) allowing for the combination of trips instead of making each trip begin and end at home or work.


