# Bogumił Wierzchowski
# cd .\lab\lab\lab07\
# poetry run python .\ising_numpy.py 500 1 0.5 2 500

import argparse
import numpy as np
from rich.console import Console
import rich.traceback
from rich.progress import track
import random
import math
from numba import njit

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

def init_spiny(r, j, b, h, k, g, f):

    spiny = np.zeros((r, r))

    for i in range(r):
        for j in range(r):
            rand = random.uniform(0,1)
            if rand >= g:
                spiny[i][j] = -1
            else:
                spiny[i][j] = 1
                
    return spiny

def hamiltonian(spiny, h, r):

    H = - h * spiny.sum()

    for i in range(r):
        for j in range(r):
            if (j == r -1 and i == r - 1):
                pass
            elif j == r - 1:
                H += -j * spiny[i][j] *  spiny[i+1][j]
            elif i == r - 1:
                H += -j * spiny[i][j] *  spiny[i][j+1]
            else:
                H += -j * spiny[i][j] *  spiny[i][j+1]
                H += -j * spiny[i][j] *  spiny[i+1][j]
    return H

def zmien_spin(spiny, x, y):
    spiny[x][y] = spiny[x][y] * (-1)
    return spiny

spiny = init_spiny(r, j, b, h, k, g, f)

for i in track(range(k)):

    E1 = hamiltonian(spiny, h, r)

    x = random.randint(0, r - 1)
    y = random.randint(0, r - 1)
    spiny = zmien_spin(spiny, x, y)

    E2 = hamiltonian(spiny, h, r)

    delta_E = E2-E1

    if (delta_E < 0):
        pass
    else:
        rand = random.uniform(0,1)
        if rand < math.exp(-b * delta_E):
            pass
        else:
            spiny = zmien_spin(spiny, x, y)