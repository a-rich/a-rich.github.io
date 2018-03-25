import sys
import subprocess
from datetime import datetime
from bs4 import BeautifulSoup

if len(sys.argv) <= 1:
    print("ERROR: Must supply at least two command-line arguments...\n\tUsage: python3 converter.py <path/to/ipynb/or/html> <post-title> [<path/to/save/html>]")
    sys.exit()

infile = sys.argv[1]
title = sys.argv[2]

if infile.split('.')[-1] == 'ipynb':
    subprocess.call(['jupyter-nbconvert', infile, '--to', 'html', '--template',
        'basic'])
    infile = '.'.join(infile.split('.')[:-1]) + '.html'

try:
    outfile = sys.argv[3]
except:
    outfile = infile

soup = BeautifulSoup(open(infile, 'r'), 'html.parser')

# Remove weird characters at end of markdown cells
[a.decompose() for a in soup.find_all('a', {'class': 'anchor-link'})]

# Remove prompt brackets before all executable cells
[i.find('div', {'class': 'prompt input_prompt'}).decompose()
        for i in soup.find_all('div', {'class': 'input'})]

# Remove prompt brackets before all outputs
[o.decompose() for o in soup.find_all('div', {'class': 'prompt output_prompt'})]

# Remove extra matplotlib.legend output line
[o.find('pre').decompose()
        for o in soup.find_all('div', {'class': 'output_text'})
        if 'matplotlib' in o.find('pre').get_text()]

"""
# Add well css class to all inputs
for i in soup.find_all('div', {'class': 'input_area'}):
    i['class'] = i.et('class', []) + ['well']
"""

# Change all "small" headers to the smallest
for size in ['4', '5']:
    for h in soup.find_all('h{}'.format(size)):
        h.name = 'h6'

# Change all "big" headers to smaller headers
for size in ['1', '2', '3']:
    for h in soup.find_all('h{}'.format(size)):
        h.name = 'h{}'.format(int(size) + 3)

with open(outfile, 'w') as f:
    meta = 'title: {}\npublished: {}\ntype: {}\n\n'.format(
            title, datetime.now().date(), 'post')
    f.write(meta)
    f.write(str(soup))
