from flask import Flask

# Configure application
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

import temper.views
