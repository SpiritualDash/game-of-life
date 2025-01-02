# Game of Life (Experimental Branch)
 Conway's Game of Life written in Python, with some more features.

 This experimental branch, if added, will add:
 - [ ] Camera
 - [x] Grid without cell initialization

 I'm not sure if I can make the grid bigger, but optimizing and removing the clutter of cells
 that are dead should make it better.

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
 - [x] Generation history/undoing & redoing (saves up to 75 previous generations, half gens are treated as full)

  Possible goals for this system:
 - [ ] Infinite/bigger grid (using quadtrees?)

 # Complex Mode
 Complex Mode can be toggled on or off by pressing R.

 In Complex Mode, the game will specify before a generation update what caused the cell to generate,
 displaying what rule kicked in to cause the cell to change. These are considered transition states, 
 and they can be solitude, overpopulation, or population.

 In order to do this, Complex Mode runs a "half generation". This means that the program
 first shows the cells in their transition states, which were stated above.
 It then runs once more and shows the same scene, except without transition states.

 It's a little overkill, but it's very interesting to look at and also adds some color to the simulation.
 I would suggest lowering the tick speed for this mode so that the half generations don't disappear too quickly.