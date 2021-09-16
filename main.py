#Libraries
from os import dup2, system
import pygame
import random
import string
import math
import time
import networkx as nx

#Settings
settings = {} # Initalise the setting values
fsettings = open('settings.txt', 'r') # Open the setting values

#Intialise settings
for line in fsettings.readlines(): # Read the lines of settings.txt
    name, val = line.split('=') # Split the text into seperate values
    settings[name] = val.replace('\n', '') # Set the value equal to the settings


#Close files
fsettings.close()

#Images
hexagonImg = pygame.image.load('assets/hexagon.png')
wallImg = pygame.image.load('assets/wall.png')
holeImg = pygame.image.load('assets/hole.png')
burrowImg = pygame.image.load('assets/burrow.png')
mouseImg = pygame.image.load('assets/' + settings['activeSkin'])
logoImg = pygame.image.load('assets/logo.png')
ventImg = pygame.image.load('assets/vent.png')
winImg = pygame.image.load('assets/win_screen.png')
loseImg = pygame.image.load('assets/lose_screen.png')


#Constants
WIDTH = 800
HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (135, 200, 0)
DARKER_GREEN = (0, 100, 0)
BOARDX = 160
BOARDY = 100


#------------- Hexagon -------------
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

        #Sounds
        self.wallPlaceSound = pygame.mixer.Sound('assets/wall_place.wav') # Place a wall

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
                self.wallPlaceSound.play()
                self.wall = True # Change the object to a wall 
                turn = 'M' # Change the turn to the mouse
            time.sleep(0.1)

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
            global mouseImg
            self.screen.blit(mouseImg, (self.x+16, self.y+16))        

        #Return the next turn
        return turn






#--- Board ---
class Board():
    #Initalise the class
    def __init__(self, graph):
        self.graph = graph # Initalise the hexagons
        self.turn = 'P' # Initalise the turn
        self.turns = 0

        #Find the mouse
        for hex in self.graph.nodes: # Iterate through every hexagon
                if hex.mouse == True: # If the hexagon has the mouse
                    self.mouse = hex

        #Find the hole
        self.hole = []
        for hex in self.graph.nodes: # Iterate through every hexagon
                if hex.hole == True: # If the hexagon has the mouse
                    self.hole.append(hex)

    #Update the board
    def update(self):
        #Mouse's Turn
        if self.turn == 'M':

            #Find next path
            #nextHex = random.choice(list(self.graph.adj[self.mouse]))
            nextHex = next_path(self.graph.subgraph([node for node in self.graph.nodes if not(node.wall)]), self.mouse, self.hole)
            if nextHex == 'W' or nextHex == 'L':
                return nextHex
            else:
                self.mouse.mouse = False # Remove mouse from previous hexagon
                self.mouse = nextHex # Change the next hexagon to the mouse
                self.mouse.mouse = True # Set next hexagon to have the mouse state
            
            self.turns += 1
            self.turn = 'P'

        #Update every hexagon
        for hex in self.graph.nodes: # Iterate through every hexagon
            self.turn = hex.update(self.turn) # Update each hexagon







#------- Shortest Path Algorithim ------
def next_path(graph, startNode, endNodes):

    #Variables
    shortestLength = math.inf
    endNode = None

    #Iterate through all end nodes
    for node in endNodes: 
        if nx.has_path(graph, startNode, node): # Check if a path exists
            if nx.shortest_path_length(graph, startNode, node) < shortestLength: # Check if the shortest length is lower then the other end nodes shortest length
                endNode = node
                shortestLength = nx.shortest_path_length(graph, startNode, node)
    
    #Choose which end node to follow
    if endNode is None:
        return 'W'
    else:
        
        path = nx.shortest_path(graph, startNode, endNode) # Define shortest path
        #Check if you lose if you move to the next node
        if path[1].hole == True:
            return 'L'
        else:
            return path[1]
           

    

    



    







