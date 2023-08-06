#LordLynx
#Part of PygameLord
import pygame,os
from pygame.locals import*
pygame.init()
#Loading Objects
'''
Parse_Locations(file)
file: Your text file, use  a .txt
# Like in Python will be ingored thusly follow this example

#Coment
./File/File
./File/Other File
...
'''
def Parse_Locations(file):
    file = open(file, 'r')#read the file
    lines = []
    folders = []
    for text_line in file:
        lines.append(text_line) #pull the files info
    file.close()#close it
    moding = []
    for i in lines:
        s =i.strip('\n')#split the lines up
        moding.append(s)
    for i in moding:
        if i  != '\n' and i[0] != '#': #ignore new lines or coments '#'
            folders.append(i)
    return folders
'''
Lord_Loaders(paths,files)
paths: The  folders returned in the Parse_Locations function
files: The .files which you wish to use
Modified versions of this are in Sounds and Images

If the opertunity arises copy and paste this code into your program and change the files like the Image and Sound loaeders
'''
def Lord_Loader(paths,files):
    Files = []
    File_Set = {}
    for path in paths:
        file = os.listdir(path)
    
        for Object in file: #loops through the parts
            for fileEnd  in files:
                if Object.endswith(fileEnd):
                    Images.append(os.path.join(path, Object))
    
    for file in Files:#appends them
        text = os.path.split(file)[-1]
        text = text.split('.')
        text =text[0]
        File_Set[text] = file
        
    return Image_Set