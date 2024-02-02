import pygame 
import math
import sys
import pygame.freetype
from pygame.locals import *
import pandas as pd
from tkinter import Tk, filedialog
from Node import Node
#==============================================

def upload_excel_file():
    """ 
    Prompts the user to select an Excel file using a file dialog window and returns the selected file's path.
    :return: the path of the selected Excel file
    """
    root = Tk()
    root.withdraw()  # Hide the main tkinter window
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    root.destroy()
    return file_path

def read_maze(file_path):
    """
    Reads the maze from an Excel file and extracts the maze layout along with the start and goal positions.
    :param file_path: the path to the Excel file containing the maze layout
    :return: a tuple containing the maze layout, start position, and goal position
    """
    maze = []
    goal = (0, 0)
    start = (0, 0)
    df = pd.read_excel(file_path)
    
    for i in range(len(df)):
        row = []
        for j in range(len(df.iloc[i])):
            if df.iloc[i, j] in [0, "G", "S"]:
                if df.iloc[i, j] == "G":
                    goal = (i, j)
                if df.iloc[i, j] == "S":
                    start = (i, j)
                row.append((i, j))
            else:
                row.append("-")
        maze.append(row)

    return maze, start, goal

def create_btn(screen, btn_rect, color, text, font_size, font_type, font_color):
    """
    Creates a button on the given screen with the specified parameters.
    :param screen: the pygame screen to draw the button on
    :param btn_rect: the pygame.Rect object representing the dimensions and position of the button
    :param color: the color of the button (RGB tuple)
    :param text: the text to display on the button
    :param font_size: the size of the font
    :param font_type: the type of font to use
    :param font_color: the color of the text (RGB tuple)
    """
    pygame.draw.rect(screen, color, btn_rect, border_radius=6)
    font = pygame.font.SysFont(font_type, font_size)
    text_surface = font.render(text, True, font_color)
    text_rect = text_surface.get_rect(center=btn_rect.center)
    screen.blit(text_surface, text_rect)
    
def create_text(screen, position, text, font_size, font_type, font_color, rect=None, rect_color=None):
    """
    Renders text on the given Pygame screen with optional rectangular background.
    :param screen: Pygame screen object to render the text on
    :param position: (x, y) tuple representing the position of the text
    :param text: the text to render
    :param font_size: the size of the font
    :param font_type: the type of font to use
    :param font_color: the color of the text (RGB tuple)
    :param rect: optional pygame.Rect object representing the dimensions and position of the background rectangle
    :param rect_color: optional color of the background rectangle (RGB tuple)
    """
    font = pygame.font.SysFont(font_type, font_size)
    words = text.split(' ')
    lines = []  
    line = ''  
    
    # Split the text into lines that fit within the specified width
    for word in words:
        if font.size(line + ' ' + word)[0] < 600:  # Check if adding the word exceeds the width
            line += ' ' + word  # Add the word to the current line
        else:
            lines.append(line)  # Add the current line to the list of lines
            line = word  # Start a new line with the current word
    
    lines.append(line)  # Add the last line
    
    y = position[1]  # Initialize the y-coordinate for rendering
    
    # Render each line of text
    for line in lines:
        text_surface = font.render(line, True, font_color)  
        text_rect = text_surface.get_rect()  
        text_rect.center = (position[0], y)  # Center the text horizontally and set the y-coordinate
        
        # Draw the background rectangle if provided
        if rect is not None:
            rect_color = rect_color if rect_color is not None else (0,0,0) 
            pygame.draw.rect(screen, rect_color, rect, border_radius=6)  
            font = pygame.font.SysFont("comicsansms", font_size)  # Re-initialize the font for consistency
            text_surface = font.render(text, True, font_color) 
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)  # Blit the text onto the screen with the background
        else:
            screen.blit(text_surface, text_rect)  # Blit the text onto the screen without background
            y += font_size + 10  # Adjust spacing between lines

