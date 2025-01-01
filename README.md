# game of life
 Conway's Game of Life written in Python, with some more features.

 I originally created this project in SkillStruck during class.
 To avoid limitations of SkillStruck and continue expanding on the code,
 I transfered this code to my personal computer to continue it. 

 This version of the Game of Life has:
 - [x] Control of simulation/tick speed
 - [x] Playing the simulation
 - [x] Stepping the generation forward one by one
 - [ ] Tooltips for alive cells
 - [x] Generation/population counter
 - [x] Complex Mode
 - [ ] Undoing generations (history saves 50 generations back!)
 - [ ] Rainbow cheat code (for fun!)

 # Complex Mode
 Complex Mode can be toggled on or off by pressing R.

 In Complex Mode, the game will specify before a generation update what caused the cell to generate.
 It essentially shows you what rule kicked in to cause the cell to change. 
 This can either be solitude, overpopulation, or population.

 In order to do this, Complex Mode runs a "half generation". This means that the program
 first shows the cells in their transition states, which were stated above.
 It then runs once more and shows the same scene, except without transition states.

 It's a little overkill, but it's very interesting to look at and also looks pretty.