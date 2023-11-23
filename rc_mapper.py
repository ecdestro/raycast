from tkinter import *
from tkinter import filedialog
import os, sys

# Define grid dimensions
rows = 20 
cols = 20
cell_size = 20  # Size of each cell in pixels
currentFile = False
border ="1 " * (cols+1) + "1"

def newFile():
    clear_grid()
    untitled = open("untitled.txt", "w")
    untitled.close()

def openFile():
    location = filedialog.askopenfile(title = "Open", initialdir = ".", defaultextension = "*.txt", filetypes = (("Text files", "*.txt"), ("All files", "*.*")))
    global currentFile
    currentFile = os.path.split(location)[1]
    try:
        pass
    except AttributeError:
        print("No File Selected")

def saveFile():
    location = filedialog.asksaveasfilename(title = "Save As", initialdir = ".", defaultextension = "*.txt", filetypes = (("Text files", "*.txt"), ("All files", "*.*")))
    try:
        with open(location, "w") as file:
            file.write(border + '\n')
            for row in grid:
                rowString = "1 " + " ".join(map(str, row)) + " 1"
                file.write(rowString + "\n")
            file.write(border)
        global currentFile
        currentFile = os.path.split(location)[1]
        file.close()
    except FileNotFoundError:
        print("No File Selected")

def updateFile():
    if currentFile:
        with open(currentFile,"w") as file:
            file.write(border + "\n")
            for row in grid:
                rowString = " ".join(map(str, row))
                file.write(rowString + "\n")
            file.write(border)
        file.close()
    else:
        try:
            saveFile()
        except FileNotFoundError:
            print("No File Selected")

def draw_cell(col, row):
    x0 = col * cell_size
    y0 = row * cell_size
    x1 = x0 + cell_size
    y1 = y0 + cell_size
    if grid[row][col] == 1:
        canvas.create_rectangle(x0, y0, x1, y1, outline="gray", fill="black")
    else:
        canvas.create_rectangle(x0, y0, x1, y1, outline="gray", fill="light gray")

def toggle_cell(event):
    col = event.x // cell_size
    row = event.y // cell_size
    grid[row][col] = 1 - grid[row][col]
    draw_cell(col, row)
    # update_text_widget()

grid = [[0 for _ in range(cols)] for _ in range(rows)]

def draw_grid():
    for row in range(rows):
        for col in range(cols):
            x0 = col * cell_size
            y0 = row * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            if grid[row][col] == 1:
                canvas.create_rectangle(x0, y0, x1, y1, outline="gray", fill="black")
            else:
                canvas.create_rectangle(x0, y0, x1, y1, outline="gray", fill="white")

# def update_text_widget():
#     text_widget.delete(1.0, END)  # Clear the current text
#     for row in grid:
#         text_widget.insert(END, " ".join(map(str, row)) + "\n")  # Add each row to the Text widget

def clear_grid():
    # Reset all the values in the list of arrays to 0
    for row in range(rows):
        for col in range(cols):
            grid[row][col] = 0
    # update_text_widget()
    draw_grid()

root = Tk()
root.title("Mapper")

canvas = Canvas(root, width=cols * cell_size, height=rows * cell_size)
canvas.pack(side=LEFT)

# text_widget = Text(root, width=cols * 2, height=rows)
# text_widget.pack(side=RIGHT, padx=10)

draw_grid()

canvas.bind("<Button-1>", toggle_cell)

# update_text_widget()

menuBar = Menu(root)

fileMenu = Menu(menuBar, tearoff = False)
fileMenu.add_command(label = "New Map", command = newFile)
fileMenu.add_command(label = "Open Map...", command = openFile)
fileMenu.add_command(label = "Save Map", command = updateFile)
fileMenu.add_command(label = "Save Map As...", command = saveFile)
fileMenu.add_command(label = "Exit Editor", command = root.quit)
menuBar.add_cascade(label = "File", menu = fileMenu)

editMenu = Menu(menuBar, tearoff = False)
editMenu.add_command(label = "Undo", command = False)
editMenu.add_command(label = "Redo", command = False)
editMenu.add_command(label = "Grid Size...", command = False)
editMenu.add_command(label = "Clear Grid", command = clear_grid)
menuBar.add_cascade(label = "Edit", menu = editMenu)

root.config(menu = menuBar)

root.mainloop()
