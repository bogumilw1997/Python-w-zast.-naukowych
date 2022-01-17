# cd .\lab\lab\lab08  
# poetry run python .\program8_a.py 

from turtle import color
import rich.traceback
import requests
from bs4 import BeautifulSoup
import urllib.request
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import Future
import os
from skimage.io import imread, imsave
from skimage import img_as_ubyte
import json
from rich.console import Console
import time

def save_img(filtered_link, image):

    img = imread(filtered_link, as_gray=True)
    imsave(f'data/{image}', img_as_ubyte(img))
        
        
if __name__ ==  '__main__':
    
    rich.traceback.install()
    
    console = Console()
    console.print('Zbieranie linkow ...', style="yellow")
    
    start = time.time()
    
    url = 'http://if.pw.edu.pl/~mrow/dyd/wdprir/'

    req = requests.get(url)

    soup = BeautifulSoup(req.text, 'html.parser')

    links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))

    filter = '.png'

    images = [x for x in links if (filter in x)]

    filtered_links = [url + x for x in images]
    
    # with open('links.txt', 'w') as file:
    #     json.dump(filtered_links, file)
    
    req.close()
    
    dirName = 'data'
    try:
        os.mkdir(dirName)

    except FileExistsError:
        pass
    
    console.print('Pobieranie obrazow ...', style="magenta")
    
    for i in range(len(images)):
        save_img(filtered_links[i], images[i])
        
    end = time.time()
    
    console.print(f'Czas wykonywania: {end - start} ms', style="blue")
    