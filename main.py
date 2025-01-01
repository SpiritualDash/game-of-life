import pygame

pygame.init()

text_font = pygame.font.SysFont("Arial", 18)

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Game of Life")

x, y = screen.get_size() # screen size

# Adjust these to change amount of cells per column & row
HORIZ_CELLS = 60
VERT_CELLS = 60

horiz_cell_space = x / HORIZ_CELLS
vert_cell_space = y / VERT_CELLS

# basic colors
HOVER = (125, 125, 125)
WHITE = (255, 255, 255)

statuses = {
    "OVERPOPULATED": (242, 222, 5),
    "SOLITUDE": (255, 0, 0),
    "ALIVE": WHITE,
    "POPULATED": (5, 100, 242),
    "DEAD": (0, 0, 0)
}

status_names = {
    statuses["OVERPOPULATED"]: "Overpopulated",
    statuses["SOLITUDE"]: "Solitude",
    statuses["ALIVE"]: "Alive",
    statuses["POPULATED"]: "Populating..."
}

# settings
complex = False
rainbow = False
tick_speed = 100 # in milliseconds

# simulation properties
generation = 0
population = 0
is_evolving = False

cells = [] 

# Cells are structured in (y, x) format
# Initialize dead units
for i in range(0, VERT_CELLS + 1):
    row_list = []

    for i in range(0, HORIZ_CELLS + 1):
        row_list.append(statuses["DEAD"])

    cells.append(row_list)

def GetCellInList(y_pos, x_pos):
    index_y = int(y_pos / vert_cell_space)
    index_x = int(x_pos / horiz_cell_space)
    
    cell_pos = (vert_cell_space * index_y, horiz_cell_space * index_x)
    return (index_y, index_x), cell_pos

def GetAmountOfLiveNeighbors(y_index, x_index):
    live_neighbors = 0

    neighbors = []

    for y_increment in range(-1, 2):
        for x_increment in range(-1, 2):
            neighbor_y = y_index + y_increment
            neighbor_x = x_index + x_increment

            if neighbor_y < 0 or neighbor_x < 0: continue
            if neighbor_y == y_index and neighbor_x == x_index: continue

            try: 
                neighbors.append(cells[neighbor_y][neighbor_x])
            except IndexError:
                continue

    for neighbor in neighbors:
        if neighbor == statuses["ALIVE"]: live_neighbors += 1

    return live_neighbors

def GetPopulation():
    count = 0

    for row in cells:
        for cell in row:
            if cell == statuses["ALIVE"] or cell == statuses["POPULATED"]:
                count += 1

    return count

def UpdateGen(generation):
    gen_changes = []

    for row_i in range(0, len(cells)):
        row = cells[row_i]
        for cell_i in range(0, len(row)):
            neighbor_count = GetAmountOfLiveNeighbors(row_i, cell_i)
            cell_tuple = (row_i, cell_i)
            cell = row[cell_i]

            result_status = False

            if generation % 1 == 0:
                if cell == statuses["ALIVE"]:
                    if neighbor_count < 2:
                    # Live cell w/ fewer than 2 live neighbours, solitude
                        if complex: 
                            result_status = statuses["SOLITUDE"]
                        else:
                            result_status = statuses["DEAD"]

                    elif neighbor_count == 2 or neighbor_count == 3:
                    # Live cell w/ 2 or 3 live neighbours, survives to next gen
                        result_status = statuses["ALIVE"]

                    elif neighbor_count > 3:
                    # Live cell w/ more than 3 live neighbours, overpopulated
                        if complex: 
                            result_status = statuses["OVERPOPULATED"]
                        else:
                            result_status = statuses["DEAD"]
                elif cell == statuses["DEAD"] and neighbor_count == 3:
                    # Dead cell w/ exactly 3 live neighbours, becomes live cell
                    if complex: 
                        result_status = statuses["POPULATED"]
                    else:
                        result_status = statuses["ALIVE"]
            else:
                if cell == statuses["POPULATED"]:
                    # Make cell live the next generation, complex mode
                    result_status = statuses["ALIVE"]
                elif cell == statuses["OVERPOPULATED"] or cell == statuses["SOLITUDE"]:
                    # Make cell die the next generation, complex mode
                    result_status = statuses["DEAD"]

            if result_status:
                gen_changes.append([cell_tuple, result_status])
    
    for change in gen_changes:
        cell_tuple = change[0]
        is_alive = change[1]

        y_ind = cell_tuple[0]
        x_ind = cell_tuple[1]

        cells[y_ind][x_ind] = is_alive

    new_population = GetPopulation()

    if complex or generation % 1 != 0:
        generation += .5
    else:
        generation += 1

    return generation, new_population 

def UpdateScreen(generation, population):
    screen.fill((0, 0, 0))

    for row_index in range(0, len(cells)):
        row = cells[row_index]
        for cell_index in range(0, len(row)):
            if row[cell_index] != statuses["DEAD"]:
                pygame.draw.rect(screen, row[cell_index], pygame.Rect(horiz_cell_space * cell_index, vert_cell_space * row_index, horiz_cell_space, vert_cell_space))

    if pygame.mouse.get_visible():
        x, y = pygame.mouse.get_pos()
        cell_in_data, cell_positions = GetCellInList(y, x)

        cell_y = cell_in_data[0]
        cell_x = cell_in_data[1]

        cell = cells[cell_y][cell_x]

        if cell == statuses["DEAD"]:
            pygame.draw.rect(screen, HOVER, pygame.Rect(cell_positions[1], cell_positions[0], horiz_cell_space, vert_cell_space))
        else:
            stat_display = text_font.render("Cell Status: " + status_names[cell], True, cell, (0, 0, 0))
            coord_display = text_font.render("Coordinates: (" + str(cell_x) + "," + str(cell_y) + ")", True, WHITE, (0, 0, 0))

            stat_rect = stat_display.get_rect()
            coord_rect = coord_display.get_rect()

            stat_rect.bottomleft = (x + 5, y + 26)
            coord_rect.bottomleft = (x + 5, y + 5)

            screen.blit(stat_display, stat_rect)
            screen.blit(coord_display, coord_rect)
    
    # Generation/Population counters
    text_color = WHITE
    
    if complex: text_color = statuses["POPULATED"]

    gen_count = text_font.render("Generation: " + str(generation), True, text_color)
    pop_count = text_font.render("Population: " + str(population), True, text_color)

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

# ------------------------------------

while True:
    if is_evolving:
        pygame.time.wait(tick_speed)

        new_gen, new_pop = UpdateGen(generation)
        generation = new_gen
        population = new_pop

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # L click
                if is_evolving: continue
                cell_clicked, cell_pos = GetCellInList(event.pos[1], event.pos[0])
                y_index = cell_clicked[0]
                x_index = cell_clicked[1]
                cell = cells[y_index][x_index]

                if cell == statuses["DEAD"]:
                    cells[y_index][x_index] = statuses["ALIVE"]
                    population += 1
                else:
                    cells[y_index][x_index] = statuses["DEAD"]
                    population -= 1
            elif event.button == 2: # M click
                new_gen, new_pop = UpdateGen(generation)

                generation = new_gen
                population = new_pop
            elif event.button == 3: # R click
                is_evolving = not is_evolving
                pygame.mouse.set_visible(not is_evolving)
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                tick_speed = pygame.math.clamp(tick_speed - 10, 5, 250)
            elif event.y < 0:
                tick_speed = pygame.math.clamp(tick_speed + 10, 5, 250)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not is_evolving:
                complex = not complex
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    UpdateScreen(generation, population)