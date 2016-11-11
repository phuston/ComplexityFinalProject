### Investigating Agent-to-Agent Communication in Agent-Based Models
Patrick Huston, Meg McCauley, Andrew Pan | Fall 2016

#### Abstract
You may remember that we were previously planning on investigating how city development and pedestrian traffic levels interact as the population of a city changes. Our plan was to to use agent-based models to represent the individual citizens and create rules for their movement (or lack thereof) based on environmental and other variables that apply to the entire canvas of the city, updating the agents’ respective information with each step. After a week-long foray into this subject, we realized we had failed to really answer the important questions regarding motivation - what are we trying to answer? Why does this matter? 

We have pivoted our project and are now planning on investigating how communication affects the behavior of agents in an agent-based model that requires cooperation, such as the Prisoner's Dilemma. We are basing this experiment on a paper, "Communication and Cooperation" that discusses how allowing communication between agents affects their decisions to defect or cooperate. We are planning on looking into the effects that communication has on the final outcome of the situation, in a variety of contexts.

#### Annotated Bibliography
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Miller, Butts, Rode. "Communication and Cooperation" SFI WORKING PAPER: 1998-04-037 (1998) In this paper, Miller, Butts, and Rode explore the construct of communication to the organization and operation of agent-based systems. Focusing on the application of communication to a single-shot prisoner's dilemma scenario, it is shown that a cooperative behavior emerges. Their naive hypothesis is that communication will not affect the behavior of the agents - that defecting always is the optimal behavior, but this is disproven in the results of the model, as a worldwide cooperative behavior emerges through a constantly evolving society.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Batty, Michael. "Building a Science of Cities." *Cities* 29 (2012): S9-S16. *ScienceDirect*. Web. 31 Oct. 2016. In this paper, the author argues that our understanding of cities is being transformed by the influence of complexity science, and serves to review the background and history of city science, explaining how complexity science has challenged traditional notions of the characteristics of cities. The main argument made is that cities are more like organisms than they are machines.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Batty, Michael. "The Size, Scale, and Shape of Cities." *Science* 319.5864 (2008): 769-71. Web. 31 Oct. 2016. This paper argues for a new kind of understanding of how cities work - a distinct move away from the historical rudimentary efforts to explain their development and growth in clean, compartmentalized rulesets. Instead, the author argues that cities exhibit many characteristics of living, complex systems - they’re emergent, far from equilibrium, require enormous energy to maintain themselves, display patterns of inequality spawned by agglomeration and competition, and appear to be barely sustainable but paradoxically resilient networks. Thinking about cities through this new lens opens up an entire new world of city network analysis and research, and the author goes on to highlight some key findings that we’re well familiar with - Schelling, Barbasi, and many more. Be sure to check out the references for some great resources on city modeling with agents, CAs, and much more.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Caruso, Geoffrey. "Spatial Configurations in a Periurban City. A Cellular Automata-based Microeconomic Model." *Regional Science and Urban Economics* 37.5 (2007): 542-67. *ScienceDirect*. Web. 31 Oct. 2016. This study used a 2D CA to model the growth of an urban city with migration influx and “farmer” units in the CA. The paper found that dense population settling potentially compensates for commuting costs, making the urban area more attractive to encourage more migrants to settle due to a higher utility rating, until the utility of the urban area matches that of the rest of the world in equilibrium.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Yang, Yong, and Ana V. Diez Roux. "A Spatial Agent-Based Model for the Simulation of Adults' Daily Walking Within a City." *American Journal of Preventive Medicine* 40.3 (2011): 353-61. *ScienceDirect*. Web. 31 Oct. 2016. This paper uses an agent based approach to model walking behaviors of different agents. Each agent has characteristics including “age, SES, walking ability, attitude toward walking and a home location.” The goal of this paper is to use the model to determine if socio-economic status and environmental status affect the walking behavior of the citizens. Two expansions upon this model, as outlined in the discussion are (1) include gender differences and (2) allow for the combination of trips instead of making each trip begin and end at home or work.

#### Experiments
##### POST-PIVOT:
0. We are now planning on replicating an experiment done in the paper "Communication and Cooperation" about agent to agent communication and decision making. We are planning on implementing an evolving prisonner's dilemma situation with communication between agents. As in the paper's model, our agents will be able to communicate to each other using a series of numbers that are not pre-assigned to any particular message. It is up to the agents to decode the messages that are being passed back and forth between them. The only message that is clear to both agents is the "done" message, which gets sent when the agent has locked in their final play for the game. There is also a time limit, referred to as the "chat limit" by which point both agents must have sent their "done" messages. The punishment for not being prepared to make your move is a deduction of funds.

##### PRE-PIVOT: 

1. We plan to replicate the experiment done in the paper “A Spatial Agent-Based Model for the Simulation of Adults’ Daily Walking Within a City.” For our first iteration, we plan to implement the same basic properties as outlined in the paper: age, socioeconomic status, walking ability, attitude toward walking, and a home and work location. The movement of the agents will be based on the same three properties in the paper: traveling for work, basic needs, and leisure. For our first iteration, we are going to abstract out the attitude change over time. If all goes well with the first iteration, this will be implemented in the future.

