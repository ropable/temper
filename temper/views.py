from flask import request, render_template
from temper import app


@app.route('/')
def index():
    return render_template('index.html')
