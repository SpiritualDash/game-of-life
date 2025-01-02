import pygame

pygame.init()

text_font = pygame.font.SysFont("Arial", 18)

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Game of Life")

x, y = screen.get_size() # screen size

# Adjust these to change amount of cells per column & row
HORIZ_CELLS = 60
VERT_CELLS = 60

HORIZ_SIZE = x / HORIZ_CELLS
VERT_SIZE = y / VERT_CELLS

HISTORY_STACK_SIZE = 75

# basic colors
HOVER = (125, 125, 125)
WHITE = (255, 255, 255)

STATUSES = {
    "OVERPOPULATED": (242, 222, 5),
    "SOLITUDE": (255, 0, 0),
    "ALIVE": WHITE,
    "POPULATED": (5, 100, 242),
    "DEAD": (0, 0, 0)
}

STATUS_NAMES = {
    STATUSES["OVERPOPULATED"]: "Overpopulated",
    STATUSES["SOLITUDE"]: "Solitude",
    STATUSES["ALIVE"]: "Alive",
    STATUSES["POPULATED"]: "Populating..."
}

cells = [] 

# Initialize dead units
for i in range(0, HORIZ_CELLS + 1):
    columns = []

    for i in range(0, VERT_CELLS + 1):
        columns.append(STATUSES["DEAD"])

    cells.append(columns)

def GetCell(cursor_x, cursor_y):
    x_index = int(cursor_x / HORIZ_SIZE)
    y_index = int(cursor_y / VERT_SIZE)

    return (x_index, y_index), cells[x_index][y_index]

def GetAmountOfLiveNeighbors(x_index, y_index):
    live_neighbors = 0

    neighbors = []

    for x_increment in range(-1, 2):
        for y_increment in range(-1, 2):
            neighbor_x = x_index + x_increment
            neighbor_y = y_index + y_increment
            
            if neighbor_x < 0 or neighbor_y < 0: continue
            if neighbor_x == x_index and neighbor_y == y_index: continue

            try: 
                neighbors.append(cells[neighbor_x][neighbor_y])
            except IndexError:
                continue

    for neighbor in neighbors:
        if neighbor == STATUSES["ALIVE"]: live_neighbors += 1

    return live_neighbors

def GetPopulation():
    count = 0

    for column in cells:
        for cell in column:
            if cell == STATUSES["ALIVE"] or cell == STATUSES["POPULATED"]:
                count += 1

    return count

def ProcessChanges(gen_changes):
    for change in gen_changes:
        cell_tuple, status = change
        y_ind, x_ind = cell_tuple

        cells[y_ind][x_ind] = status

# for saving actions for the redo/undo stack
def StorePreviousStates(changes, prev_gen, prev_pop, prev_complex):
    previous_states = [(prev_gen, prev_pop, prev_complex)]

    for change in changes:
        y_ind, x_ind = change[0]
        previous_states.append((change[0], cells[y_ind][x_ind]))

    return previous_states

def UpdateGen(generation, population, complex):
    gen_changes = []

    for x, column in enumerate(cells):
        for y, cell in enumerate(column):
            neighbor_count = GetAmountOfLiveNeighbors(x, y)
            cell_tuple = x, y 

            result_status = False

            if generation % 1 == 0:
                if cell == STATUSES["ALIVE"]:
                    if neighbor_count < 2:
                    # Live cell w/ fewer than 2 live neighbours, solitude
                        if complex: 
                            result_status = STATUSES["SOLITUDE"]
                        else:
                            result_status = STATUSES["DEAD"]
                    elif neighbor_count == 2 or neighbor_count == 3:
                    # Live cell w/ 2 or 3 live neighbours, survives to next gen
                        result_status = STATUSES["ALIVE"]

                    elif neighbor_count > 3:
                    # Live cell w/ more than 3 live neighbours, overpopulated
                        if complex: 
                            result_status = STATUSES["OVERPOPULATED"]
                        else:
                            result_status = STATUSES["DEAD"]
                elif cell == STATUSES["DEAD"] and neighbor_count == 3:
                    # Dead cell w/ exactly 3 live neighbours, becomes live cell
                    if complex: 
                        result_status = STATUSES["POPULATED"]
                    else:
                        result_status = STATUSES["ALIVE"]
            else:
                if cell == STATUSES["POPULATED"]:
                    # Make cell live the next generation, complex mode
                    result_status = STATUSES["ALIVE"]
                elif cell == STATUSES["OVERPOPULATED"] or cell == STATUSES["SOLITUDE"]:
                    # Make cell die the next generation, complex mode
                    result_status = STATUSES["DEAD"]

            if result_status:
                gen_changes.append((cell_tuple, result_status))
    
    undo_states = StorePreviousStates(gen_changes, generation, population, complex)
    ProcessChanges(gen_changes)

    new_population = GetPopulation()

    if complex or generation % 1 != 0:
        generation += .5
    else:
        generation += 1

    return generation, new_population, undo_states

