# Tasks attempted

Move robot along corridor without straying past the walls

Find its way out of the maze

Escape the maze by the fastest possible route

Find the quickest route out of the maze

Map the maze

Return to home

# How my code works

My code is split into 3 main parts being, how the robot moves, how the robot recognises to avoid dead ends after it has escaped
and returning back to the beginning by the most efficient path possible.

My code starts with initializing some basic variables:
movenumber = 1, so that I am able to keep track of what number move this is that is being made.
ongoing = True, so that I am able to keep the loop going until the robot reaches the exit.
route = [] and positions = [], so that i am able to keep track of the moves the robot makes and the cooirdinates and angle the robot are facing.

Before starting any of the movements I record the starting position as facing forward and activate the pen so it is easy to track where the robots been
and set the robots speed to maximum to make the process faster.

The first move the robot always does is turn to the right as it follows the right wall to solve the maze.
This move is recorded by a function called wayback which is used after every move/turn and cooirdinate and angle to the route and position arrays.

Then the code enters the while loop which runs until the robot has returned back to the start of the maze.
The robot decides to move forwards if there is 230mm of space in front of it and after it will turn to the right,
however if the robot is unable to move forward it will turn to the left.

As well as these main movement features in the main there is also a dead end check a check for a variable called fix and a check after every forward move 
to see if the robot detects red underneath it which means it has reached the end of the maze.

a dead end is checked for after the robot has done its moves for the iteration and it tells that the robot is at a dead end by seeing if its 4 most recent moves are
Left, Left, Left, Right
This only happens if a robot moves into part of the maze where there are 3 walls surrounding it so the only way to turn is behind it
but by continuing to follow the right wall.
If this is detected then a variable called fix will be set to true.

There is an if check ran to see if fix is true after every move forward and inside it checks the current position of the robot and compares it to
all the positions in the positions array other than itself to see if it has visited that cooirdinate before and if the code iterates through all of the
positions and doesnt find a position identical or within 20mm of it then it is recognised as a new position and a function called fix route is called.

Fix route is one of the main two functions responsible for removing the dead ends in order to create the fastest route for the robot.
At the start of it an Xvalue and a Yvalue are set to zero, these variables are used for finding out where the crossroad before the new space was.

A small calculation is then done which looks at the angle that the robot is facing and sets the Xvalue or Y value to either -250 or 250 based on direction.
For example if the robot is facing 0 (forward) then the Yvalue will be set to -250 because the position at the crossroads is 250 less than the current position.
Then after the location of where the crossroads would be is gotten the code iterates through all of the positions the robot has been in order
to find the first time that the robot visited the crossroads space and after finding it it calls a function called destroy route.

The destroyroute functions purpose is to remove the path the robot has taken down the dead end from the route and accomodate for the turn the robot needs to turn
(if it has to sometimes it may already be facing it) so that it can get to the new position.
Three variables are initialized at the start of this function, addturn = "", this variable acts as a way to store the turn the robot will have to make if it needs to.
angle = 720, this variable is used to store the rotation angle that the turn that is being added needs to be (720 is just a random number out of range).
priordirection = positions[i][2], this variable records the angle that the robot was facing during the first time it reached the crossroads.

Then i have quite a few if statements which activate for each of the ways the robot can be facing 0 = forward, 90 = right, 180 = backwards, 270 = left but i also have
360 = forward as well because when the robot turns towards the front it will sometimes be at 360 instead of 0 and this just accomodates for this.
In each of these if statements there is then 2 (sometimes 3) more if statements that measure the current angle that the robot is facing and 
set the angle and add turn variables to match the direction that the robot needs to face to move from the crossroads to the new space.

Then there is a check done to see if the angle has been changed and if it has not and is still 720 then it will be set to continue facing the way it was
at the crossroads as no turn is necessary as the first way it was facing when it reached the crossroads is the corrrect way to head.
After this check the route and positions arrays are then trimmed so that they stop at the first instance of the crossroad, this is what removes the dead end from the route.

Then there is a check to make sure that the route is greater or = to 1 in length to avoid messing up the route order if the starting point happens to be a crossroad.
Then if the angle is not 720 so then a turn will be added to route and positions and I made it so it will print out the turn that has been added, 
this was for tracking and debugging as I was having trouble with the robot turning the wrong way whilst developing it.
After a turn is added if it needs to be a move forward is also added to the route and positions this represents the move forward from the crossroads to the correct route.

After this the new complete correct route up to the point the robot has gotten is printed out which helps see if the dead ends have been successfully removed.
This will then continue to happen until the robot has reached the exit tile in the maze.
When the robot has reached the end of the maze in most cases it will have been down multiple dead ends and removed them correctly from the route and added in correct
moves to properly adjust it from the crossroads into the next correct path.

When the robot detects the exit, it will print out "Solved" and it will then call a function called clean_route, the purpose of this function is to create the fastest
route possible for the robot to and from the exit.
It does this by looking for turns where the robot was mapping the maze for the first time and it turned right then left putting it back to the position it was originally in.
If it sees instances of this it removes these from the route meaning that the route that this function produces is one without the pointless right then left turns the
robot makes when it first scans the maze.


After the clean function has looked through the whole route and returned the new version of the route it is printed out and then the final retreat function is called.
The retreat function starts by setting the pen to green so that the robot can make the quickest path visible and then it reverses the route and inverts the turns so that
RIGHT becomes LEFT and LEFT becomes RIGHT and this will run until the robot reaches the starting space again and then the program finishes.


# References

### Source used to learn about the robots basic movements and how it works: 

https://education.vex.com/stemlabs/cs/cs-level-1-vexcode-vr-blocks

This source was how I first learnt the basics of vexcode vr and by following the tutorials on here I was able to learn the basics of how to program the robot.

### Source used to learn about maze solving algorithm: 

https://arcbotics.com/lessons/maze-solving-home-lessons/

This source was what made me decide to use the wall follower algorithm as it explained it very well and illustrated it very well with an easy for me to understand video
which allowed for me to understand how I could program the robot to do this.

### Source used to learn about alternate maze solving methods: 

https://www.algosome.com/articles/maze-generation-depth-first.html

This source helped me consider my options for how I could make the robot solve the maze and I considered the option of doing a more depth search oriented maze algorithm,
however I decided to go against this as the wall algorithm I found seemed like a better and more manageable algorithm for this project.

### Source used to learn about tremaux algorithm and how to deal with dead ends and junctions:

https://www.flyingcoloursmaths.co.uk/dictionary-of-mathematical-eponymy-tremauxs-algorithm/

This source is quite short however it taught me about tremauxs algorithm for solving mazes and although I didnt implement it exactly how it is talked about in this source
I based the way that my robot deals with dead ends based on this. 
Tremaux algorithm places markers for every space in the maze it visits and my maze uses this through the positions array and using this concept of storing a previous
positions is what allowed for me to create my fixroute and destroyroute functions.

# AI Transparency Statement: 

I confirm that I have used no AI in the preparation of completion of my assessment, my submission aligns with AITS 1 of the Artificial Intelligence Transparency Scale.

