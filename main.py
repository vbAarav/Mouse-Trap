#Libraries
import pygame
import random
import networkx as nx
import matplotlib.pyplot as plt

#Initalise modules
pygame.init()

#Board Variables
hexagonImg = pygame.image.load('hexagon.png')
wallImg = pygame.image.load('wall.png')
mouseImg = pygame.image.load('mouse.png')
holeImg = pygame.image.load('hole.png')
burrowImg = pygame.image.load('burrow.png')

#Constants
WIDTH = 800
HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARDX = 350
BOARDY = 50

#Pygame Settings
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Display the screen
clock = pygame.time.Clock() # Get the clock


#--- Hexagon ---
class Hexagon(pygame.sprite.Sprite):

    #Initalise hexagon object
    def __init__(self, x=0, y=0, states=[]):
        #Properties
        pygame.sprite.Sprite.__init__(self) # Initalise class for game object
        self.x = x # Set the x position of the object
        self.y = y # Set the y position of the object
        self.image = hexagonImg # Set the image of the hexagon
        self.rect = self.image.get_rect() # Set the hitbox of the object
        self.rect.move_ip(x, y) # Update the hitbox

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
        

        screen.blit(self.image, (self.x, self.y)) # Draw the object on the screen

        #Check if there is a mouse on the hexagon
        if self.mouse:
            screen.blit(mouseImg, (self.x+16, self.y+16))        

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
            nextHex = self.mouse
            try: # Check to see if a path can be made
                nextHex = next_path(self.graph, self.mouse, self.hole) # Select the next hexagon
            except:
                nextHex = self.mouse # Do not change choices

            self.mouse.mouse = False # Remove mouse from previous hexagon
            self.mouse = nextHex # Change the next hexagon to the mouse
            nextHex.mouse = True # Set next hexagon to have the mouse state

            self.turn = 'P'

        #Update every hexagon
        for hex in self.graph.nodes: # Iterate through every hexagon
            self.turn = hex.update(self.turn) # Update each hexagon

# Shortest Path Algorthim
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
            nextNode = path[-1]
            path.pop(-1)        
        else: 
            while nextNode in visited: # While the node being chosen has been visited
                nextNode = random.choice(list(graph.adj[currentNode])) # Choose a neigbhbouring node
            path.append(nextNode) # Add the node to the path
            unvisited.remove(nextNode) # Remove from the unvisited list
            visited.append(nextNode) # Add to the visited list
        currentNode = nextNode # Move to the next node

    return path[1]

    

#--- Game Board ---
hexagons = nx.Graph() # Initalise the hexagon graph
A1 = Hexagon(x=BOARDX, y=BOARDY)
B1 = Hexagon(x=BOARDX - 64, y=BOARDY + 64)
B2 = Hexagon(x=BOARDX + 64, y=BOARDY + 64)
C1 = Hexagon(x=BOARDX, y=BOARDY + (64 * 2), states=['hole'])
D1 = Hexagon(x=BOARDX - 64, y=BOARDY + (64 * 3))
D2 = Hexagon(x=BOARDX + 64, y=BOARDY + (64 * 3))
E1 = Hexagon(x=BOARDX, y=BOARDY + (64 * 4))
E2 = Hexagon(x=BOARDX + (64 * 2), y=BOARDY + (64 * 4), states=['burrow'])
F1 = Hexagon(x=BOARDX - 64, y=BOARDY + (64 * 5))
F2 = Hexagon(x=BOARDX + 64, y=BOARDY + (64 * 5))
F3 = Hexagon(x=BOARDX + (64 * 3), y=BOARDY + (64 * 5), states=['burrow'])
G1 = Hexagon(x=BOARDX, y=BOARDY + (64 * 6))
G2 = Hexagon(x=BOARDX + (64 * 4), y=BOARDY + (64 * 6), states=['burrow'])
H1 = Hexagon(x=BOARDX - 64, y=BOARDY + (64 * 7))
H2 = Hexagon(x=BOARDX + 64, y=BOARDY + (64 * 7))
H3 = Hexagon(x=BOARDX + (64 * 3), y=BOARDY + (64 * 7), states=['burrow'])
I1 = Hexagon(x=BOARDX, y=BOARDY + (64 * 8), states=['mouse'])
I2 = Hexagon(x=BOARDX + (64 * 2), y=BOARDY + (64 * 8), states=['burrow'])
J1 = Hexagon(x=BOARDX - 64, y=BOARDY + (64 * 9))
J2 = Hexagon(x=BOARDX + 64, y=BOARDY + (64 * 9))
K1 = Hexagon(x=BOARDX, y=BOARDY + (64 * 10))

hexagons.add_nodes_from([A1, B1, B2, C1, D1, D2, E1, E2, F1, F2, F3, G1, G2, H1, H2, H3, I1, I2, J1, J2, K1]) # Add the hexagons
hexagons.add_edges_from([
                            (A1, B1), (A1, B2), (B1, C1), (B2, C1),
                            (C1, D1), (C1, D2), (D1, E1), (D2, E1),
                            (E1, F1), (E1, F2), (F1, G1), (F2, G1),    # Add the indiviual choices
                            (G1, H1), (G1, H2), (H1, I1), (H2, I1),
                            (I1, J1), (I1, J2), (J1, K1), (J2, K1),
                            (D2, E2), (F2, E2), (F2, F3), (F3, G2),
                            (H2, I2), (J2, I2), (I2, H3), (H3, G2)
                            
                        ]) 
gameBoard = Board(hexagons) # Initalse the game board

#--- Game Loop ---
gameLoop = True
while gameLoop: # Run game loop
    #Draw the background
    screen.fill(BLACK)

    #Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Quit Event
            gameLoop = False

        if event.type == pygame.MOUSEBUTTONDOWN: # Mouse Press Event
            if (event.button == 1):
                pass

    

    #Update display
    gameBoard.update()
    pygame.display.update()
