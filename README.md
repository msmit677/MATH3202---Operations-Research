# MATH3202-Operations-Research
Optimisation of a power grid using Gurobi packages. This specific	project	is in response to a hypothetical client, 'ElectriGrid',	who are an	energy	company	that	supplies	electricity	
to a	region. At the beginning of the project, the client sent through data for the locations of the 50 nodes in the region and their corresponding demands along with the arcs connecting nodes together. 
The client also provided the node locations of the four generators that were being implemented to power the grid and their corresponding costs to run ($/MWh) and capacity (MW). Therefore, the aim of this project was to minimise the total
cost of power required to meet the demands of each node in the grid. This assignment was broken up into 5 communications, which were all released at different times.

- Communication 1: the optimal cost was found in response to the node, arc and generator costs outlined in the preamble
- Communication 2: the client outlined that the transmission lines (arcs) lose electricity along them, at 0.1%/km. The new optimal cost was then found
- Communication 3: transmission lines capacities were introduced for some of the arcs. The new optimal cost was then found
- Communicaiton 4: the demands for each node were broken up into 6 4-hour time periods throughout the day to model realistic behaviour in a typical day. The new optimal cost was then found
- Communication 5: the client stated that the change in power output from a generator cannot exceed a certain amount from one period to another. The new optimal cost was then found

The results from all communications ae provided in the pdf file attached.
