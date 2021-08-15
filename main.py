#Libraries
import pygame
import random
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
class MainGame():

    #Initalise the game
    def __init__(self, width, height):
        self.font = 'freesansbold.ttf' # Initalise the font

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
        self.gameLoop = True
        self.running = True

    #Draw Text
    def draw_text(self, text, font, size, screen, color, x, y):
        text_font = pygame.font.Font(font, size) # Initalise the font
        text_surface = text_font.render(text, True, color) # Render the text on the surface
        text_rect = text_surface.get_rect() # Get the rectangle object of the text
        text_rect.center = (x, y) # Center the text to the position
        screen.blit(text_surface, text_rect)

    #Initalise the game board
    def init_gameBoard(self):
        self.hexagons = nx.Graph() # Initalise the hexagon graph
        A1 = Hexagon(self.screen, x=BOARDX, y=BOARDY)
        A2 = Hexagon(self.screen, x=BOARDX + 48, y=BOARDY + (64 * 0.5))
        A3 = Hexagon(self.screen, x=BOARDX + (48 * 2), y=BOARDY, states=['hole'])
        A4 = Hexagon(self.screen, x=BOARDX + (48 * 3), y=BOARDY + (64 * 0.5))
        A5 = Hexagon(self.screen, x=BOARDX + (48 * 4), y=BOARDY)
        B1 = Hexagon(self.screen, x=BOARDX, y=BOARDY + 64)
        B2 = Hexagon(self.screen, x=BOARDX + 48, y=BOARDY + (64 * 1.5))
        B3 = Hexagon(self.screen, x=BOARDX + (48 * 2), y=BOARDY + 64)
        B4 = Hexagon(self.screen, x=BOARDX + (48 * 3), y=BOARDY + (64 * 1.5))
        B5 = Hexagon(self.screen, x=BOARDX + (48 * 4), y=BOARDY + 64)
        C1 = Hexagon(self.screen, x=BOARDX, y=BOARDY + (64 * 2))
        C2 = Hexagon(self.screen, x=BOARDX + 48, y = BOARDY + (64 * 2.5), states=['burrow'])
        C3 = Hexagon(self.screen, x=BOARDX + (48 * 2), y=BOARDY + (64 * 2))
        C4 = Hexagon(self.screen, x=BOARDX + (48 * 3), y = BOARDY + (64 * 2.5))
        C5 = Hexagon(self.screen, x=BOARDX + (48 * 4), y=BOARDY + (64 * 2), states=['mouse'])
        D1 = Hexagon(self.screen, x=BOARDX, y=BOARDY + (64 * 3))
        D2 = Hexagon(self.screen, x=BOARDX + 48, y=BOARDY + (64 * 3.5))
        D3 = Hexagon(self.screen, x=BOARDX + (48 * 2), y=BOARDY + (64 * 3))
        D4 = Hexagon(self.screen, x=BOARDX + (48 * 3), y=BOARDY + (64 * 3.5))
        D5 = Hexagon(self.screen, x=BOARDX + (48 * 4), y=BOARDY + (64 * 3))


        self.hexagons.add_edges_from([
                                (A1, A2), (A2, A3), (A3, A4), (A4, A5),
                                (B1, B2), (B2, B3), (B3, B4), (B4, B5),
                                (B1, A1), (B1, A2), (B2, A2), (B2, B3), 
                                (B3, A2), (B3, A3), (B3, A4),
                                (B4, A4), (B5, A4), (B5, A5),
                                
                                (C1, C2), (C2, C3), (C3, C4), (C4, C5),
                                (C1, B1), (C1, B2), (C2, B2), (C3, B3),
                                (C3, B4), (C4, B4), (C5, B4), (C5, B5),

                                (D1, D2), (D2, D3), (D3, D4), (D4, D5),
                                (D1, C1), (D1, C2), (D2, C2), (D3, C3),
                                (D3, C4), (D4, C4), (D5, C4), (D5, C5)
                                ]) 
        self.gameBoard = Board(self.hexagons) # Initalse the game board

    
    #Run the game
    def run(self):
        self.init_gameBoard()
        self.game_loop()

    #Game Loop
    def game_loop(self):
        while self.gameLoop: # While the game constantly being looped        
            self.screen.fill(BLACK) # Fill the background

            #Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Quit Event
                    self.gameLoop = False
                    self.running = False
                    break                   

            #Update the game board
            state = self.gameBoard.update()
            if state == 'W':
                self.draw_text('Win', self.font, 64, self.screen, WHITE, 200, 200)
                print('Win')
                self.gameLoop = False

            elif state == 'L':
                self.draw_text('Lose', self.font, 64, self.screen, WHITE, 200, 200)
                print('Lose')
                self.gameLoop = False

            #Update the display
            pygame.display.update()








# --- Menu ---
class Menu():

    #Intialise the menu class
    def __init__(self, width, height):
        pygame.init() # Initialise the pygame module
        self.playing, self.running = True, True # Store the state of the menu class
        self.game = MainGame(width, height) # Store the game
        self.screen = pygame.display.set_mode((width, height)) # Display the screen
        self.font = 'freesansbold.ttf' # Initalise the font

         

    #Run the menu
    def menu_loop(self):
        while self.running:
            self.screen.fill(BLACK) # Fill the background

            #Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Quit Event
                    self.playing, self.running = False, False  

            #Check for button events
            if self.button_pressed(self.button('Play', 30, 30, 40, 40, RED)): # If the play button is pressed
                self.playing = False

            #Update display            
            pygame.display.update()
            self.check_state()

    #Check if menu should be active
    def check_state(self):
        if self.running: # If the menu is running
            if not(self.playing): # If the menu is not being played
                self.game.run() # Run the game

                #If the game is not running
                if self.game.running == False:
                    self.running = False

    
    #Draw Button
    def button(self, text, x, y, width, height, color):
        btnRect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, btnRect)
        self.draw_text(text, self.font, 16, self.screen, BLACK, x + width/2, y + height/2)
        return btnRect

    #Check if button is pressed
    def button_pressed(self, button):
        return pygame.mouse.get_pressed()[0] and button.collidepoint(pygame.mouse.get_pos())        


    #Draw Text
    def draw_text(self, text, font, size, screen, color, x, y):
        text_font = pygame.font.Font(font, size) # Initalise the font
        text_surface = text_font.render(text, True, color) # Render the text on the surface
        text_rect = text_surface.get_rect() # Get the rectangle object of the text
        text_rect.center = (x, y) # Center the text to the position
        screen.blit(text_surface, text_rect)

        





#Run the game
M = Menu(WIDTH, HEIGHT)
M.menu_loop()
