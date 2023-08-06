#LordLynx
#Paer of PygameLord
#Images and the things related to it.
import pygame, os
from pygame.locals import*
pygame.init()
#Tilesset
'''
now a class
If you are unaware of the power of these
open the python docs turn to the tutorial of the object orented part and study.

The Class
Tileset(file, (width, height))
Tilset a single word, A tilesheet is a group of images stuck tgether found in the games of long ago, this class will store and split it when needed 
file: the file to load and store
width: The width of every single tile on the set 
hight: the highth of the tiles on the set they are in a tuple
'''

class Tilesheet:
    def __init__(self, file, space,):
        self.image = pygame.image.load(file) #load the file.
        self.width = space[0] #
        self.height = space[1]
        self.image_width, self.image_height = self.image.get_size() #Get the image size
        self.tile_table = []
        for self.tile_x in range(0, int(int(self.image_width)/int(self.width))): #Splitting it, basicly a loop and a bit of magic
            self.line = []
            self.tile_table.append(self.line)
            for self.tile_y in range(0, int(int(self.image_height)/int(self.height))):
                self.rect = (self.tile_x*self.width, self.tile_y*self.height, self.width, self.height)
                self.line.append(self.image.subsurface(self.rect))

    '''
    Get_Tile(self, x, y)
    Thus it returns the tiles to your use.
    x: X cordanince that starts with 0
    y: same as x but with the y cords
    '''
    def Get_Tile(self, space):
         for X, row in enumerate(self.tile_table):
            if X == space[0]:
                for Y, tile in enumerate(row):
                    if Y == space[1]:
                        return tile
                

'''
pygame projects lacking a tilset they feebly attempt to pull there images like so:
Image1 = ImageLoad('Image1.png')
Image2 = ImageLoad('Image2.png')
Image3 = ImageLoad('Image3.png')
etc, etc etc

 
Perhaps  for larger projects you should  pull them in a dictionary. In the unforunate case that you are un aware of such data types look it up.
Now the code.
'''


'''
Load_Images(paths,files)
paths: The list of folders you wish to use
files: the endings like .png or .jpeg you use
Note: you use the ParseLocations in Loads, this is a modified of Lord_Loader code.
'''    
def Load_Images(paths,files):
    Images = []
    Image_Set = {}
    for path in paths:
        file = os.listdir(path)
    
        for Object in file: #loops through the parts
            for fileEnd  in files:
                if Object.endswith(fileEnd):
                    Images.append(os.path.join(path, Object))

    for image in Images:#appends them
        text = os.path.split(image)[-1]
        text = text.split('.')
        text = text[0]
        im = pygame.image.load(image)#Here's the defrence it loads them.
        Image_Set[text] = im
        
    return Image_Set