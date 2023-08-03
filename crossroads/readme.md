Simulation of traffic at a crossroads
Traffic lights are located at the intersection of two highways. Each of the roads contains several lanes (rows),
cars move in both directions. Traffic lights ensure the passage of cars on both roads, including the left and right turns of cars,
as well as the crossing of these roads by pedestrians.
The program for modeling and visualizing traffic at such an intersection is used to study the nature of traffic occurring at the intersection.
traffic jams and their resorption, depending on the density of car flows and the modes of operation of traffic lights.
Cars must spawn at the ends of each of the roads randomly, drive through them at the speed set when they spawn,
slowing down and stopping if necessary at the intersection, and disappearing after passing the entire road at its opposite end.

Each car can have its own initial speed, it is determined as a random value from a certain range (for example, from 30 to 120 km/h). A random variable is also the interval between the appearance of cars on each road - the range of change of this value (and the law of its distribution) determines the density of the flow of cars. As a random variable determined at the moment the car appears on the road, the direction of its passage through the intersection (straight / left / right) should also be modeled.
Cars must change from one lane to another and cross the intersection in accordance with the rules of the road.

In particular, in the left lane in front of the traffic lights are cars that need to turn left. In addition to the rules for changing lanes, the program should fix the laws of braking and accelerating cars at the intersection, which generally depend on the admissible approach between cars, their speeds, etc. The possibility of accidents (for example, due to violations of traffic rules) in the model may not be taken into account.
The purpose of the simulation is to study the various modes of operation of traffic lights in order to find the mode of their optimal operation.

Two types of operating modes should be considered: static, when the glow intervals of each color (yellow, green, red) are fixed in advance,
and dynamic, in which the glow intervals change in accordance with the number of cars (and pedestrians) waiting to pass (pass) through the road. The changeable parameters of traffic simulation should include: the type of traffic light operation mode, the glow intervals of each color (for the static mode), the visibility distance of the traffic light, the range of possible car speeds, the intervals of random appearance of cars on each of the roads.
The visual picture of traffic at the crossroads should contain images of roads, traffic lights, moving cars. It is useful to display in one way or another (for example, in different colors) the possible directions of movement of the car through the intersection (straight/left/right). It is also desirable to provide for the output of some values ​​calculated during the simulation, for example, the average time for cars to stop at an intersection