2. We also plan on creating a simplified version of the 2D CA from the paper “Spatial configurations in a periurban city.  A cellular automata-based microeconomic model,” which modeled the growth of an urban city from migration while the utility of locations of the city was higher than that of the rest of the world.  We will likely reduce the number of parameters assigned to consumer/household limits and the complexity of our utility rating for city areas.  From this experiment replication, we hope to gain experience in actually generating a city based on system components (determined by the needs and wants of the residents).

#### Extensions
##### POST-PIVOT:
0. A possible extension is described in the paper about agents being able to "tag" one another, that is, to determine who the other agent is based on some characteristic communicated when they send their information. Additionally, we could experiment with different 'games' or general interactions between agents, as first parts of paper describe and develop a general framework for this type of communication-injected agent-based model.

##### PRE-PIVOT:

1. As part of the conclusion of “A Spatial Agent-Based Model…” the authors suggest follow up experiments that can be done to expand on their results. We are planning on using some of these ideas to implement a more accurate and in-depth model. The extension that we have chosen to focus on from this paper is allowing the walking trips to start and end not just at the agent’s home or work location. The authors suggested that this could be done by adding activity centers where multiple activities can take place.

2. In “Spatial configurations in a periurban city…”, the authors mention that further research from their model could focus on sprawl and sustainability issues.  We would like to consider expanding upon our simpler implementation of their model by continuing to add an influx of migrations after the utility rating of the city is equal to the rest of the world, and determine through factors such as cost of living whether continuing to live in the urban area is sustainable for existing residents.

#### Possible Results

##### POST-PIVOT:
0. The following are punchline graphs from "Communication and Cooperation." The first graph shows that there are generally low sustained periods of no communciation, but every once in a while there are high but not sustained periods of communication. These two occurances tend to happen at the same time, as can be seen by the tick marks lining up.
!["Cooperation..." punchline graph](https://github.com/phuston/ComplexityFinalProject/blob/master/images/generation_cooperation.png "Cooperation punchline graph")
The second graph shows that by increasing the number of tokens that agents can use to communicate, the cooperation levels increase. This demostrates that the more options agents have to communicate-the more complex their language skills are-will allow them to communicate more productively and leads to more positive outcomes for both parties.
!["Cooperation..." punchline graph 2](https://github.com/phuston/ComplexityFinalProject/blob/master/images/4_token_graph.png "Cooperation punchline graph 2")

##### PRE-PIVOT:

1. This is the punchline graph from “A Spatial Agent-Based Model for the Simulation of Adults’ Daily Walking Within a City.” 

!["A Spatial Agent-Based Model..." punchline graph](https://github.com/phuston/ComplexityFinalProject/blob/master/images/punchline_agent_based_walking.png "A Spatial Agent-Based Model..." punchline graph")

After we implement our extension of allowing the starting and ending locations to exist outside of the agents’ home and work locations, our graphs would not separate along the lines of work, basic needs, and leisure so easily. Rather, it might make more sense to graph the amount of time spent or the distance walked between activities to get a more comprehensive look at how the agents are using their time and resources. A pie graph that demonstrates how much of their walking time the agents spend walking to or from one activity would also be useful. This could have separate sections for each of the three current options and then a fourth combined section to determine when the agents are both walking home from work and walking to the grocery store to fulfill a basic need. This graph could look something like this: 

![Possible result pie graph](https://github.com/phuston/ComplexityFinalProject/blob/master/images/possible_results_pie_graph.png "Possible result pie graph")


2. The results from “Spatial configurations in a periurban city…” did not represent the model in an easily-plottable manner, but when we run our simplified version we plan to plot the average utility rating as a function of time.  We can expect the slope of the resulting plot to be negative, but until we conduct our simulation we do not have enough information to create a sketch of the general trend of utility ratings.

#### Learning Goals

##### Meg

My learning goal for the second half of the semester is to become more familiar with one of the models that we have covered in class. I am most interested in learning more about cellular automatons or agent-based models. I want to be able to implement one of these models in a more “from scratch” way so that I can have a deeper understanding of everything that goes into implementing such a model. This project will help me achieve this learning goal by giving me a hands-on experience writing code about an agent-based modeling system. By iterating and experimenting on the base implementations provided from the papers we have read, I will be able to adjust each of the parameters from the bottom up, allowing me to have a more complete understanding of what the behavior of the model will look like when it is implemented.
##### Andrew

My learning goal for the remainder of the class is to create an agent-based model that involves a simulation of some sort of social interaction.  Our project is focused on the dynamics of a city’s structure and multiple parameters of the residents of the city, and by recreating models from the papers we read as research for this project I will gain experience in both designing and implementing an agent-based model.  I haven’t created an agent-based model completely from the ground up before, so being able to practice through recreating experiments and actually determining what aspects to model as design decisions would be a substantial learning experience.

##### Patrick

My learning goals for the second half of the semester is to work on a project that investigates and explores something new and useful. To achieve this, I plan on being diligent in researching the work that has been done in the area we’re working in, and making sure that we’re not just spending the entire semester replicating existing results in a boring way. Along these lines, I’d like to get better at quickly scanning and analyzing research papers - getting to the punchline of ‘why does this matter’ and ‘is this legit’ in a short amount of time. If the results are compelling, I want to get better at being able to look at the implementation described, and get a good idea of how I could recreate a similar model, and make intelligent and reasoned decisions about whether it makes sense to replicate at all. 