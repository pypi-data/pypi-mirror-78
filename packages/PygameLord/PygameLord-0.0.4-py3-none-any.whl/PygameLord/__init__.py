#LordLynx
#PygameLord
version = '0.0.4'
version_name = "Vez'nan"
import os, sys
#This is PygameLord so clearly pygame comes first.
try: 
    import pygame
except ModuleNotFoundError:
    raise Exception('Please Get Pygame 2.0')
if pygame.get_sdl_version() < (2, 0, 0):
    raise Exception('Please Get Pygame 2.0')
from pygame.locals import*
pygame.init() #We Init it already-yet you should probably run this also in your code
Path = os.path.dirname(os.path.realpath(__file__));
print('Greetings from PygameLord ' + version  +'('+ version_name +')' '.')
'''
At last this  the PygameLord package!, That it tries help with pygame as much as possible.
It will reach it's full power by breaking with open GL into the 3rd dimention.
But of corse, it requires pygame so make sure the module is installed
'''


'''
the pygame module can be acsessed by PygameLord.pygame for ease you should import pygame into your code.
our example will follow that way

import pygame
from pygame.locals import*
pygame.init()

Exelent! 
'''
#Importing the sepreate parts
import PygameLord.ColorChanger #Color changing module.
import PygameLord.Images #Images Modules
import PygameLord.Loads #Loading objects
import PygameLord.Sounds #Loading sounds
import PygameLord.ColorConstants# Colors
import PygameLord.Font#Font
import PygameLord.Surface# Surface stuff
import PygameLord.Motion#Motion
LORD  = pygame.image.load(Path + '/Resorces/PygameLord.png')
pygame.display.set_caption('PygameLord')
pygame.display.set_icon(LORD)

# exiting
def exit():
    pygame.quit()
    
def quit():
    pygame.quit
    sys.exit()