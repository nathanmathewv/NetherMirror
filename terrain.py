from mainGame import *

def makemap(objects, block_size):
    temp = [Block((2)*block_size, HEIGHT//2-3*block_size, block_size),
            Block((3)*block_size, HEIGHT//2-3*block_size, block_size),
            Block((4)*block_size, HEIGHT//2-3*block_size, block_size),
            Block(4*block_size, HEIGHT//2-4*block_size, block_size), 
            Block(6*block_size, HEIGHT//2-5*block_size, block_size),
            Block(7*block_size, HEIGHT//2-3*block_size, block_size),
            Block(8*block_size, HEIGHT//2-3*block_size, block_size),
            Block(10*block_size, HEIGHT//2-5*block_size, block_size),
            Block(11*block_size, HEIGHT//2-5*block_size, block_size),
            Block(12*block_size, HEIGHT//2-5*block_size, block_size),
            Block(12*block_size, HEIGHT//2-3*block_size, block_size),
            Block(13*block_size, HEIGHT//2-3*block_size, block_size),
            Block(14*block_size, HEIGHT//2-3*block_size, block_size),
            Block(15*block_size, HEIGHT//2-3*block_size, block_size),
            Block(16*block_size, HEIGHT//2-4*block_size, block_size),
            Block(17*block_size, HEIGHT//2-4*block_size, block_size),
            Block(18*block_size, HEIGHT//2-4*block_size, block_size),
            Block(20*block_size, HEIGHT//2-3*block_size, block_size),
            Block(21*block_size, HEIGHT//2-3*block_size, block_size),
            Block(22*block_size, HEIGHT//2-3*block_size, block_size),
            Block(22*block_size, HEIGHT//2-5*block_size, block_size),
            Block(24*block_size, HEIGHT//2-4*block_size, block_size),
            Block(25*block_size, HEIGHT//2-4*block_size, block_size),
            Block(28*block_size, HEIGHT//2-5*block_size, block_size),
            Block(30*block_size, HEIGHT//2-3*block_size, block_size),
            Block(31*block_size, HEIGHT//2-3*block_size, block_size),
            Block(33*block_size, HEIGHT//2-4*block_size, block_size),
            Block(33*block_size, HEIGHT//2-5*block_size, block_size),
            Block(34*block_size, HEIGHT//2-4*block_size, block_size),
            Block(37*block_size, HEIGHT//2-3*block_size, block_size),
            Block(38*block_size, HEIGHT//2-3*block_size, block_size),
            Block(40*block_size, HEIGHT//2-5*block_size, block_size)]
    
    objects.extend(temp)

    return objects