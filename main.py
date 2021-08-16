#Libraries
from os import system
import pygame
import random
import time
import networkx as nx

#Images
hexagonImg = pygame.image.load('assets/hexagon.png')
wallImg = pygame.image.load('assets/wall.png')
holeImg = pygame.image.load('assets/hole.png')
burrowImg = pygame.image.load('assets/burrow.png')
mouseImg = pygame.image.load('assets/mouse.png')

#Constants
WIDTH = 800
HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (135, 200, 0)
BOARDX = 350
BOARDY = 120


#--- Hexagon ---
class Hexagon(pygame.sprite.Sprite):

    #Initalise hexagon object
    def __init__(self, screen, x=0, y=0, states=[]):
        #Properties
        pygame.sprite.Sprite.__init__(self) # Initalise class for game object
        self.x = x # Set the x position of the object
        self.y = y # Set the y position of the object
        self.image = hexagonImg # Set the image of the hexagon
        self.rect = self.image.get_rect() # Set the hitbox of the object
        self.rect.move_ip(x, y) # Update the hitbox
        self.screen = screen # Get the screen

        #States
        if 'mouse' in states: # Mouse State Check
            self.mouse = True
        else:
            self.mouse = False 

        if 'wall' in states: # Wall State Check
            self.wall = True        
        else:
            self.wall = False 

        if 'hole' in states: # Hole State Check
            self.hole = True
        else:
            self.hole = False

        if 'burrow' in states: # Burrow State Check
            self.burrow = True
        else:
            self.burrow = False

    #When this object is printed to the terminal
    def __str__(self):
        return f'''
                Position:
                    X - {self.x}
                    Y - {self.y}
                States:
                    Mouse - {self.mouse}
                    Burrow - {self.burrow}
                    Hole - {self.burrow}
                    Wall - {self.wall}

                '''        

    #Check if object is being clicked method
    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

    #Update the image
    def update(self, turn):
        #Check if the object has been clicked
        if self.is_clicked() and turn == 'P':
            if not(self.mouse) and not(self.hole) and not(self.wall) and not(self.burrow): # If the conditions for a wall to be placed are met
                self.wall = True # Change the object to a wall 
                turn = 'M' # Change the turn to the mouse

        #Check if the corresponding state has the correct image
        if self.wall:
            self.image = wallImg # Change the image to a wall        

        elif self.hole: # Check for hole state
            self.image = holeImg # Change to hole image

        elif self.burrow: # Check for hole state
            self.image = burrowImg # Change to hole image

        else:
            self.image = hexagonImg # Change the image to a hexagon
        

        self.screen.blit(self.image, (self.x, self.y)) # Draw the object on the screen

        #Check if there is a mouse on the hexagon
        if self.mouse:
            self.screen.blit(mouseImg, (self.x+16, self.y+16))        

        #Return the next turn
        return turn






#--- Board ---
class Board():
    #Initalise the class
    def __init__(self, graph):
        self.graph = graph # Initalise the hexagons
        self.turn = 'P' # Initalise the turn

        #Find the mouse
        for hex in self.graph.nodes: # Iterate through every hexagon
                if hex.mouse == True: # If the hexagon has the mouse
                    self.mouse = hex

        #Find the hole
        for hex in self.graph.nodes: # Iterate through every hexagon
                if hex.hole == True: # If the hexagon has the mouse
                    self.hole = hex

    #Update the board
    def update(self):
        #Mouse's Turn
        if self.turn == 'M':

            #Find next path
            nextHex = random.choice(list(self.graph.adj[self.mouse]))
            nextHex = next_path(self.graph.subgraph([node for node in self.graph.nodes if not(node.wall)]), self.mouse, self.hole)
            if nextHex == 'W' or nextHex == 'L':
                return nextHex
            else:
                self.mouse.mouse = False # Remove mouse from previous hexagon
                self.mouse = nextHex # Change the next hexagon to the mouse
                nextHex.mouse = True # Set next hexagon to have the mouse state

            self.turn = 'P'

        #Update every hexagon
        for hex in self.graph.nodes: # Iterate through every hexagon
            self.turn = hex.update(self.turn) # Update each hexagon







#--- Shortest Path Algorithim ---
def next_path(graph, startNode, endNode):
    #Check if the algorithim requirements are met
    if startNode not in graph.nodes or endNode not in graph.nodes:
        return startNode    
    
    #Initalise algorithim variables
    visited = []
    unvisited = []
    unvisited.extend(graph.nodes)
    path = []
    currentNode = startNode
    nextNode = startNode

    #Algorthim Loop
    while endNode not in path:
        #Choose the next node to add to the path
        if set(graph.adj[currentNode].keys()) <= set(visited): # If all the neighbours have been visited
            try: # Find the next node
                nextNode = path[-1]
                path.pop(-1)
            except: # If there is no path
                break        
        else: 
            while nextNode in visited: # While the node being chosen has been visited
                nextNode = random.choice(list(graph.adj[currentNode])) # Choose a neigbhbouring node
            path.append(nextNode) # Add the node to the path
            unvisited.remove(nextNode) # Remove from the unvisited list
            visited.append(nextNode) # Add to the visited list
        currentNode = nextNode # Move to the next node

    #Check for win condition or return next path
    try:
        if startNode in path: # Check if the start node was included in the path
            if path[1].hole:
                return 'L'
            return path[1] # Return next hexagon
        else:
            if path[0].hole:
                return 'L'
            return path[0] # Return next hexagon
    except:
        return 'W' # Return no hexagon





