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
 - [x] Generation history/undoing & redoing (saves up to 75 previous generations)
 - [x] Camera
 - [x] Theoretically infinite grid

 # Controls:
 **R - Complex Mode**
 LMB - Place/Destroy Cell
 RMB - Start Simulation
 MMB - Step/Tick Simulation
 Scroll - Change Tick Speed
 CTRL + Z - Undo
 CTRL + Y - Redo

 # Complex Mode
 Complex Mode can be toggled on or off by pressing R.

 In Complex Mode, the game will specify before a generation update what caused the cell to generate,
 displaying what rule kicked in to cause the cell to change. These are considered transition states, 
 and they can be solitude, overpopulation, or population.

 In order to do this, Complex Mode runs a "half generation". This means that the program
 first shows the cells in their transition states, which were stated above.
 It then runs once more and shows the same scene, except without transition states.
 Keep in mind that these half generations are saved and do count towards the history limit. 

 It may be a little overkill, but it's a very great visualization to look at when trying to understand
 changes in the simulation, and it adds some color. 