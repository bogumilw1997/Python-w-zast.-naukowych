# poetry run python .\program4.py -f output.json -n 4

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import argparse
import pandas as pd
import json
from selenium.webdriver.common.keys import Keys
from rich.console import Console
import rich.traceback
from rich.progress import track

console = Console()
console.clear()
console.rule('Web-scraping, part2.')
console.print()
rich.traceback.install()

parser = argparse.ArgumentParser(description="Web Scraping - dynamic")
parser.add_argument('-f', help='Nazwa pliku do zapisu', default='output.json', type=str)
parser.add_argument('-n', help='Ilość scrollowań', default='3', type=int)

args = parser.parse_args()

output_file = args.f
n = args.n

options = Options()
options.add_argument('--disable-notifications')
service = Service('chromedriver.exe')
driver = webdriver.Chrome(service = service, options=options)

driver.get('https://www.youtube.com/')


button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/div[5]/div[2]/ytd-button-renderer[2]')))
button.click()

time.sleep(2)

html = driver.find_element(By.TAG_NAME, 'html')

start = 0

video_dict = {}

for i in range(n):
    
    videos = driver.find_elements(By.CLASS_NAME, 'style-scope ytd-rich-grid-media')
    
    videos_len = len(videos)
    
    for video in videos[start:]:
        
        if len(video.text) > 0:
            
            title = video.find_element(By.XPATH, './/*[@id="video-title"]').text
            views = video.find_element(By.XPATH, './/*[@id="metadata-line"]/span[1]').text
            video_dict[title] = views
        
    start = videos_len - start
    
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)
    time.sleep(1.5)

with open(f'data/{output_file}', 'w', encoding='utf-8-sig') as f:
    json.dump(video_dict, f, ensure_ascii=False, indent=4)

driver.close()