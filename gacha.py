#Libraries
import pygame
import random

#Initalise pygame module
pygame.init()

#Constants
WINDOW_WIDTH, WINDOW_HEIGHT  = 1280, 480

#Colors
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0


#Set the box window
size = WINDOW_WIDTH, WINDOW_HEIGHT
screen = pygame.display.set_mode(size)

#Text
font = pygame.font.Font('freesansbold.ttf', 22) # Get the font


#Banner
class Banner():
    
    #Initalise the class
    def __init__(self, units, funits, funitRate):
        self.units = [i for i in units if i not in funits] # Initalise the normal banner units
        self.funits = funits # Initalise the featured banner units
        self.funitRate = funitRate

    def summon(self):
        num = random.randint(1, 100)
        if num <= self.funitRate:
            return '-' + random.choice(self.funits)
        else:
            return random.choice(self.units)

    def multiSummon(self, amount):
        return [self.summon() for i in range(amount)]

#Button
class Button():

    #Initalise Button
    def __init__(self, x, y, length, width, text):
        self.x = x
        self.y = y
        self.text = text
        self.pressed = False
        self.rect = pygame.Rect(x, y, length, width)

    #Update
    def update(self):
        pygame.draw.rect(screen, RED, self.rect)
        label = font.render(self.text, True, BLACK)
        screen.blit(label, (self.x + 16, self.y + 24))

    #Check if the button is being clicked method
    def is_clicked(self):        
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.pressed = True
            return True
        else:
            return False


    #Check if the button is being clicked method
    def is_released(self):
        if not(self.is_clicked()) and self.pressed:
            self.pressed = False
            return True   
        else:
            return False

#Show units
def show_units(unit):
    if type(unit) == str: # If the input is a single summon
        if unit[0] == '-':
            label = font.render(f'{unit[1:]}', True, RED)
        else:
            label = font.render(f'{unit}', True, WHITE)
        screen.blit(label, (65, 95)) # Draw the unit
    elif type(unit) == list: # If the input is a multi summon
        #Local Draw Variables
        lx = 80
        ly = 96

        #Iterate through all the units
        for u in unit:
            #Correctly label the text
            if u[0] == '-':
                label = font.render(f'{u[1:]}', True, RED)
            else:
                label = font.render(f'{u}', True, WHITE)
                
            screen.blit(label, (lx, ly))
            if lx >= 900:
                ly += 24
                lx = 80            
            else:
                lx += 240
            

    


#Mechanic Initialisation
singleButton = Button(320, 300, 200, 100, 'Single Summon')
multiButton = Button(760, 300, 200, 100, 'Multi Summon')
allUnits = [
    'Loki', 'Cell', 'Moni', 'Moni Requiem', 'Mash', 'Mash (Blue Masked)', 'Alligator Loki', 'Flipili', 'Impostor (Silohuete)'
           ]

banner = Banner(allUnits, ['Moni Requiem', 'Impostor (Silohuete)'], 5)

#Game Loop
gameLoop = True
result = False
buttonPress = False
while gameLoop:
    screen.fill(BLACK)

     #Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Quit Event
            gameLoop = False

    if singleButton.is_released():
        result = banner.summon()

    if multiButton.is_released():
        result = banner.multiSummon(10)

    #Update
    singleButton.update()
    multiButton.update()
    show_units(result)
    pygame.display.update()