#--- Main Game ---
class Level():

    #Initalise the game
    def __init__(self, width, height, level):
        self.font = 'freesansbold.ttf' # Initalise the font
        self.level = level  # Initalise the level

        #Settings
        self.settings = {} # Initalise the setting values
        self.fsettings = open('settings.txt', 'r') # Open the setting values

        #Intialise settings
        for line in self.fsettings.readlines(): # Read the lines of settings.txt
            name, val = line.split('=') # Split the text into seperate values
            self.settings[name] = val # Set the value equal to the settings

        #Load the skin
        global mouseImg
        mouseImg = pygame.image.load('assets/' + self.settings['skin'])        

        #Close files
        self.fsettings.close()

        #Pygame Settings
        self.screen = pygame.display.set_mode((width, height)) # Display the screen
        self.clock = pygame.time.Clock() # Get the clock
        self.playing, self.running = True, True


    #Draw Text
    def draw_text(self, text, font, size, screen, color, x, y):
        text_font = pygame.font.Font(font, size) # Initalise the font
        text_surface = text_font.render(text, True, color) # Render the text on the surface
        text_rect = text_surface.get_rect() # Get the rectangle object of the text
        text_rect.center = (x, y) # Center the text to the position
        screen.blit(text_surface, text_rect)

    #Initalise the game board
    def init_gameBoard(self):
        xOffset = 48
        yOffset = 64
        self.hexagons = nx.Graph() # Initalise the hexagon graph

        #Check which level it is
        if self.level == 1:
            
            #Set up the board
            A1 = Hexagon(self.screen, x=BOARDX, y=BOARDY, states=['mouse'])
            A2 = Hexagon(self.screen, x=BOARDX + xOffset, y = BOARDY + (yOffset * 0.5))
            B1 = Hexagon(self.screen, x=BOARDX, y=BOARDY + yOffset)
            B2 = Hexagon(self.screen, x=BOARDX + xOffset, y = BOARDY + (yOffset * 1.5), states=['hole'])
            self.hexagons.add_edges_from([(A1, B1), (A1, B1), (B1, B2), (B2, A2)])
            self.gameBoard = Board(self.hexagons) # Initalse the game board

    
    #Run the game
    def run(self):
        self.init_gameBoard()
        self.game_loop()

    #Game Loop
    def game_loop(self):
        while self.playing: # While the game constantly being looped     
            if self.running:   
                self.screen.fill(BLACK) # Fill the background

                #Check for events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: # Quit Event
                        self.running = False                 

                #Update the game board
                state = self.gameBoard.update()
                if state == 'W':
                    self.draw_text('Win', self.font, 64, self.screen, WHITE, 200, 200)
                    print('Win')
                    self.playing = False

                elif state == 'L':
                    self.draw_text('Lose', self.font, 64, self.screen, WHITE, 200, 200)
                    print('Lose')
                    self.playing = False

                #Update the display
                pygame.display.update() 
            else:    
                break 


# --- Menu ---
class MainMenu():

    #Intialise the menu class
    def __init__(self, width, height, events):
        pygame.init() # Initialise the pygame module
        self.playing, self.running = True, True # Store the state of the menu class
        self.events = events
        self.screen = pygame.display.set_mode((width, height)) # Display the screen
        self.font = 'freesansbold.ttf' # Initalise the font         

    #Run the menu
    def run(self):
        while self.playing:
            if self.running:                           
                self.screen.fill(DARK_GREEN) # Draw the background            
                self.check_events(self.events) # Check if any events have occured                    
                self.update() # Update the display of the menu
            else:
                break

    #Check Events
    def check_events(self, buttonEvents):

        #Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit Event
                self.playing = False
                pygame.quit() 
                

        #Check for button events
        x = 300
        y = 300 
        for button in buttonEvents: # Iterate through all buttons
            if self.button_pressed(self.button(button[0], x, y, 210, 50, RED)): # If the play button is pressed
                time.sleep(0.1) # Delay for button press effect
                button[1].run() # Run the event

                #Check if the game has been quit
                if button[1].running == False:
                    self.running = False
                    break

            #Move the position of the next button
            y += 100 


    #Update the screen
    def update(self):
        pygame.display.update()

    #Draw Button
    def button(self, text, x, y, width, height, color):
        btnRect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, btnRect)
        self.draw_text(text, self.font, 16, self.screen, BLACK, x + width/2, y + height/2)
        return btnRect

    #Check if button is pressed
    def button_pressed(self, button):
            return pygame.mouse.get_pressed()[0] and button.collidepoint(pygame.mouse.get_pos()) # Check if mouse condition matches                

    #Draw Text
    def draw_text(self, text, font, size, screen, color, x, y):
        text_font = pygame.font.Font(font, size) # Initalise the font
        text_surface = text_font.render(text, True, color) # Render the text on the surface
        text_rect = text_surface.get_rect() # Get the rectangle object of the text
        text_rect.center = (x, y) # Center the text to the position
        screen.blit(text_surface, text_rect)




#Run the game
M = MainMenu(WIDTH, HEIGHT, [
                                        ('Play', MainMenu(WIDTH, HEIGHT, [ 
                                                                                ('Levels', MainMenu(WIDTH, HEIGHT, [
                                                                                                                            ('Level 1', Level(WIDTH, HEIGHT, 1))
                                                                                                                    ])),
                                                                                ('Endless', Level(WIDTH, HEIGHT, 1))
                                                                         ])),

                                        ('Skins', Level(WIDTH, HEIGHT, 1)),
                                        ('Settings', Level(WIDTH, HEIGHT, 1))
                            ])
M.run()
