# Bogumił Wierzchowski
# cd .\lab\lab01\
# poetry run python .\program1.py pan-tadeusz.txt -l 5 -n 15

import argparse
from collections import defaultdict
import re
from keras.preprocessing.text import text_to_word_sequence
from ascii_graph import Pyasciigraph

parser = argparse.ArgumentParser(description="Fantastyczny program do rysowania histogramu słów w pliku!")
parser.add_argument('file', help='Nazwa pliku')
parser.add_argument('-n', '--number', help='Dla ilu wyrazów wyświetlić histogram', type=int, default=10)
parser.add_argument('-l', '--length', help='Minimalna długość histogramowanego słowa', type=int, default=0)
args = parser.parse_args()

file = args.file
n = args.number
l = args.length

with open(file,'r', encoding='utf8') as f:
    text = f.read()
    formated_text = re.sub(r'[0-9…—]+', '', text)
    words = text_to_word_sequence(formated_text)

words_dict = defaultdict(int)

for word in words:
    words_dict[word] += 1

words_dict_filtered = {k: v for k, v in words_dict.items() if len(k) >= l}

words_dict_sorted = sorted(words_dict_filtered.items(), key=lambda x: x[1], reverse=True)

data = words_dict_sorted[:n]

graph = Pyasciigraph()

for line in graph.graph(f'Histogram {n} najdłuższych słów o długości >= {l} z pliku: {file}', data):
    print(line)