#--- Game/Level ---
class Level():

    #Initalise the game
    def __init__(self, width, height, level):
        self.font = 'freesansbold.ttf' # Initalise the font
        self.level = level  # Initalise the level               

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
        if self.level == 0:
            
            #Set up board variables
            lstHex = {}
            x = BOARDX
            y = BOARDY

            #Create the board
            for i in range(1, 10):
                for j in range(1, 11):
                    lstHex[f'{i}{j}']  = Hexagon(self.screen, x=x, y=y)
                    
                    #Change the position of the next hexagon
                    x += xOffset
                    if j % 2 == 0:
                        y -= (yOffset * 0.5)
                    else:
                        y += (yOffset * 0.5)   

                x = BOARDX             
                y += yOffset

            #Create the inital positions
            lstHex['55'].mouse = True
            holeHex = Hexagon(self.screen, x=-500, y=-500, states=['hole'])
            
            #Add the edges
            for key in lstHex:
                if len(key) == 2:
                    try:                    
                        self.hexagons.add_edge(lstHex[key], lstHex[f'{key[0]}{int(key[1]) + 1}'])
                    except:
                        pass

                    try:                    
                        self.hexagons.add_edge(lstHex[key], lstHex[f'{int(key[0]) + 1}{key[1]}'])
                    except:
                        pass

                    try:                    
                        self.hexagons.add_edge(lstHex[key], lstHex[f'{int(key[0]) - 1}{key[1]}'])
                    except:
                        pass  
            
            #Connect outer hexagons to hole
            for key in lstHex:
                if key[0] == '1' or key[1] == '1' or key[0] == '9':
                    self.hexagons.add_edge(lstHex[key], holeHex)
             
        #Level 1
        elif self.level == 1:
            
            #Initial Board Position
            x = BOARDX + (xOffset * 2)
            y = BOARDY

            A3 = Hexagon(self.screen, x=x, y=y + (yOffset * 1), states=['mouse'])
            B3 = Hexagon(self.screen, x=x, y=y + (yOffset * 2) , states=['burrow'])
            C3 = Hexagon(self.screen, x=x, y=y + (yOffset * 3), states=['burrow'])
            D3 = Hexagon(self.screen, x=x, y=y + (yOffset * 4))
            E3 = Hexagon(self.screen, x=x, y=y + (yOffset * 5), states=['hole'])
            C4 = Hexagon(self.screen, x=x + xOffset, y=y + (yOffset * 3.5))
            C2 = Hexagon(self.screen, x=x - xOffset, y=y + (yOffset * 3.5))
            C1 = Hexagon(self.screen, x=x - (xOffset * 2), y=y + (yOffset * 3), states=['hole'])
            C5 = Hexagon(self.screen, x=x + (xOffset * 2), y=y + (yOffset * 3), states=['hole'])

            self.hexagons.add_edges_from([
                                             (A3, B3), (B3, C3),
                                             (C3, C2), (C3, C4), (C3, D3),
                                             (D3, C2), (D3, C4),
                                             (D3, E3), (C2, C1), (C4, C5)
                                         ])
        
        #Level 2
        elif self.level == 2:
            
            #Initial Board Position
            x = BOARDX
            y = BOARDY

            A1 = Hexagon(self.screen, x=x + (xOffset * 0), y=y + (yOffset * 0), states=['mouse'])
            A2 = Hexagon(self.screen, x=x + (xOffset * 1), y=y + (yOffset * 0.5))
            A3 = Hexagon(self.screen, x=x + (xOffset * 2), y=y + (yOffset * 0))
            B1 = Hexagon(self.screen, x=x + (xOffset * 0), y=y + (yOffset * 1))
            B2 = Hexagon(self.screen, x=x + (xOffset * 1), y=y + (yOffset * 1.5))
            B3 = Hexagon(self.screen, x=x + (xOffset * 2), y=y + (yOffset * 1))
            B4 = Hexagon(self.screen, x=x + (xOffset * 3), y=y + (yOffset * 1.5), states=['hole'])

            self.hexagons.add_edges_from([
                                             (A1, A2), (A1, B1), 
                                             (A2, B1), (A2, B2), (A2, B3), (A2, A3),
                                             (A3, B3),
                                             (B1, B2), (B2, B3), (B3, B4) 
                                         ])
            

        self.gameBoard = Board(self.hexagons) # Initalise the gameboard             
 

    
    #Run the game
    def run(self):
        self.init_gameBoard()
        self.game_loop()

    #Check for win condition
    def win_condition(self, state):
        if state == 'W':
            
            #Display win screen
            self.screen.blit(winImg, (0, 50))
            pygame.display.update() 
            time.sleep(1.1)
            self.playing = False

        elif state == 'L':
            #Display win screen
            self.screen.blit(loseImg, (0, 50))
            pygame.display.update() 
            time.sleep(1.1)
            self.playing = False

    #Game Loop
    def game_loop(self):
        while self.playing: # While the game constantly being looped     
            if self.running:   
                self.screen.fill(DARKER_GREEN) # Fill the background

                #Check for events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: # Quit Event
                        self.running = False                 

                #Update the game board
                state = self.gameBoard.update()
                self.win_condition(state)                

                #Update the display
                self.update()
                
            else:    
                break

    #Update Display
    def update(self):
        self.draw_text(f'Turns: {self.gameBoard.turns}', self.font, 24, self.screen, WHITE, 80, 50)
        pygame.display.update() 










