#LordLynx
#Part of PygameLord
import pygame
from pygame.locals import*
pygame.init()
'''
Surfaces to display your project on, windows...
Help for these.
'''

'''
resize_window(event)
event: the event set from' for event in pygame.event.get(): ' Alteritivly another way if you desire
it returns a tuple for screen size
'''
def resize_window(event):
    if event.type == VIDEORESIZE:
        SCREEN_SIZE = event.size
        winwith = event.size[0]
        winhight = event.size[1]
        return winwith,winhight
    
'''
Defult set ups for windows thus
pygame.display.set_mode(screensize, otherstuff, bitinteger)
The bitinterger must be 32, 24,16,15 or 8 for best performance 32
The otherstuff is tags for the program, The following are a colection of these tags put for practical purposes
'''
RESIZEABLE_WINDOW = RESIZABLE
SPLASHSCREEB_WINDOW = NOFRAME
OPENGL_WINDOW = OPENGL
FULSCREEN_WINDOW = FULLSCREEN
OPENGL_FULLSCREEN_WINDOW = FULLSCREEN | OPENGL | DOUBLEBUF | HWSURFACE