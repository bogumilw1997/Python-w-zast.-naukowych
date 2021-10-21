# Bogumił Wierzchowski
# cd .\lab\lab02\
# poetry run python .\program2.py 5 1 0.5 2 5 -g 0.3 -f symulacja

import argparse
import numpy as np
from rich.console import Console
import rich.traceback
from rich.progress import track
import random
import math
from PIL import Image, ImageDraw
import os

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

        step_size = int(image.width / sym.r)

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

console = Console()
console.clear()
console.rule('Symulacja modelu Isinga.')
console.print()

parser = argparse.ArgumentParser(description="Fantastyczny program do wizualizacji modelu Isinga 2D!")
parser.add_argument('r', help='Rozmiar siatki', type=int)
parser.add_argument('j', help='Wartość J', type=float)
parser.add_argument('b', help='Parametr beta', type=float)
parser.add_argument('h', help='Wartość pola H', type=float)
parser.add_argument('k', help='Liczba kroków', type=int)
parser.add_argument('-g', help='Początkowa gęstość spinów', default=0.5, type=float)
parser.add_argument('-f', help='Nazwa pliku z obrazkami', default='step', type=str)

args = parser.parse_args()
r = args.r
j = args.j
b = args.b
h = args.h
k = args.k
g = args.g
f = args.f

sym = Symulacja(r, j, b, h, k, g, f)

path = './obrazki'
try: 
    os.mkdir(path) 
except OSError: 
    pass

n = 0
k = 0

height = 1024
width = 1024

img = sym.rysuj_stan(height, width)
img.save(f'obrazki/{sym.f}0.png')
img.close()

for i in track(sym):
    n += 1
    E1 = i.hamiltonian()

    x = random.randint(0, i.r - 1)
    y = random.randint(0, i.r - 1)
    i.zmien_spin(x, y)

    E2 = i.hamiltonian()

    delta_E = E2-E1

    if (delta_E < 0):
        pass
    else:
        rand = random.uniform(0,1)
        if rand < math.exp(-i.b * delta_E):
            pass
        else:
            i.zmien_spin(x, y)

    if n>=i.r**2:
        k+=1
        n = 0
        img = i.rysuj_stan(height, width)
        img.save(f'obrazki/{sym.f}{k}.png')
        img.close()