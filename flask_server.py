from flask import Flask, render_template, request, request_started
from search import handle_query

app = Flask(__name__)

# NOTE: Start server using python gui.py

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html', result=None)
    if request.method == 'POST':
        # Send query
        top_urls = handle_query(request.form.get('search'))
        return render_template('index.html', result=top_urls)