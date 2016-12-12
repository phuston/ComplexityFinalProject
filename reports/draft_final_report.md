## Investigating Agent-to-Agent Communication in Agent-Based Models
Patrick Huston, Meg McCauley, Andrew Pan | Fall 2016
Updated December 8th, 2016


### Abstract
In this project, we investigate how communication affects the behavior of agents in an agent-based model that requires cooperation, primarily through play of the prisoner's dilemma. The impetus for this idea comes from a paper from the Santa Fe Institute, "Communication and Cooperation." Through the replication of a model described in the paper, we create a model that demonstrates emergent generations of mutual cooperation through agent communication. This result contradicts our expectation based on the the prisoner's dilemma ruleset, which encourages defection for maximum individual payoff. 


### Experiments
The motivating question in our first experiment is to determine whether the introduction of a communication framework creates conditions like those described in the paper “Communication and Cooperation.” Particularly, we are interested in determining whether or not communication and mutual cooperation will emerge in a system that naturally tends towards mutual defection.


In order to answer this question, we replicated an experiment described in the paper "Communication and Cooperation" which details agent-to-agent communication and decision making using an evolving prisoner's dilemma situation and communication between agents. As in the paper's model, our agents are able to communicate to each other using a series of numbers (called tokens).


Our model is composed of a set number of agents, each of which contain an automata that determine its actions and decisions during play. The automata is composed of two parts. The first is a transition table, which maps an agent’s current state and the token they receive to a new state. The second part is an action map, which maps the agent’s current state to an action, either the sending of a token in the discrete set {1, 2, ... T} (where T is the number of allowed tokens), or deciding on an action (cooperate or defect), and sending the null token, 0. Together, these two structures define an agent’s behavior in the system. 


In a single step of the model, all agents compete against each of the other agents in their generation once and their scores recorded. (Scoring will be discussed in a later section.) There are two steps to determine which agents move on to the next generation. First, two agents are randomly selected from the current population and the one with the higher score is chosen to move onto the next population pool. Next, this chosen agent is copied and there is a 50% chance that it is mutated in one of two ways: there is a 50% chance that one of the states is randomly changed in the agent’s transition table or a 50% chance that one of the tokens that the agent can send from their action map is randomly changed. This concludes a single step of the model and creates a new generation of agents. The model is now ready to step again by having the new population of agents compete against each other.


#####Scoring


If both agents cooperate, they each get 3 points. If both agents defect, they each get 1 point. If one agent defects and the other cooperates, the defecting agent gets 5 points and the cooperating agent gets 0 points. When agents reach the time limit (referred to as the “chat limit”) but have not made a decision to either cooperate or defect, this is deemed “no action.” The punishment for “no action” is a deduction of 5 points from the unprepared agent(s).  If one agent is ready to make a decision (as indicated by their sending of a “done” token) but the other agent is not, the prepared agent gains 2 points while the unprepared agents has 5 points deducted.


Note that the tokens that the agents are sending back and forth do not map to any particular values or meanings, so it is up to the agents to decode these tokens and make a decision based on the value of their opponent's token. The only message that is clear to both agents is the "done" token, which gets sent when the agent has locked in their final play for the game.


| Agent 1             | Agent 2   | Payout 1 | Payout 2 |
|---------------------|-----------|----------|----------|
| Cooperate           | Cooperate | 3        | 3        |
| Defect              | Defect    | 1        | 1        |
| Defect              | Cooperate | 5        | 0        |
| Cooperate or defect | No action | 2        | -5       |
| No action           | No action | -5       | -5       |
We ran our model with a variety of changes to the number of states in the agents’ automata and the number of tokens they could use. This resulted in multiple graphs that tended to exhibit the same behavior.  The model had very high levels of defection, but there were intermittent periods where the levels of both communication and cooperation would increase to very high levels, only to return to high levels of defection again.  These spikes occurred a few times over the span of thousands of generations, but as the number of allowed states and tokens increased, both the number of spikes and the levels of cooperation increased as well.