def UpdateScreen(generation, population, complex):
    screen.fill((0, 0, 0))

    if pygame.mouse.get_visible():
        x, y = pygame.mouse.get_pos()
        cell_list_pos, status = GetCell(x, y)

        cell_x, cell_y = cell_list_pos
        cell_screen_x, cell_screen_y = HORIZ_SIZE * cell_x, VERT_SIZE * cell_y

        if status == STATUSES["DEAD"]:
            pygame.draw.rect(screen, HOVER, pygame.Rect(cell_screen_x, cell_screen_y, HORIZ_SIZE, VERT_SIZE))
        else:
            stat_display = text_font.render(f"Cell Status: {STATUS_NAMES[status]}", True, status, (0, 0, 0))
            coord_display = text_font.render(f"Coordinates: ({cell_x}, {cell_y})", True, WHITE, (0, 0, 0))

            stat_rect = stat_display.get_rect()
            coord_rect = coord_display.get_rect()

            stat_rect.bottomleft = (x + 5, y + 26)
            coord_rect.bottomleft = (x + 5, y + 5)

            screen.blit(stat_display, stat_rect)
            screen.blit(coord_display, coord_rect)
    
    for x, column in enumerate(cells):
        for y, cell in enumerate(column):
            if cell != STATUSES["DEAD"]:
                pygame.draw.rect(screen, cell, pygame.Rect(HORIZ_SIZE * x, VERT_SIZE * y, HORIZ_SIZE, VERT_SIZE))

    
    # Generation/Population counters
    text_color = WHITE
    
    if complex: text_color = STATUSES["POPULATED"]

    gen_count = text_font.render(f"Generation: {generation}", True, text_color)
    pop_count = text_font.render(f"Population: {population}", True, text_color)

    gen_rect = gen_count.get_rect()
    pop_rect = pop_count.get_rect()
    
    gen_rect.width = 100
    gen_rect.height = 75
    gen_rect.topleft = (0, 0)

    pop_rect.width = 100
    pop_rect.height = 75
    pop_rect.topleft = (0, 20)

    screen.blit(gen_count, gen_rect)
    screen.blit(pop_count, pop_rect)

    pygame.display.flip()

def main():
    # settings
    complex = False
    tick_speed = 100 # in milliseconds

    # simulation properties
    generation = 0
    population = 0
    is_evolving = False

    undo_stack = []
    redo_stack = []

    while True:
        if is_evolving:
            pygame.time.wait(tick_speed)

            generation, population, undo_states = UpdateGen(generation, population, complex)
            undo_stack.insert(0, undo_states)

            if len(undo_stack) >  HISTORY_STACK_SIZE:
                undo_stack.pop()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # L click
                    if is_evolving: continue
                    cell_data_pos, status = GetCell(event.pos[0], event.pos[1])
                    x_index, y_index = cell_data_pos

                    if status == STATUSES["DEAD"]:
                        cells[x_index][y_index] = STATUSES["ALIVE"]
                        population += 1
                    else:
                        cells[x_index][y_index] = STATUSES["DEAD"]
                        population -= 1
                elif event.button == 2: # M click
                    generation, population = UpdateGen(generation, population, complex)
                elif event.button == 3: # R click
                    is_evolving = not is_evolving
                    pygame.mouse.set_visible(not is_evolving)

            # elif event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
            #     cell_data_pos, status = GetCell(event.pos[0], event.pos[1])
            #     x_index, y_index = cell_data_pos

            #     if status == STATUSES["DEAD"]:
            #         cells[x_index][y_index] = STATUSES["ALIVE"]
            #         population += 1
            #     else:
            #         cells[x_index][y_index] = STATUSES["DEAD"]
            #         population -= 1
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    tick_speed = pygame.math.clamp(tick_speed - 10, 5, 250)
                elif event.y < 0:
                    tick_speed = pygame.math.clamp(tick_speed + 10, 5, 250)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    complex = not complex
                elif not is_evolving and event.mod % pygame.KMOD_CTRL:
                    if event.key == pygame.K_y and len(redo_stack) > 0:
                        change_list = redo_stack.pop(0)
                        stats = change_list[0]
                        changes = change_list[1: ]

                        undo_stack.insert(0, StorePreviousStates(changes, generation, population, complex))

                        if len(undo_stack) >  HISTORY_STACK_SIZE:
                            undo_stack.pop()

                        generation = stats[0]
                        population = stats[1]
                        complex = stats[2]

                        ProcessChanges(changes)
                    elif event.key == pygame.K_z and len(undo_stack) > 0:
                        change_list = undo_stack.pop(0)
                        stats = change_list[0]
                        changes = change_list[1: ]

                        redo_stack.insert(0, StorePreviousStates(changes, generation, population, complex))

                        if len(redo_stack) > HISTORY_STACK_SIZE:
                            redo_stack.pop()

                        generation = stats[0]
                        population = stats[1]
                        complex = stats[2]

                        ProcessChanges(changes)
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
        UpdateScreen(generation, population, complex)

if __name__ == "__main__":
    main()