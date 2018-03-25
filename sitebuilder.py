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
    """
    grouped_pages = [sorted([(' '.join([s.capitalize() for s in group.split('-')]), p) for p in pages if p.path.split('/')[0] == group], key=lambda x: x[1].meta['title']) for group in sorted(set([p.path.split('/')[0] for p in pages]))]
    """

    return render_template('index.html', pages=pages)

@app.route('/<path:path>/')
def page(path):
    for k,v in {
            'about': 'about.html',
            'all': 'all.html',
            'data-visualization': 'data-visualization.html',
            'in-a-nutshell': 'in-a-nutshell.html',
            'machine-learning': 'machine-learning.html',
            'python': 'python.html'
            }.items():

        if k == path.split('/')[-1]:
            return render_template(v)

    page = pages.get_or_404(path).html
    return render_template('content.html', page=page)

"""
@app.route('/site/<path:path>/')
def site(path):
    for k,v in {
            'about': 'about.html',
            'all': 'all.html',
            'data-visualization': 'data-visualization.html',
            'in-a-nutshell': 'in-a-nutshell.html',
            'machine-learning': 'machine-learning.html',
            'python': 'python.html'
            }.items():

        if k in path:
            return render_template(v)
"""

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run()
