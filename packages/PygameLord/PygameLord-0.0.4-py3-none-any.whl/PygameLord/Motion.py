#LordLynx
#Part of PygameLord
import pygame, os,math
from pygame.locals import*
pygame.init()
from pygame.math import Vector2
'''
Pygame's roatation is an exelent tool,
yet still somthing can be added for we must be able to lord over drag and drop programs with a point towards function
'''
'''
point_towards(current_pos, point_pos)
current_pos: The pos which the thing to rotate is set
point_pos: The pos to point towards.
Note: the images when put into this ought to have the way you want pointing right.
'''
def point_towards(current_pos, point_pos):
    x1 = current_pos[0]
    y1 = current_pos[1]
    x2 = point_pos[0]
    y2 = point_pos[1]
    position1 = Vector2(current_pos)
    position =  point_pos -  position1
    radius, angle = position.as_polar()
    return(int(angle))