!["Cooperation..." punchline graph](https://github.com/phuston/ComplexityFinalProject/blob/master/graphs/4state2token.png "Proportion of Mutually Cooperative Games through Generations")
Figure 1: Proof of our replication of the Miller, et al. results.


!["Cooperation..." punchline graph](https://github.com/phuston/ComplexityFinalProject/blob/master/images/generation_cooperation.png "Cooperation punchline graph")

Figure 2: The cooperation graph from Miller, et al.


The existence of any amount of high cooperation in the prisoner’s dilemma is counterintuitive, as it is in each agent’s best interest to defect to avoid losing all points in the event that their opponent defects, and to maximize their points if their opponent cooperates.  A reason for this behavior was described in the “Communication and Cooperation” paper as agents that communicated would eventually develop a “handshake” of tokens they would send each other and cooperate with agents that communicated while defecting against agents that didn’t communicate. The communicating agents perform better than agents that only defect because they receive more points from cooperating with each other than they would get if they both defected, causing more of the communicating agents to be inserted into future generations.  However, the high levels of cooperation die out quickly because the communicating agents are easily taken advantage of by an agent that communicates but then defects, causing the population to revert back to high levels of defection.  These periods are short-lived because the fairly high levels of mutation cause agents to frequently change, and a single change to a communicating and cooperating agent could make it a communicating and defecting agent.


We also noticed that the amount of communication and cooperation increases as we allow more states and tokens to exist in the agents’ automata without changing the number of decision states, but we currently do not know why this occurs.  The “Communication and Cooperation” paper suggests that it is a result of the increased complexity of the agents’ language, but we hope to gain better insights as to why this occurs through extensions and characterizing traits of the agents.


!["Cooperation..." punchline graph 2](https://github.com/phuston/ComplexityFinalProject/blob/master/images/4_token_graph.png "Cooperation punchline graph 2")

Figure 3: Correlation between the complexity of the language and the amount of emergent cooperation


### Extensions
We are continuing to extend our implementation of the model by adding more metrics by which to measure data, such as graphing how the number of cooperative generations in a run of the model changes as we edit the parameters for communication, and characterizing the transition tables of our agents to better understand how certain agents will tend to communicate.  We are also working on different implementations of communication to see if any different behaviors will emerge with the usage of a Turing machine instead of a state automata.


A possible extension is described in the paper about agents being able to "tag" one another, that is, to determine who the other agent is based on some characteristic communicated when they send their information.


### Future Work
An additional experiment that we thought about but will not have time to implement in this project is experimenting with different 'games' or general interactions between agents, as first parts of the “Communication and Cooperation” paper describe and develop a general framework for this type of communication-injected agent-based model.


### Learning Goals and Reflections


##### Meg


My learning goal for the second half of the semester is to become more familiar with one of the models that we have covered in class. I am most interested in learning more about cellular automatons or agent-based models. I want to be able to implement one of these models in a more “from scratch” way so that I can have a deeper understanding of everything that goes into implementing such a model. This project will help me achieve this learning goal by giving me a hands-on experience writing code about an agent-based modeling system. By iterating and experimenting on the base implementations provided from the papers we have read, I will be able to adjust each of the parameters from the bottom up, allowing me to have a more complete understanding of what the behavior of the model will look like when it is implemented.


Reflection:
Through this project I was able to learn more about both agent-based models and cellular automatas. My team did implement this model from scratch, using the Mesa Python package and tutorials to guide the structure of our code. I do believe that implementing the model on our own was a great way for me to further understand the model. As we adjusted the parameters of finite state machine size and number of tokens, I was able to see into the inner workings of the model’s behavior, which was very interesting and a valuable learning experience as well.


##### Andrew


My learning goal for the remainder of the class is to create an agent-based model that involves a simulation of some sort of social interaction.  Our project is focused on the dynamics of communication between agents, and by recreating models from the papers we read as research for this project I will gain experience in both designing and implementing an agent-based model.  I haven’t created an agent-based model completely from the ground up before, so being able to practice through recreating experiments and actually determining what aspects to model as design decisions would be a substantial learning experience.


Reflection:
After working on implementing our model from the ground up, I feel that I have a much stronger understanding of and intuition for designing a model.  I am more confident in my ability to investigate a problem by creating a model of the system to find unique emergent behaviors, and I feel that I have uncovered a personal interest in further working with agent-based models of social interactions.


##### Patrick


My learning goal for the second half of the semester is to work on a project that investigates and explores something new and useful. To achieve this, I plan on being diligent in researching the work that has been done in the area we’re working in, and making sure that we’re not just spending the entire semester replicating existing results in a boring way. Along these lines, I’d like to get better at quickly scanning and analyzing research papers - getting to the punchline of ‘why does this matter’ and ‘is this legit’ in a short amount of time. If the results are compelling, I want to get better at being able to look at the implementation described, and get a good idea of how I could recreate a similar model, and make intelligent and reasoned decisions about whether it makes sense to replicate at all.


Reflection:
Working on this project has been a great experience in inciting further interest in complexity science and modeling in general. In our initial research and in the last parts of the class, which involved a lot of reading and scanning research papers quickly, I felt like I got a better intuition for what papers were strong and grounded, and which were missing some key ‘so what?’ components. Our project started out a little shaky, but with the model we ended up implementing, I’ve gained a lot of really valuable experience in implementing a model to investigate a motivating question. Throughout the process, we also put a lot of work into debugging, which a very useful skill to have in a modeling context.




### Annotated Bibliography


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Miller, Butts, Rode. "Communication and Cooperation" SFI WORKING PAPER: 1998-04-037 (1998) In this paper, Miller, Butts, and Rode explored the construct of communication to the organization and operation of agent-based systems. The focus on the application of communication to a single-shot prisoner's dilemma scenario showed that a cooperative behavior emerged. Their naive hypothesis was that communication will not affect the behavior of the agents - that always defecting is the optimal behavior, but this is disproven in the results of the model, as a worldwide cooperative behavior emerged through a constantly evolving society.


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Miller, Moser. "Communication and Coordination" SFI WORKING PAPER: 2003-03-019 (2003) In this paper, Miller and Moser further explored applications of the agent-based communication framework described in "Communication and Cooperation," but applied to a coordination-based game, Stag Hunt. Through the development of a model that borrows many of the same structure and principles as in "Communication and Cooperation," Miller and Moser showed that brief spikes of coordinated behavior occur when agents are allowed to communication, which directly defied the expectation of the stable state of Stag Hunt. 


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Batty, Michael. "Building a Science of Cities." *Cities* 29 (2012): S9-S16. *ScienceDirect*. Web. 31 Oct. 2016. In this paper, the author argued that our understanding of cities is transformed by the influence of complexity science. This served to review the background and history of city science by explaining how complexity science has challenged traditional notions of the characteristics of cities. The main argument made is that cities are more like organisms than they are machines.


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Batty, Michael. "The Size, Scale, and Shape of Cities." *Science* 319.5864 (2008): 769-71. Web. 31 Oct. 2016. This paper argued for a new kind of understanding of how cities work - a distinct move away from the historical rudimentary efforts to explain their development and growth in clean, compartmentalized rulesets. Instead, the author argued that cities exhibit many characteristics of living, complex systems - they are emergent, far from equilibrium, require enormous energy to maintain themselves, display patterns of inequality spawned by agglomeration and competition, and appear to be barely sustainable but paradoxically resilient networks. Thinking about cities through this new lens opens up an entire new world of city network analysis and research, and the author went on to highlight some key findings that we are well familiar with - Schelling, Barbasi, and many more. The references include great resources on city modeling with agents, CAs, and much more.


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Yang, Yong, and Ana V. Diez Roux. "A Spatial Agent-Based Model for the Simulation of Adults' Daily Walking Within a City." *American Journal of Preventive Medicine* 40.3 (2011): 353-61. *ScienceDirect*. Web. 31 Oct. 2016. This paper used an agent based approach to model walking behaviors of different agents. Each agent had characteristics including “age, SES, walking ability, attitude toward walking and a home location.” The goal of this paper was to use the model to determine if socio-economic status and environmental status affected the walking behavior of the citizens. Two expansions upon this model, as outlined in the discussion are (1) include gender differences and (2) allow for the combination of trips instead of making each trip begin and end at home or work.
