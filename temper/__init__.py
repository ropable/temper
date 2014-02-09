from flask import Flask
from flaskext.cache import Cache

# Configure application
DEBUG = True
CACHE_TYPE = 'simple'
CACHE_DEFAULT_TIMEOUT = 60 * 5  # Cache for 5 minutes by default.
CACHE_THRESHOLD = 20
TEMP_LOGS = '/var/log/temps'
TEMP_SENSORS = ['Interior', 'Exterior']  # Order is important.
GPIO_PINS = [17, 18, 21]
GPIO_CFG = 'gpio.cfg'

app = Flask(__name__)
cache = Cache(app)
app.config.from_object(__name__)

import temper.views
