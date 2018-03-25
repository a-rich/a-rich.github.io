import os
import shutil
import sys
from flask import Flask, url_for, render_template, send_from_directory
from flask_flatpages import FlatPages
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.html'

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

@app.route('/')
def index():
    return render_template('index.html', pages=pages)

@app.route('/<path:path>/')
def page(path):

    groups = {' '.join([s.capitalize() for s in group.split('-')]):
        sorted([p for p in pages if p.path.split('/')[0] == group],
               key=lambda x: x.meta['title'])
        for group in sorted(set([p.path.split('/')[0]
                                 for p in pages
                                 if p.path.split('/')[0] != 'site']))
        }

    for topic in ['Data Visualization', 'In A Nutshell', 'Machine Learning',
            'Python']:
        if topic not in groups:
            groups[topic] = []

    for k,v in {
            'about': ['about.html', [], ''],
            'all': ['blog_posts.html',
                [(k, [p for p in v]) for k,v in groups.items()],
                'Blog Posts'],
            'data-visualization': ['blog_posts.html',
                groups['Data Visualization'],
                'Data Visualization'],
            'in-a-nutshell': ['blog_posts.html',
                groups['In A Nutshell'],
                'In A Nutshell'],
            'machine-learning': ['blog_posts.html',
                groups['Machine Learning'],
                'Machine Learning'],
            'python': ['blog_posts.html',
                groups['Python'],
                'Python'],
            }.items():

        if k == path.split('/')[-1]:
            return render_template(v[0], pages=v[1], header=v[2])

    page = pages.get_or_404(path).html
    return render_template('content.html', page=page)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
        for directory in ['site', 'machine-learning', 'data-visualization',
                'python', 'in-a-nutshell']:
            if os.path.exists(directory):
                shutil.rmtree(directory)
        if os.path.exists('index.html'):
            os.remove('index.html')
        os.remove('build/index.html')
        shutil.rmtree('build/static')
        os.rename('build/site/about/index.html', 'index.html')
        shutil.rmtree('build/site/about')
        for directory in os.listdir('build'):
            os.rename('build/'+directory, directory)
        shutil.rmtree('build')
    else:
        app.run()
