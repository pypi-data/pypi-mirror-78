#LordLynx
#Part of PygameLord
import pygame, os
from pygame.locals import*
pygame.init()

'''
Load_Sounds(paths,files)
paths: Those folders returned in the Parse locations section
files: a list of your .mp3 or .ogg endings you want to use
Note: you use the ParseLocations in Loads, this is a modified of Lord_Loader code.
'''    
def Load_Sounds(paths,files):
    Sounds = []
    Sounds_Set = {}
    for path in paths:
        file = os.listdir(path)
    
        for Object in file: #loops through the parts
            for fileEnd  in files:
                if Object.endswith(fileEnd):
                    Images.append(os.path.join(path, Object))

    for sound in Sounds:#appends them
        text = os.path.split(image)[-1]
        text = text.split('.')
        text =text[0]
        sound = pygame.mixer.Sound(im)#Here's the defrence it loads them.
        Image_Set[text] = sound
        
    return Image_Set
