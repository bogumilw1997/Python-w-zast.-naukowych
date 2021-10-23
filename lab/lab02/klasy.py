import numpy as np
from PIL import Image, ImageDraw
import random

class Symulacja:

    def __init__(self, r, j, b, h, k, g, f):
        self.r = r
        self.j = j
        self.b = b
        self.h = h
        self.k = k
        self.g = g
        self.f = f
        self.spiny = np.zeros((self.r, self.r))

        for i in range(self.r):
            for j in range(self.r):
                rand = random.uniform(0,1)
                if rand >= self.g:
                    self.spiny[i][j] = -1
                else:
                    self.spiny[i][j] = 1

    def hamiltonian(self):

        H = - self.h * self.spiny.sum()

        for i in range(self.r):
            for j in range(self.r):
                if (j == self.r -1 and i == self.r - 1):
                    pass
                elif j == self.r - 1:
                    H += -self.j * self.spiny[i][j] *  self.spiny[i+1][j]
                elif i == self.r - 1:
                    H += -self.j * self.spiny[i][j] *  self.spiny[i][j+1]
                else:
                    H += -self.j * self.spiny[i][j] *  self.spiny[i][j+1]
                    H += -self.j * self.spiny[i][j] *  self.spiny[i+1][j]
        return H

    def __iter__(self):
        for i in range(self.r ** 2 * self.k):
            yield self
    
    def __len__(self):
        return (self.k * self.r**2)
    
    def zmien_spin(self, x, y):
        self.spiny[x][y] = self.spiny[x][y] * (-1)

    def rysuj_stan(self, h, w):

        height = h
        width = w
        image = Image.new(mode='RGB', size = (height,width), color = (255, 255, 255))
        
        draw = ImageDraw.Draw(image)

        x_start = 0
        x_end = image.width
        y_start = 0
        y_end = image.height

        step_size = int(image.width / self.r)

        for x in range(0, image.width, step_size):
            line = ((x, y_start), (x, y_end))
            draw.line(line, fill='black')

        for y in range(0, image.height, step_size):
            line = ((x_start, y), (x_end, y))
            draw.line(line, fill='black')

        for x in range(self.r):
            for y in range(self.r):
                if self.spiny[x,y] == 1:
                    draw.polygon([(step_size/2 + x*step_size,step_size/5 + y*step_size), (step_size/5 + x*step_size, step_size/1.5 + y*step_size), (step_size - step_size/5 + x*step_size, step_size/1.5 + y*step_size)], fill = 'blue')
                else:
                    draw.polygon([(step_size/2 + x*step_size,step_size/1.5 + y*step_size), (step_size/5 + x*step_size, step_size/5 + y*step_size), (step_size - step_size/5 + x*step_size, step_size/5 + y*step_size)], fill = 'red')

        return image