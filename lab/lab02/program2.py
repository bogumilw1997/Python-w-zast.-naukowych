# Bogumił Wierzchowski
# cd .\lab\lab02\
# poetry run python .\program2.py 10 1 0.5 2 5 -g 0.3 -f symulacja

import argparse
import numpy as np
from rich.console import Console
import rich.traceback
from rich.progress import track
import random
import math
from PIL import Image, ImageDraw
import os
from klasy import Symulacja

rich.traceback.install()
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

height = 200 * r
width = 200 * r

images = []

img0 = sym.rysuj_stan(height, width)
img0.save(f'obrazki/{sym.f}0.png')

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
        images.append(img)
        img.save(f'obrazki/{sym.f}{k}.png')

img0.save(f'{sym.f}.gif', save_all=True, append_images=images, optimize=False, duration=500, loop=0)
