from flask import request, render_template
from temper import app, utils
from datetime import datetime



@app.route('/')
def index():
    temps_list = utils.read_log()
    return render_template('index.html')
