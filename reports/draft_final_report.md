### Investigating Agent-to-Agent Communication in Agent-Based Models
Patrick Huston, Meg McCauley, Andrew Pan | Fall 2016
Updated November 15, 2016

#### Abstract
In this project, we investigated how communication affects the behavior of agents in an agent-based model that requires cooperation, primarily through play of the prisoner's dilemma. The impetus for this idea comes from a paper from the Santa Fe Institute, "Communication and Cooperation". Through the replication of a model described in the paper, we were able to create a model that demonstrated emergent generations of mutual cooperation through agent communication, which defies the expectation of the prisoner's dilemma ruleset, which encourages defection for maximum payoff. 

##### Annotated Bibliography

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Miller, Butts, Rode. "Communication and Cooperation" SFI WORKING PAPER: 1998-04-037 (1998) In this paper, Miller, Butts, and Rode explore the construct of communication to the organization and operation of agent-based systems. Focusing on the application of communication to a single-shot prisoner's dilemma scenario, it is shown that a cooperative behavior emerges. Their naive hypothesis is that communication will not affect the behavior of the agents - that defecting always is the optimal behavior, but this is disproven in the results of the model, as a worldwide cooperative behavior emerges through a constantly evolving society.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Miller, Moser. "Communication and Coordination" SFI WORKING PAPER: 2003-03-019 (2003) In this paper, Miller and Moser explore further applications of the agent-based communication framework described in "Communication and Cooperation", but applied to a coordination-based game, Stag Hunt. Through the development of a model that borrows many of the same structure and princples as in "Communication and Cooperation", Miller and Moser show that brief spikes of coordinated behavior occur when agents are allowed to communication, which directly defies the expectation of the stable state of Stag Hunt. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Batty, Michael. "Building a Science of Cities." *Cities* 29 (2012): S9-S16. *ScienceDirect*. Web. 31 Oct. 2016. In this paper, the author argues that our understanding of cities is being transformed by the influence of complexity science, and serves to review the background and history of city science, explaining how complexity science has challenged traditional notions of the characteristics of cities. The main argument made is that cities are more like organisms than they are machines.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Batty, Michael. "The Size, Scale, and Shape of Cities." *Science* 319.5864 (2008): 769-71. Web. 31 Oct. 2016. This paper argues for a new kind of understanding of how cities work - a distinct move away from the historical rudimentary efforts to explain their development and growth in clean, compartmentalized rulesets. Instead, the author argues that cities exhibit many characteristics of living, complex systems - they’re emergent, far from equilibrium, require enormous energy to maintain themselves, display patterns of inequality spawned by agglomeration and competition, and appear to be barely sustainable but paradoxically resilient networks. Thinking about cities through this new lens opens up an entire new world of city network analysis and research, and the author goes on to highlight some key findings that we’re well familiar with - Schelling, Barbasi, and many more. Be sure to check out the references for some great resources on city modeling with agents, CAs, and much more.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Yang, Yong, and Ana V. Diez Roux. "A Spatial Agent-Based Model for the Simulation of Adults' Daily Walking Within a City." *American Journal of Preventive Medicine* 40.3 (2011): 353-61. *ScienceDirect*. Web. 31 Oct. 2016. This paper uses an agent based approach to model walking behaviors of different agents. Each agent has characteristics including “age, SES, walking ability, attitude toward walking and a home location.” The goal of this paper is to use the model to determine if socio-economic status and environmental status affect the walking behavior of the citizens. Two expansions upon this model, as outlined in the discussion are (1) include gender differences and (2) allow for the combination of trips instead of making each trip begin and end at home or work.

#### Experiments
1. We replicated an experiment done in the paper "Communication and Cooperation" describing agent to agent communication and decision making, with an evolving prisoner's dilemma situation and communication between agents. As in the paper's model, our agents will be able to communicate to each other using a series of numbers that are not pre-assigned to any particular message. It is up to the agents to decode the messages that are being passed back and forth between them. The only message that is clear to both agents is the "done" message, which gets sent when the agent has locked in their final play for the game. There is also a time limit, referred to as the "chat limit" by which point both agents must have sent their "done" 0 tokens. The punishment for not being prepared to make a final decision is a deduction of 5 points.


