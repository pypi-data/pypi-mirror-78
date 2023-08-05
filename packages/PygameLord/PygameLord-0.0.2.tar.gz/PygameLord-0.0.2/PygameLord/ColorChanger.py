#LordLynx
#Part of PygameLord
import pygame
from pygame.locals import*
pygame.init()
'''
Color manipulation. Gives you utter power over your images.

'''
'''
ChangeColor(image, color_to_change, color_change_into)

images: The image you wish to change
color_to_change: The color to change in RGB Value
color_to_change: The color that color_to_change is replaced with
'''
def ChangeColor(image, color_to_change, color_change_into):
    image_changed = image
    array = pygame.PixelArray(image_changed)
    array.replace(color_to_change, color_change_into, 0.06)
    del array
    return image_changed