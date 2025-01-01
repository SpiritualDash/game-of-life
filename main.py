import pygame

pygame.init()

text_font = pygame.font.SysFont("Arial", 12)

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Game of Life")

x, y = screen.get_size() # screen size

# Adjust these to change amount of cells per column & row
HORIZ_CELLS = 50
VERT_CELLS = 40

horiz_cell_space = x / HORIZ_CELLS
vert_cell_space = y / VERT_CELLS

# basic colors
DEAD = (0, 0, 0)
HOVER = (125, 125, 125)
ALIVE = (255, 255, 255)

# settings
complex = False
rainbow = False
tick_speed = 100 # in milliseconds

# simulation properties
generation = 0
population = 0
running = True
is_evolving = False

cells = [] 

# Cells are structured in (y, x) format
# Initialize dead units
for i in range(0, VERT_CELLS + 1):
    row_list = []

    for i in range(0, HORIZ_CELLS + 1):
        row_list.append(False)

    cells.append(row_list)


def DisplayText(words): # , position, size
    text_obj = text_font.render(words, True, ALIVE)

    rect = text_obj.get_rect()
    rect.width = 100
    rect.height = 50
    rect.center = (x // 2, y // 2)

    screen.blit(text_obj, rect)

def GetCellInList(y_pos, x_pos):
    index_y = int(y_pos / vert_cell_space)
    index_x = int(x_pos / horiz_cell_space)
    
    cell_pos = (vert_cell_space * index_y, horiz_cell_space * index_x)
    return (index_y, index_x), cell_pos

def GetAmountOfLiveNeighbors(y_index, x_index):
    live_neighbors = 0

    increment_list = [-1, 1]

    # Ensure that the index is within the range.
    # Handle valid indexes that go past length of cell list (negative index?)
    # rewrite this later?

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
        if neighbor == True: live_neighbors += 1

    return live_neighbors

def UpdateGen():
    global generation
    generation += 1

    gen_changes = []

    for row_i in range(0, len(cells)):
        row = cells[row_i]
        for cell_i in range(0, len(row)):
            neighbor_count = GetAmountOfLiveNeighbors(row_i, cell_i)
            cell_tuple = (row_i, cell_i)

            if row[cell_i] == True:
                if neighbor_count < 2:
                    # Live cell w/ fewer than 2 live neighbours, death
                    gen_changes.append([cell_tuple, False])

                elif neighbor_count == 2 or neighbor_count == 3:
                    # Live cell w/ 2 or 3 live neighbours, lives to next gen
                    gen_changes.append([cell_tuple, True])

                elif neighbor_count > 3:
                    # Live cell w/ more than 3 live neighbours, death
                    gen_changes.append([cell_tuple, False])

            elif row[cell_i] == False and neighbor_count == 3:
                # Dead cell w/ exactly 3 live neighbours, becomes live cell
                gen_changes.append([cell_tuple, True])

    for change in gen_changes:
        cell_tuple = change[0]
        is_alive = change[1]

        y_ind = cell_tuple[0]
        x_ind = cell_tuple[1]

        cells[y_ind][x_ind] = is_alive

def UpdateScreenRects():
    screen.fill(DEAD)

    for row_index in range(0, len(cells)):
        row = cells[row_index]
        for cell_index in range(0, len(row)):
            if row[cell_index] == True:
                pygame.draw.rect(screen, ALIVE, pygame.Rect(horiz_cell_space * cell_index, vert_cell_space * row_index, horiz_cell_space, vert_cell_space))

    if pygame.mouse.get_visible():
        x, y = pygame.mouse.get_pos()
        cell_in_data, cell_positions = GetCellInList(y, x)

        pygame.draw.rect(screen, HOVER, pygame.Rect(cell_positions[1], cell_positions[0], horiz_cell_space, vert_cell_space))
    
    DisplayText("Generation: " + str(generation), )

    pygame.display.flip()

def ProcessEvents():
    global is_evolving
    global tick_speed

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # L click
                cell_clicked, cell_pos = GetCellInList(event.pos[1], event.pos[0])
                y_index = cell_clicked[0]
                x_index = cell_clicked[1]
                cell = cells[y_index][x_index]
                cells[y_index][x_index] = not cell
            elif event.button == 2: # M click
                UpdateGen()
            elif event.button == 3: # R click
                is_evolving = not is_evolving
                pygame.mouse.set_visible(not is_evolving)
        elif event.type == pygame.MOUSEWHEEL:
            if event.y == 1:
                tick_speed = pygame.math.clamp(tick_speed - 5, 5, 200)
            else:
                tick_speed = pygame.math.clamp(tick_speed + 5, 5, 200)
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()

# ------------------------------------

while running:
    if is_evolving:
        pygame.time.wait(tick_speed)
        UpdateGen()

    ProcessEvents()

    UpdateScreenRects()