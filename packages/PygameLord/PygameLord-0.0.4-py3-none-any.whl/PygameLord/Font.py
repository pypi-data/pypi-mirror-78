#LordLynx
#Part of PygameLord
import pygame, os
from pygame.locals import*
pygame.init()
Path = os.path.dirname(os.path.realpath(__file__));
IBMFONT = pygame.font.Font(Path+'/Resorces/PxPlus_AmstradPC1512.ttf', 12 ) #Loading the defult font for PygameLord this font hass full ASCII potental
'''
Pygame itself has two fonts for itself so why another crafted by me?
But in a way Pygame is infirior Pygame does not have \t or \n suport.
Gaze upon the power this grants you freeing much of your time for your evil plan
'''

'''
display_text(text, font, surface, xpos,ypos, color)
text: Text to display
font: The font to display it with
surface: On wich to display thine text
xpos: The location of the top left corner of the text on the x cordanints
ypos The y positon of the top left corenr
color: the color desired to the theme of thine project.
'''
def display_text(text, font, surface, xpos,ypos, color):
    if font is None: #Check wether to use defult font or not.
        Font = IBMFONT
    else:
        Font = font
    #text rangling parts
    parttext = ''
    for s in text:
        if s == '\t': #Replace Tabs with four spaces...
            parttext += '    '
        else:
            parttext += s
    Text = parttext.split('\n')
    NewText = []
    for t in Text:
        if t != '\n':#Split the new lines up.
            NewText.append(t)
    y = 0
    for i in  NewText:
        FinalTextSurface = Font.render(i,1,color)
        FinalTextRect = FinalTextSurface.get_rect()
        y+= FinalTextRect.height
        FinalTextRect.topleft = (xpos, y+ypos) #assign the text rect
        surface.blit(FinalTextSurface, FinalTextRect)