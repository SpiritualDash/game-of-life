import pygame

pygame.init()

text_font = pygame.font.SysFont("Arial", 18)

screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
pygame.display.set_caption("Game of Life")

# change cell size
SIZE = 7

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

GEN_UPDATE = pygame.USEREVENT + 1

cells = {}

def get_cell(cursor_x, cursor_y, camera_pos):
    cell_pos =  int(cursor_x / SIZE) + int(camera_pos[0] / SIZE), int(cursor_y / SIZE) + int(camera_pos[1] / SIZE)
    cell_status = cells.get(cell_pos, STATUSES["DEAD"])

    return cell_pos, cell_status

def get_neighbors(x_index, y_index):
    live_neighbors = 0
    dead_neighbors = []

    for x_increment in range(-1, 2):
        for y_increment in range(-1, 2):
            neighbor_x = x_index + x_increment
            neighbor_y = y_index + y_increment
            cell_pos = neighbor_x, neighbor_y

            if neighbor_x == x_index and neighbor_y == y_index: continue

            cell_status = cells.get(cell_pos, STATUSES["DEAD"])

            if cell_status == STATUSES["ALIVE"]: 
                live_neighbors += 1
            elif cell_status == STATUSES["DEAD"]:
                dead_neighbors.append(cell_pos)

    return live_neighbors, dead_neighbors

def get_population():
    count = 0

    for status in cells.values():
        if status == STATUSES["ALIVE"] or status == STATUSES["POPULATED"]: count += 1

    return count

def get_result_status(complex, neighbor_count, status):
    if status == STATUSES["ALIVE"]:
        if neighbor_count < 2:
            # Live cell w/ fewer than 2 live neighbours, solitude
            if complex: 
                return STATUSES["SOLITUDE"]
            else:
                return STATUSES["DEAD"]
        elif neighbor_count == 2 or neighbor_count == 3:
            # Live cell w/ 2 or 3 live neighbours, survives to next gen
            return STATUSES["ALIVE"]
        elif neighbor_count > 3:
            # Live cell w/ more than 3 live neighbours, overpopulated
            if complex: 
                return STATUSES["OVERPOPULATED"]
            else:
                return STATUSES["DEAD"]
    elif status == STATUSES["DEAD"] and neighbor_count == 3:
        # Dead cell w/ exactly 3 live neighbours, becomes live cell
        if complex: 
            return STATUSES["POPULATED"]
        else:
            return STATUSES["ALIVE"]
            
    return None

def process_changes(gen_changes):
    for cell_pos, status in gen_changes.items():
        if status == STATUSES["DEAD"]: 
            cells.pop(cell_pos)
        else:
            cells[cell_pos] = status

# for saving actions for the redo/undo stack
def store_previous_states(changes, prev_gen, prev_pop, prev_complex):
    previous_states = {cell_pos: STATUSES["DEAD"] for cell_pos, _ in changes.items()}
    previous_states["stats"] = (prev_gen, prev_pop, prev_complex)

    return previous_states

def update_gen(generation, population, complex):
    gen_changes = {}
    dead_cells_checked = []

    for cell_pos, status in cells.items():
        # all cells here have a status
        result_status = None

        # not half gen
        if generation % 1 == 0:
            neighbor_count, dead_neighbors = get_neighbors(cell_pos[0], cell_pos[1])

            result_status = get_result_status(complex, neighbor_count, status)

            # check dead cells around alive cell
            for dead_pos in dead_neighbors:
                if dead_pos in dead_cells_checked: continue 
                dead_cells_checked.append(dead_pos)

                count, _ = get_neighbors(dead_pos[0], dead_pos[1])
                dead_status = get_result_status(complex, count, STATUSES["DEAD"])

                if dead_status is not None:
                    gen_changes[dead_pos] = dead_status
        else:
            if status == STATUSES["POPULATED"]:
                # Make cell live the next generation, complex mode
                result_status = STATUSES["ALIVE"]
            elif status == STATUSES["OVERPOPULATED"] or status == STATUSES["SOLITUDE"]:
                # Make cell die the next generation, complex mode
                result_status = STATUSES["DEAD"]

        if result_status is not None:
            gen_changes[cell_pos] = result_status
    
    undo_states = store_previous_states(gen_changes, generation, population, complex)
    process_changes(gen_changes)

    new_population = get_population()

    if complex or generation % 1 != 0:
        generation += .5
    else:
        generation += 1

    return generation, new_population, undo_states

