from operator import itemgetter
from flask import Flask, render_template, request

from search import handle_query

app = Flask(__name__)

# NOTE: Start server using python gui.py

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html', urls=None)
    if request.method == 'POST':
        # Send query
        top_urls, search_time = itemgetter('urls', 'search_time')(handle_query(request.form.get('search')))
        return render_template('index.html', urls=top_urls, search_time=search_time)