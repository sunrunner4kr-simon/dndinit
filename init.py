import time

from operator import attrgetter
from socket import socket
from rpi_ws281x import Color, PixelStrip, ws

from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from characters import Character
from seats import Seat
import os.path
from database import db

from index_blueprint import index_blueprint


# LED strip configuration:
LED_COUNT = 91         # Number of LED pixels.
LED_PIN = 18           # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100   # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0
LED_STRIP = ws.SK6812_STRIP_RGBW


# Create app first
def create_app():
    app = Flask(__name__)
    app.register_blueprint(index_blueprint)
    app.secret_key = "hello"
    # SQLITE DB STUFF
    db_name = "init.db"

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    return app


def setup_database(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()


if __name__ == "__main__":
    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
                           LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    #strip.begin()
    app = create_app()
    app.strip = strip
    app.strip.begin()
    if not os.path.isfile('/init.db'):
        setup_database(app)
    app.run(debug=True, host='0.0.0.0')