def update_screen(generation, population, complex, camera_pos):
    screen.fill((0, 0, 0))

    if pygame.mouse.get_visible():
        x, y = pygame.mouse.get_pos()
        cell_pos, status = get_cell(x, y, camera_pos)

        cell_x, cell_y = cell_pos

        if status == STATUSES["DEAD"]:
            pygame.draw.rect(screen, HOVER, pygame.Rect(int(x / SIZE) * SIZE, int(y / SIZE) * SIZE, SIZE, SIZE))
        else:
            stat_display = text_font.render(f"Cell Status: {STATUS_NAMES[status]}", True, status, (0, 0, 0))
            coord_display = text_font.render(f"Coordinates: ({cell_x}, {cell_y})", True, WHITE, (0, 0, 0))

            stat_rect = stat_display.get_rect()
            coord_rect = coord_display.get_rect()

            stat_rect.bottomleft = (x + 5, y + 26)
            coord_rect.bottomleft = (x + 5, y + 5)

            screen.blit(stat_display, stat_rect)
            screen.blit(coord_display, coord_rect)
    
    for cell_pos, status in cells.items():
        x, y = cell_pos
        pygame.draw.rect(screen, status, pygame.Rect((SIZE * x) - camera_pos[0], (SIZE * y) - camera_pos[1], SIZE, SIZE))
    
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

    camera_pos =  [0, 0]

    undo_stack = []
    redo_stack = []

    while True:
        pygame.time.Clock().tick(60)
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            camera_pos[1] -= SIZE
        if pressed[pygame.K_a]:
            camera_pos[0] -= SIZE
        if pressed[pygame.K_s]:
            camera_pos[1] += SIZE
        if pressed[pygame.K_d]:
            camera_pos[0] += SIZE
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not is_evolving: # L click
                    cell_pos, status = get_cell(event.pos[0], event.pos[1], camera_pos)
                    if status == STATUSES["DEAD"]:
                        cells[cell_pos] = STATUSES["ALIVE"]
                        population += 1
                    else:
                        cells.pop(cell_pos)
                        population -= 1
                elif event.button == 2: # M click
                    generation, population, _ = update_gen(generation, population, complex)
                elif event.button == 3: # R click
                    is_evolving = not is_evolving

                    if is_evolving:
                        wait_time = tick_speed

                        if complex: wait_time = tick_speed - int(tick_speed / 4)
                        pygame.time.set_timer(GEN_UPDATE, wait_time)
                    else:
                        pygame.time.set_timer(GEN_UPDATE, 0)
                    
                    pygame.mouse.set_visible(not is_evolving)
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    tick_speed = pygame.math.clamp(tick_speed - 10, 50, 200)
                elif event.y < 0:
                    tick_speed = pygame.math.clamp(tick_speed + 10, 50, 200)

                if is_evolving:
                    wait_time = tick_speed
                    if complex: wait_time = tick_speed - int(tick_speed / 4)

                    pygame.time.set_timer(GEN_UPDATE, wait_time)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    complex = not complex
                elif not is_evolving and event.mod % pygame.KMOD_CTRL:
                    if event.key == pygame.K_y and len(redo_stack) > 0:
                        change_dict = redo_stack.pop(0)
                        stats = change_dict.pop("stats")

                        undo_stack.insert(0, store_previous_states(change_dict, generation, population, complex))

                        if len(undo_stack) >  HISTORY_STACK_SIZE:
                            undo_stack.pop()

                        generation, population, complex = stats

                        process_changes(change_dict)
                    elif event.key == pygame.K_z and len(undo_stack) > 0:
                        change_dict = undo_stack.pop(0)
                        stats = change_dict.pop("stats")

                        redo_stack.insert(0, store_previous_states(change_dict, generation, population, complex))

                        if len(redo_stack) > HISTORY_STACK_SIZE:
                            redo_stack.pop()

                        generation, population, complex = stats

                        process_changes(change_dict)
            elif event.type == GEN_UPDATE:
                generation, population, undo_states = update_gen(generation, population, complex)
                undo_stack.insert(0, undo_states)

                if len(undo_stack) >  HISTORY_STACK_SIZE:
                    undo_stack.pop()
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()
                

                # elif event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
            #     cell_data_pos, status = GetCell(event.pos[0], event.pos[1])
            #     x_index, y_index = cell_data_pos

            #     if status == STATUSES["DEAD"]:
            #         cells[x_index][y_index] = STATUSES["ALIVE"]
            #         population += 1
            #     else:
            #         cells[x_index][y_index] = STATUSES["DEAD"]
            #         population -= 1
    
        update_screen(generation, population, complex, camera_pos)

if __name__ == "__main__":
    main()