# ---- Menu ----
class MainMenu():

    #Intialise the menu class
    def __init__(self, width, height, events):
        pygame.init() # Initialise the pygame module
        self.playing, self.running = True, True # Store the state of the menu class
        self.events = events
        self.screen = pygame.display.set_mode((width, height)) # Display the screen
        self.font = 'freesansbold.ttf' # Initalise the font        

        #Sounds
        self.buttonPressSound = pygame.mixer.Sound('assets/button_press.wav') # Button Press Sound

        pygame.mixer.music.load('assets/mainmenu.wav') # Main Menu Music
        pygame.mixer.music.play(-1)
               

    #Run the menu
    def run(self):
        while self.playing:
            if self.running:                           
                self.screen.fill(DARK_GREEN) # Draw the background    
                self.screen.blit(logoImg, (0, 0)) # Add the logo        
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
        if self.button_pressed(ventImg.get_rect()):
            time.sleep(0.3)
            self.buttonPressSound.play()
            self.playing = False

        else:
            x = 300
            y = 350 
            for button in buttonEvents: # Iterate through all buttons
                if self.button_pressed(self.button(button[0], x, y, 210, 50, RED)): # If the play button is pressed
                    time.sleep(0.4) # Delay for button press effect
                    self.buttonPressSound.play()
                    button[1].playing = True
                    button[1].run() # Run the event

                    #Check if the game has been quit
                    if button[1].running == False:
                        self.running = False
                        break

                #Move the position of the next button
                y += 100 


    #Update the screen
    def update(self):
        self.screen.blit(ventImg, (0, 0))        
        pygame.display.update()

    #Draw Button
    def button(self, text, x, y, width, height, color):
        btnRect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, btnRect)
        self.draw_text(text, self.font, 16, self.screen, BLACK, x + width/2, y + height/2)
        return btnRect

    #Check if button is pressed
    def button_pressed(self, button):
        if self.playing:
            return pygame.mouse.get_pressed()[0] and button.collidepoint(pygame.mouse.get_pos()) # Check if mouse condition matches                

    #Draw Text
    def draw_text(self, text, font, size, screen, color, x, y):
        text_font = pygame.font.Font(font, size) # Initalise the font
        text_surface = text_font.render(text, True, color) # Render the text on the surface
        text_rect = text_surface.get_rect() # Get the rectangle object of the text
        text_rect.center = (x, y) # Center the text to the position
        screen.blit(text_surface, text_rect)















# ---- Skin Menu ----
class SkinMenu(MainMenu):

    #Intialise the menu class
    def __init__(self, width, height):
        pygame.init() # Initialise the pygame module
        self.playing, self.running = True, True # Store the state of the menu class
        self.screen = pygame.display.set_mode((width, height)) # Display the screen
        self.font = 'freesansbold.ttf' # Initalise the font     

        #Sounds
        self.buttonPressSound = pygame.mixer.Sound('assets/button_press.wav') # Button Press Sound
        pygame.mixer.music.load('assets/mainmenu.wav') # Main Menu Music
        pygame.mixer.music.play(-1)

        #Skins
        skins = ['A', 'B', 'C', 'D']
        fskins = ['F', 'G']
        self.skins = [s for s in skins if s not in fskins] # Get the skins
        self.fskins = fskins # Get the rate up skins

    #Run the menu
    def run(self):
        while self.playing:
            if self.running:                           
                self.screen.fill(DARK_GREEN) # Draw the background 
                self.check_events() # Check events              
                self.update() # Update the display of the menu
            else:
                break
            
    
    #Update the screen
    def update(self):
        self.screen.blit(ventImg, (0, 0))        
        pygame.display.update()

    #Check for events
    def check_events(self):        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit Event
                self.playing = False
                self.running = False
                pygame.quit() 
                

        #Check for button events
        if self.button_pressed(ventImg.get_rect()):
            time.sleep(0.3)
            self.buttonPressSound.play()
            self.playing = False

        aSkins = [pygame.image.load(f'assets/{skin}') for skin in settings['availableSkins'].split(',')]  # Retrieve available skins
        scaledSkins = [pygame.transform.scale(skin, (128, 128)) for skin in aSkins] # Scale the skins

        #Place the skins in the correct position
        x = 100
        y = 100
        for i in range(len(scaledSkins)): # Iterate through all the skins
            if self.button_pressed(self.screen.blit(scaledSkins[i], (x, y))):
                #Effects
                time.sleep(0.3)
                self.buttonPressSound.play()

                #Change the skin
                settings['activeSkin'] = aSkins[i]
                global mouseImg
                mouseImg = aSkins[i]
            y += 128
    
      


#Run the game
M = MainMenu(WIDTH, HEIGHT, [
                                        ('Play', MainMenu(WIDTH, HEIGHT, [ 
                                                                                ('Levels', MainMenu(WIDTH, HEIGHT, [
                                                                                                                            ('Level 1', Level(WIDTH, HEIGHT, 1)),
                                                                                                                            ('Level 2', Level(WIDTH, HEIGHT, 2))
                                                                                                                    ])),
                                                                                ('Endless', Level(WIDTH, HEIGHT, 0))
                                                                         ])),

                                        ('Skins', SkinMenu(WIDTH, HEIGHT)),
                                        ('Settings', Level(WIDTH, HEIGHT, 1))
                            ])
M.run()
