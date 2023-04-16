import os
import random 
import math
import pygame
from os import listdir
from os.path import isfile, join 
from tutorial import *



def makemap(objects, block_size):
    for i in range(3):
        objects.append(Block((i+2)*block_size, HEIGHT - 3*block_size, block_size))
    objects.append(Block(4*block_size, HEIGHT-4*block_size, block_size))    

    return objects