The purpose of our experiment was to replicate and verify the results of the main experiment conducted in “Communication and Cooperation” paper, to show a correlation between high levels of both communication and cooperation that would occur for short spans of time. Without the ability to communicate, agents would be expected to play the game with high levels of defection nearly all the time. When communication is allowed, however, this allows for a cooperative phenomena to emerge, and both agents are able to mutually cooperate through increasingly complex communication handshake patterns.


Our model included usage of both agent-based modeling and evolution.  For each step of the model, our set of agents play every other agent in the generation in the prisoner’s dilemma game, communicating with each other by sending tokens that would allow each agent to change the state of its finite state automata.  The agents’ decisions are ultimately dependent on what state of their automata they ended up in, choosing to either cooperate, defect, or take no action.  Once all pairs of agents had played each other, the model creates a new generation through a tournament selection by repeatedly selecting two random agents and adding the one with the highest total score to the next generation, with a chance to mutate their automata or action map (which determined what tokens to send).  The model then repeats the process for the next generation.


#### Extensions
1. A possible extension is described in the paper about agents being able to "tag" one another, that is, to determine who the other agent is based on some characteristic communicated when they send their information. Additionally, we could experiment with different 'games' or general interactions between agents, as first parts of paper describe and develop a general framework for this type of communication-injected agent-based model.

#### Results

1. The following are punchline graphs from "Communication and Cooperation." The first graph shows that there are generally low sustained periods of no communciation, but every once in a while there are high but not sustained periods of communication. These two occurances tend to happen at the same time, as can be seen by the tick marks lining up.
!["Cooperation..." punchline graph](https://github.com/phuston/ComplexityFinalProject/blob/master/images/generation_cooperation.png "Cooperation punchline graph")
The second graph shows that by increasing the number of tokens that agents can use to communicate, the cooperation levels increase. This demostrates that the more options agents have to communicate-the more complex their language skills are-will allow them to communicate more productively and leads to more positive outcomes for both parties.
!["Cooperation..." punchline graph 2](https://github.com/phuston/ComplexityFinalProject/blob/master/images/4_token_graph.png "Cooperation punchline graph 2")

#### Learning Goals

##### Meg

My learning goal for the second half of the semester is to become more familiar with one of the models that we have covered in class. I am most interested in learning more about cellular automatons or agent-based models. I want to be able to implement one of these models in a more “from scratch” way so that I can have a deeper understanding of everything that goes into implementing such a model. This project will help me achieve this learning goal by giving me a hands-on experience writing code about an agent-based modeling system. By iterating and experimenting on the base implementations provided from the papers we have read, I will be able to adjust each of the parameters from the bottom up, allowing me to have a more complete understanding of what the behavior of the model will look like when it is implemented.

##### Andrew

My learning goal for the remainder of the class is to create an agent-based model that involves a simulation of some sort of social interaction.  Our project is focused on the dynamics of a city’s structure and multiple parameters of the residents of the city, and by recreating models from the papers we read as research for this project I will gain experience in both designing and implementing an agent-based model.  I haven’t created an agent-based model completely from the ground up before, so being able to practice through recreating experiments and actually determining what aspects to model as design decisions would be a substantial learning experience.

##### Patrick

My learning goals for the second half of the semester is to work on a project that investigates and explores something new and useful. To achieve this, I plan on being diligent in researching the work that has been done in the area we’re working in, and making sure that we’re not just spending the entire semester replicating existing results in a boring way. Along these lines, I’d like to get better at quickly scanning and analyzing research papers - getting to the punchline of ‘why does this matter’ and ‘is this legit’ in a short amount of time. If the results are compelling, I want to get better at being able to look at the implementation described, and get a good idea of how I could recreate a similar model, and make intelligent and reasoned decisions about whether it makes sense to replicate at all.


