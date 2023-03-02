import tkinter as tk
import random

# screen info
screen_width = 800
screen_height = 500

# canvas info
canvas_width = screen_width
canvas_height = screen_height

# cell manager
cell_size = 20
rows = int(screen_height / cell_size)
cols = int(screen_width / cell_size)
cells = []
cells_states = [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]

def make_cells():
    for row in range(rows):
        cells_col = []
        for col in range(cols):
            cell_xtop = col * cell_size 
            cell_ytop = row * cell_size
            cell_xbottom = cell_xtop + cell_size
            cell_ybottom = cell_ytop + cell_size

            if cells_states[row][col] == 0:
                current_rect = canvas.create_rectangle(cell_xtop, cell_ytop, cell_xbottom, cell_ybottom, fill="black")
            else:
                current_rect = canvas.create_rectangle(cell_xtop, cell_ytop, cell_xbottom, cell_ybottom, fill="white")

            cells_col.append(current_rect)
        cells.append(cells_col)

def click_cell(event):
    x = event.x
    y = event.y

    cell_in_row = y // cell_size
    cell_in_col = x // cell_size
    cell_clicked = cells[cell_in_row][cell_in_col]

    # change the state (1 means alive)
    # change the color
    if canvas.itemcget(cell_clicked, "fill") == "black":
        canvas.itemconfig(cell_clicked, fill="white")
        cells_states[cell_in_row][cell_in_col] = 1
    else:
        canvas.itemconfig(cell_clicked, fill="black")
        cells_states[cell_in_row][cell_in_col] = 0

# grid manager
def get_num_neighbours(row, col):
    num_neighbours = 0
    for i in range(-1, 2):  # Loop through the rows
        for j in range(-1, 2):  # Loop through the columns
            # If the cell is itself
            if i == 0 and j == 0:
                # Skip the cell
                continue
            # Calculate the neighbour row
            neighbour_row = row + i
            # Calculate the neighbour column
            neighbour_col = col + j
            # If the neighbour is out of bounds
            if neighbour_row < 0 or neighbour_row >= rows or neighbour_col < 0 or neighbour_col >= cols:
                # Skip the cell
                continue
            # Add the neighbour to the number of neighbours
            num_neighbours += cells_states[neighbour_row][neighbour_col]
    return num_neighbours

def update_grid_state():
    next_cells_states = [[0] * cols for _ in range(rows)]

    # conway's game of life main logic'
    for i in range(rows):
        for j in range(cols):
            num_neighbours = get_num_neighbours(i, j)

            # If the cell is alive
            if cells_states[i][j] == 1:
                # If the cell has less than 2 neighbours
                if num_neighbours < 2:
                    # The cell dies
                    next_cells_states[i][j] = 0
                # If the cell has 2 or 3 neighbours
                elif num_neighbours == 2 or num_neighbours == 3:
                    # The cell stayes alive
                    next_cells_states[i][j] = 1
                elif num_neighbours > 3:
                    # The cell dies
                    next_cells_states[i][j] = 0
            # If the cell is dead
            else:
                # If the cell has 3 neighbours
                if num_neighbours == 3:
                    # The cell becomes alive
                    next_cells_states[i][j] = 1
                # If the cell has less than 3 neighbours
                else:
                    # The cell stays dead
                    next_cells_states[i][j] = 0

    return next_cells_states

def update_grid():
    global cells_states
    cells_states = update_grid_state()

    for i in range(rows):
        for j in range(cols):
            # change the color
            if cells_states[i][j] == 1:
                canvas.itemconfig(cells[i][j], fill="white")
            else:
                canvas.itemconfig(cells[i][j], fill="black")

# animation manager
animating = False
animation_speed = 500

def animate():
    if animating:
        update_grid()
        canvas.after(animation_speed, animate)

# main window
window = tk.Tk()
window.title("Conway's Game of Life")
window.minsize(screen_width, screen_height)
window.resizable(False, False)

## menu frame
menu_frame = tk.Frame(window)
menu_frame.grid(row=0, column=0)

### start button
def stop_vis():
    global animating
    animating = False

    start_btn.config(text="Start", command=start_vis)
def start_vis():
    global animating
    animating = True

    start_btn.config(text="Stop", command=stop_vis)

    animate()
start_btn = tk.Button(menu_frame, text="Start", command=start_vis)
start_btn.grid(row=0, column=0)

### reset button
def reset_vis():
    global animating
    global cells_states
    animating = False
    cells_states = [[0] * cols for _ in range(rows)]
    
    update_grid()

    # update start button
    start_btn.config(text="Start", command=start_vis)
reset_btn = tk.Button(menu_frame, text="Reset", command=reset_vis)
reset_btn.grid(row=0, column=1)

### random button
def randomize():
    global animating
    global cells_states
    animating = False
    cells_states = [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]
    
    update_grid()

    # update start button
    start_btn.config(text="Start", command=start_vis)
random_btn = tk.Button(menu_frame, text="Random", command=randomize)
random_btn.grid(row=0, column=2)

### animation speed
### animation speed label
anim_speed_lbl = tk.Label(menu_frame, text="Animation speed: ")
anim_speed_lbl.grid(row=0, column=3)
### animation speed spinbox
def spinbox_used():
    global animation_speed
    animation_speed = anim_speed_spinbox.get()
default_speed = tk.StringVar()
anim_speed_spinbox = tk.Spinbox(menu_frame, from_=1, to=1000, increment=500, width=5, textvariable=default_speed, command=spinbox_used, state="readonly")
anim_speed_spinbox.grid(row=0, column=4)
default_speed.set(animation_speed)
### animation speed unit label
speed_unit_lbl = tk.Label(menu_frame, text="ms")
speed_unit_lbl.grid(row=0, column=5)

## canvas
canvas = tk.Canvas(window, height=canvas_height, width=canvas_width, bg="white", highlightthickness=0)
canvas.bind("<Button-1>", click_cell)
canvas.grid(row=1, column=0)

# draw grid
make_cells()

window.mainloop()