def draw_maze(screen, width, height, maze, start, goal, animation, path=None):
    """
    Renders the maze grid and icons on the given Pygame screen.
    :param screen: Pygame screen object to render the maze on
    :param width: Width of the screen
    :param height: Height of the screen
    :param maze: 2D list representing the maze grid
    :param start: Tuple representing the coordinates of the starting point (row, column)
    :param goal: Tuple representing the coordinates of the goal point (row, column)
    :param animation: Boolean indicating whether animation is enabled
    :param path: List of tuples representing the cells of the path to be highlighted
    """
    rows, columns = len(maze), len(maze[0])
    rect_x, rect_y = 50, 50  # Define the position of the maze grid

    # Load maze icons
    goal_icon = pygame.image.load('img/target.png')
    start_icon = pygame.image.load('img/finish-flag2.png')


    # Calculate cell dimensions
    cell_width = (width - rect_x * 2) // columns
    rect_width = cell_width * columns
    cell_height = (height - rect_y * 3.5) // rows
    rect_height = cell_height * rows

    # Draw the outer rectangle with white border
    pygame.draw.rect(screen, (255, 255, 255), (rect_x - 1, rect_y - 1, rect_width + 1, rect_height + 1), 1)

    # Draw horizontal lines (rows)
    for row in range(1, rows):
        y = rect_y + row * cell_height
        pygame.draw.line(screen, (255, 255, 255), (rect_x, y), (rect_x + rect_width, y), 1)

    # Draw vertical lines (columns)
    for col in range(1, columns):
        x = rect_x + col * cell_width
        pygame.draw.line(screen, (255, 255, 255), (x, rect_y), (x, rect_y + rect_height), 1)

    # Fill each cell with color based on maze values
    for row in range(rows):
        for col in range(columns):
            cell_x = rect_x + col * cell_width
            cell_y = rect_y + row * cell_height

            pygame.draw.rect(screen, (255, 255, 255), (cell_x + 1, cell_y + 1, cell_width - 2, cell_height - 2), 1)

            if maze[row][col] == "-":
                pygame.draw.rect(screen, (155, 93, 118), (cell_x + 1, cell_y + 1, cell_width - 2, cell_height - 2), 0)
            else:
                pygame.draw.rect(screen, (109, 79, 107), (cell_x + 1, cell_y + 1, cell_width - 2, cell_height - 2), 0)

                if path and animation:
                    animate_path(screen, path, rect_x, rect_y, cell_width, cell_height, start, goal, start_icon,
                                 goal_icon)
                    animation = False

                if path and not animation and (row, col) in path:
                    pygame.draw.rect(screen, (195,197,187), (cell_x + 1, cell_y + 1, cell_width - 2, cell_height - 2),
                                     0)

                if maze[row][col] == start:
                    # Blit the start icon
                    icon_width = min(cell_width, cell_height)
                    icon_height = min(cell_width, cell_height)
                    scaled_icon = pygame.transform.scale(start_icon, (icon_width - 10, icon_height - 10))
                    icon_rect = scaled_icon.get_rect(center=(cell_x + cell_width // 2, cell_y + cell_height // 2))
                    screen.blit(scaled_icon, icon_rect)

                if maze[row][col] == goal:
                    # Blit the goal icon
                    icon_width = min(cell_width, cell_height)
                    icon_height = min(cell_width, cell_height)
                    scaled_icon = pygame.transform.scale(goal_icon, (icon_width - 10, icon_height - 10))
                    icon_rect = scaled_icon.get_rect(center=(cell_x + cell_width // 2, cell_y + cell_height // 2))
                    screen.blit(scaled_icon, icon_rect)

def animate_path(screen, path, rect_x, rect_y, cell_width, cell_height, start, goal, start_icon, goal_icon):
    """
    Animates the path on the screen, highlighting the cells in the given path.
    :param screen: Pygame screen object to render the animation
    :param path: List of tuples representing the cells in the path
    :param rect_x: X-coordinate of the top-left corner of the maze grid
    :param rect_y: Y-coordinate of the top-left corner of the maze grid
    :param cell_width: Width of each cell in the maze grid
    :param cell_height: Height of each cell in the maze grid
    :param start: Tuple representing the coordinates of the starting point (row, column)
    :param goal: Tuple representing the coordinates of the goal point (row, column)
    :param start_icon: Image object for the start icon
    :param goal_icon: Image object for the goal icon
    """
    for cell in path:
        row, col = cell
        cell_x = rect_x + col * cell_width
        cell_y = rect_y + row * cell_height
        
        # Highlight the cell in the path
        pygame.draw.rect(screen, (195,197,187), (cell_x + 1, cell_y + 1, cell_width - 2, cell_height - 2), 0)  
        
        # Blit the goal icon if the current cell is the goal
        if (row, col) == goal:
            icon_width = min(cell_width, cell_height)
            icon_height = min(cell_width, cell_height)
            scaled_icon = pygame.transform.scale(goal_icon, (icon_width - 10, icon_height - 10))
            icon_rect = scaled_icon.get_rect(center=(cell_x + cell_width // 2, cell_y + cell_height // 2))
            screen.blit(scaled_icon, icon_rect)
        
        # Blit the start icon if the current cell is the start
        if (row, col) == start:
            icon_width = min(cell_width, cell_height)
            icon_height = min(cell_width, cell_height)
            scaled_icon = pygame.transform.scale(start_icon, (icon_width - 10, icon_height - 10))
            icon_rect = scaled_icon.get_rect(center=(cell_x + cell_width // 2, cell_y + cell_height // 2))
            screen.blit(scaled_icon, icon_rect)
        
        # Update the display
        pygame.display.flip()
        pygame.time.wait(100)
          
def DFS(maze, start, goal):
    """
    Performs a depth-first search (DFS) algorithm to find a path from the start position to the end position in a maze.

    :param maze: The maze grid representing the environment.
    :param start: The starting position in the maze.
    :param goal: The target position to reach in the maze.
    :return: A tuple containing the path from start to end and its length.
    """
    explored = set()
    stack = [Node(start, [], 0)]
    path = []

    while stack:
        current = stack.pop()
        path += [current.name]
        
        if current.name == goal:
            return current.path, len(current.path)

        for direction in "ESNW":
            node = check_next_node(maze, current.name, direction)
            if node != "-" and node is not None and node not in explored:
                explored.add(node)
                stack.append(Node(node, path, current.cost + 1))

    return None, 0
                       
def BFS(maze, start, goal):
    """
    Performs a breadth-first search (BFS) algorithm to find a path from the start position to the goal position in a maze.

    :param maze: The maze grid representing the environment.
    :param start: The starting position in the maze.
    :param goal: The target position to reach in the maze.
    :return: A tuple containing the path from start to end and its length.
    """
    explored = set()
    queue = [Node(start, [], 0)]
    path = []
    cost = 0
    
    while queue:
        current = queue.pop(0)
        cost += 1
        path.append(current.name)
        
        if current.name == goal:
            return current.path, cost
        
        for direction in "ESNW":
            node = check_next_node(maze, current.name, direction)
            if node != "-" and node is not None and node not in explored:
                explored.add(node)
                queue.append(Node(node, path, cost))
                
    return None, 0
   
def heuristic(a, b):
    """
    Calculates the heuristic (estimated) cost from node 'a' to node 'b' using the Euclidean distance formula.

    :param a: The current node position.
    :param b: The goal node position.
    :return: The heuristic cost from 'a' to 'b'.
    """
    h_cost = math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
    return h_cost

def a_star(maze, start, goal):
    """
    Performs the A* search algorithm to find the shortest path from the start position to the end position in a maze.

    :param maze: The maze grid representing the environment.
    :param start: The starting position in the maze.
    :param goal: The target position to reach in the maze.
    :return: A tuple containing the path from start to end and its length.
    """
    explored = set()
    g_cost = 0
    queue = [Node((start, heuristic(start, goal), g_cost + 1))]
    came_from = {start: None}
    
    while queue:
        queue.sort(key=lambda x: x.name[1])
        current = queue.pop(0)
        explored.add(current)
        
        if current.name[0] == goal:
            path = [goal]
            while came_from[goal] is not None:
                path.append(came_from[goal])
                goal = came_from[goal]
            cost = len(path) - 1
            path = list(reversed(path))
            return path, cost
        
        for direction in "ENSW":
            node = check_next_node(maze, current.name[0], direction)
            if node != "-" and node is not None and node not in explored:
                g_cost = current.name[2]
                f_cost = heuristic(node, goal) + g_cost + 1
                if node != start and node not in explored:
                    came_from[node] = current.name[0]
                explored.add(node)
                queue.append(Node((node, f_cost, g_cost + 1)))
                
    return None, 0     
        
def check_next_node(maze, current_node, direction):
    """
    Checks the next node in the specified direction within the maze.

    :param maze: The maze grid representing the environment.
    :param current_node: The current position in the maze.
    :param direction: The direction to check for the next node (E, S, N, W).
    :return: The next node in the specified direction or None if it's out of bounds.
    """
    current_row, current_col = current_node

    if direction == "E" and current_col + 1 < len(maze[0]):
        return maze[current_row][current_col + 1]
    elif direction == "S" and current_row - 1 >= 0:
        return maze[current_row - 1][current_col]
    elif direction == "N" and current_row + 1 < len(maze):
        return maze[current_row + 1][current_col]
    elif direction == "W" and current_col - 1 >= 0:
        return maze[current_row][current_col - 1]
    else:
        return None

def make_gradient_background(screen, color1, color2, width, height):
    """
    Generates a gradient background on the given Pygame screen.

    :param screen: Pygame screen surface to draw the gradient background on.
    :param color1: Starting color of the gradient as a tuple (R, G, B).
    :param color2: Ending color of the gradient as a tuple (R, G, B).
    :param width: Width of the screen.
    :param height: Height of the screen.
    """
    for y in range(height):
        # Interpolate colors between color1 and color2 based on the current height
        r = int(color1[0] + (color2[0] - color1[0]) * (y / height))
        g = int(color1[1] + (color2[1] - color1[1]) * (y / height))
        b = int(color1[2] + (color2[2] - color1[2]) * (y / height))
        # Draw a horizontal line with the interpolated color
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))
       
def main():
    # Define window dimensions
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 700

    # Define fonts and colors
    FONT1 = "comicsansms"
    FONT2 = "Calibri"
    FONT3 = "Trebuchet MS"
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (147, 144, 137)
    PURPLE = (109, 79, 107)
    PINK = (155, 93, 118)
    BLUE = (48, 174, 235)
    RED = (235, 80, 98)
    YELLOW = (243, 202, 50)
    ORANGE = (255,160,105)
    
    

    # Define introductory text and footer
    INTRO_TEXT = "Welcome to A Maze Solver Program! This program allows you to upload various maze shapes from Excel files and solve them using different searching algorithms."
    FOOTER = "© created by MALAKBADER"

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    # Define button rectangles
    upload_btn_rect1 = pygame.Rect(WINDOW_WIDTH / 2.75, WINDOW_HEIGHT / 1.9, 200, 50)
    upload_btn_rect2 = pygame.Rect(410, 580, 100, 40)
    dfs_btn_rect = pygame.Rect(50, 580, 80, 40)
    bfs_btn_rect = pygame.Rect(140, 580, 80, 40)
    astar_btn_rect = pygame.Rect(230, 580, 80, 40)
    reset_btn_rect = pygame.Rect(320, 580, 80, 40)
    output_btn_rect = pygame.Rect(520, 580, 230, 40)

    # Initialize variables
    current_event_dfs = None
    current_event_bfs = None
    current_event_reset = None
    current_event_astar = None
    output = "Cost = 0"
    window1 = True
    path = None
    animation = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if window1 and upload_btn_rect1.collidepoint(mouse_pos):
                    file_path = upload_excel_file()
                    if file_path:
                        maze, start, goal = read_maze(file_path)
                        window1 = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if dfs_btn_rect.collidepoint(event.pos):
                    output = "Cost = 0"
                    current_event_dfs = event.pos
                    current_event_reset = None
                    current_event_bfs = None
                    current_event_astar = None
                    animation = True

                if reset_btn_rect.collidepoint(event.pos):
                    output = "Cost = 0"
                    current_event_reset = event.pos
                    current_event_dfs = None
                    current_event_bfs = None
                    current_event_astar = None

                if bfs_btn_rect.collidepoint(event.pos):
                    output = "Cost = 0"
                    current_event_bfs = event.pos
                    current_event_dfs = None
                    current_event_reset = None
                    current_event_astar = None
                    animation = True

                if astar_btn_rect.collidepoint(event.pos):
                    output = "Cost = 0"
                    current_event_astar = event.pos
                    current_event_bfs = None
                    current_event_dfs = None
                    current_event_reset = None
                    animation = True

                if upload_btn_rect2.collidepoint(event.pos):
                    output = "Cost = 0"
                    current_event_astar = None
                    current_event_bfs = None
                    current_event_dfs = None
                    current_event_reset = None

                    file_path = upload_excel_file()
                    if file_path:
                        maze, start, goal = read_maze(file_path)

        make_gradient_background(screen, PURPLE, PINK, WINDOW_WIDTH, WINDOW_HEIGHT)
        create_text(screen, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.02), FOOTER, 15, FONT2, WHITE)

        if not window1:
            create_text(screen, (WINDOW_WIDTH - 240, WINDOW_HEIGHT - 99), output, 20, FONT1, BLACK, output_btn_rect, WHITE)
            draw_maze(screen, WINDOW_WIDTH, WINDOW_HEIGHT, maze, start, goal, animation)
            create_btn(screen, dfs_btn_rect, RED, "RUN DFS", 16, FONT1, WHITE)
            create_btn(screen, bfs_btn_rect, BLUE, "RUN BFS", 16, FONT1, WHITE)
            create_btn(screen, astar_btn_rect, ORANGE, "RUN A*", 16, FONT1, WHITE)
            create_btn(screen, reset_btn_rect, GRAY, "Reset", 20, FONT1, WHITE)
            create_btn(screen, upload_btn_rect2, YELLOW, "Upload maze", 16, FONT1, WHITE)

            if current_event_dfs:
                path, cost = DFS(maze, start, goal)
                if path is None:
                    output = "No Path Found"
                else:
                    draw_maze(screen, WINDOW_WIDTH, WINDOW_HEIGHT, maze, start, goal, animation, path)
                    output = "Cost = " + str(cost)
                    animation = False

            if current_event_reset:
                draw_maze(screen, WINDOW_WIDTH, WINDOW_HEIGHT, maze, start, goal, animation)

            if current_event_bfs:
                path, cost = BFS(maze, start, goal)
                if path is None:
                    output = "No Path Found"
                else:
                    draw_maze(screen, WINDOW_WIDTH, WINDOW_HEIGHT, maze, start, goal, animation, path)
                    output = "Cost = " + str(cost)
                    animation = False

            if current_event_astar:
                path, cost = a_star(maze, start, goal)
                if path is None:
                    output = "No Path Found"
                else:
                    draw_maze(screen, WINDOW_WIDTH, WINDOW_HEIGHT, maze, start, goal, animation, path)
                    output = "Cost = " + str(cost)
                    animation = False

        else:
            create_text(screen, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3.5), INTRO_TEXT, 25, FONT3, WHITE)
            create_btn(screen, upload_btn_rect1, YELLOW, "Upload the maze", 22, FONT1, WHITE)

        pygame.display.flip()
        clock.tick(60)


main()