#Libraries
import pygame
import random
import networkx as nx

#Initalise modules
pygame.init()
fsettings = open('settings.txt', 'r')
settings = {}

#Intialise settings
for line in fsettings.readlines():
    name, val = line.split('=')
    settings[name] = val


#Board Variables
hexagonImg = pygame.image.load('assets/hexagon.png')
wallImg = pygame.image.load('assets/wall.png')
mouseImg = pygame.image.load('assets/' + settings['skin'])
holeImg = pygame.image.load('assets/hole.png')
burrowImg = pygame.image.load('assets/burrow.png')

#Constants
WIDTH = 800
HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARDX = 350
BOARDY = 120

#Pygame Settings
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Display the screen
clock = pygame.time.Clock() # Get the clock

#Close files
fsettings.close()






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






#--- Game Loop ---
def game_loop():
    global gameLoop
    #Draw the background
    screen.fill(BLACK)

    #Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Quit Event
            gameLoop = False

    #Update display
    state = gameBoard.update()
    if state == 'W':
        print('Win')
        gameLoop = False
    elif state == 'L':
        print('Lose')
        gameLoop = False
    pygame.display.update()






#--- Game Board ---
hexagons = nx.Graph() # Initalise the hexagon graph
A1 = Hexagon(x=BOARDX, y=BOARDY)
A2 = Hexagon(x=BOARDX + 48, y=BOARDY + (64 * 0.5))
A3 = Hexagon(x=BOARDX + (48 * 2), y=BOARDY, states=['hole'])
A4 = Hexagon(x=BOARDX + (48 * 3), y=BOARDY + (64 * 0.5))
A5 = Hexagon(x=BOARDX + (48 * 4), y=BOARDY)
B1 = Hexagon(x=BOARDX, y=BOARDY + 64)
B2 = Hexagon(x=BOARDX + 48, y=BOARDY + (64 * 1.5))
B3 = Hexagon(x=BOARDX + (48 * 2), y=BOARDY + 64)
B4 = Hexagon(x=BOARDX + (48 * 3), y=BOARDY + (64 * 1.5))
B5 = Hexagon(x=BOARDX + (48 * 4), y=BOARDY + 64)
C1 = Hexagon(x=BOARDX, y=BOARDY + (64 * 2))
C2 = Hexagon(x=BOARDX + 48, y = BOARDY + (64 * 2.5))
C3 = Hexagon(x=BOARDX + (48 * 2), y=BOARDY + (64 * 2))
C4 = Hexagon(x=BOARDX + (48 * 3), y = BOARDY + (64 * 2.5))
C5 = Hexagon(x=BOARDX + (48 * 4), y=BOARDY + (64 * 2), states=['mouse'])
D1 = Hexagon(x=BOARDX, y=BOARDY + (64 * 3))
D2 = Hexagon(x=BOARDX + 48, y=BOARDY + (64 * 3.5))
D3 = Hexagon(x=BOARDX + (48 * 2), y=BOARDY + (64 * 3))
D4 = Hexagon(x=BOARDX + (48 * 3), y=BOARDY + (64 * 3.5))
D5 = Hexagon(x=BOARDX + (48 * 4), y=BOARDY + (64 * 3))


hexagons.add_edges_from([
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
gameBoard = Board(hexagons) # Initalse the game board


#Run the game loop
gameLoop = True
while gameLoop: 
    game_loop()
