# Game of Life
 Conway's Game of Life written in Python, with some more features.

 I originally created this project in SkillStruck during Computer Science I class.
 To avoid limitations of SkillStruck and continue expanding on the code,
 I transfered this code to my personal computer to continue it. 

 This version of the Game of Life has:
 - [x] Control of simulation/tick speed
 - [x] Playing the simulation
 - [x] Stepping the generation forward one by one
 - [x] Tooltips for alive cells
 - [x] Generation/population counter
 - [x] Complex Mode
 - [ ] Generation history/undoing (saves up to 50 previous generations)
 - [ ] Rainbow cheat code (for fun!)

 Possible goals for this system:
 - [ ] Infinite/bigger grid using quadtrees

 # Complex Mode
 Complex Mode can be toggled on or off by pressing R while the simulation is not running.

 In Complex Mode, the game will specify before a generation update what caused the cell to generate,
 displaying what rule kicked in to cause the cell to change. These are considered transition states, 
 and they can be solitude, overpopulation, or population.

 In order to do this, Complex Mode runs a "half generation". This means that the program
 first shows the cells in their transition states, which were stated above.
 It then runs once more and shows the same scene, except without transition states.

 It's a little overkill, but it's very interesting to look at and also adds some color to the simulation.
 I would suggest lowering the tick speed for this mode so that the half generations don't disappear too quickly.