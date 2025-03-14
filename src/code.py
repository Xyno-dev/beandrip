import usb_hid
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_httpserver import Server, Request, Response, POST
import socketpool
import wifi
import time
import math
import random
from secrets import secrets

time.sleep(2)

m = Mouse(usb_hid.devices)
k = Keyboard(usb_hid.devices)
l = KeyboardLayoutUS(k)

#print(f"Connecting to {secrets['WIFI_SSID']}...")
wifi.radio.connect(secrets['WIFI_SSID'], secrets['WIFI_PASSWORD'])
#print(f"Connected to {secrets['WIFI_SSID']}")

pool = socketpool.SocketPool(wifi.radio)

server = Server(pool, "/static", debug=True)

def indexhtml():
    html = """
        <!DOCTYPE html>
        <head>
            <title>Pico Birb</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,200..1000;1,200..1000&display=swap');
                body {
                    color: #efefff;
                    background-color: #111122;
                    font: 20px Nunito, sans-serif;
                    button {
                        color: #efefff;
                        background-color: #111122;
                        background-image: url('down.svg');
                        padding: 20px 20px;
                        border-radius: 50%;
                    }
                }
            </style>
        </head>
        <body>
            <h1>Pico Birb</h1>
            <hr>
            <p>Welcome to the Pico Birb webserver</p>
            <p>
                <form accept-charset="utf-8" method="POST">
                    <button class="button" name="mouseup" value="up" type="submit"></button>
                    </a>
                </form>
            </p>
            <p>
                <form accept-charset="utf-8" method="POST">
                    <button class="button" name="mousedown" value="down" type="submit"></button>
                    </a>
                </form>
            </p>
            <p>
                <form accept-charset="utf-8" method="POST">
                    <button class="button" name="mouseleft" value="left" type="submit"</button>
                    </a>
                </form>
            </p>
            <p>
                <form accept-charset="utf-8" method="POST">
                    <button class="button" name="mouseright" value="right" type="submit"></button>
                    </a>
                </form>
            </p>
        </body>
    """
    return html

@server.route("/")
def index(request: Request):
    return Response(request, f"{indexhtml()}", content_type="text/html")

@server.route("/", POST)
def buttonpress(request: Request):
    text = request.raw_request.decode("utf8")
    if "up" in text:
        m.move(0, -50)
    if "down" in text:
        m.move(0, 50)
    if "left" in text:
        m.move(-50, 0)
    if "right" in text:
        m.move(50, 0)
    return Response(request, f"{indexhtml()}", content_type="text/html")

server.serve_forever(str(wifi.radio.ipv4_address))