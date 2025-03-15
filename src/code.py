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

autoclick = False

print(f"Connecting to {secrets['WIFI_SSID']}...")
wifi.radio.connect(secrets['WIFI_SSID'], secrets['WIFI_PASSWORD'])
print(f"Connected to {secrets['WIFI_SSID']}")

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
                }
                button {
                    width: 50px;
                    height: 50px;
                    border-radius: 50%;
                    border: none;
                }
                .up {
                    background: url('https://raw.githubusercontent.com/Xyno-dev/beandrip/refs/heads/main/up.svg') no-repeat center;
                    background-size: contain;
                }
                .down {
                    background: url('https://raw.githubusercontent.com/Xyno-dev/beandrip/refs/heads/main/down.svg') no-repeat center;
                    background-size: contain;
                }
                .left {
                    background: url('https://raw.githubusercontent.com/Xyno-dev/beandrip/refs/heads/main/left.svg') no-repeat center;
                    background-size: contain;
                }
                .right {
                    background: url('https://raw.githubusercontent.com/Xyno-dev/beandrip/refs/heads/main/right.svg') no-repeat center;
                    background-size: contain;
                }
            </style>
        </head>
        <body>
            <h1>Pico Birb</h1>
            <hr>
            <p>Welcome to the Pico Birb webserver</p>
            <p>
                <form accept-charset="utf-8" method="POST">
                    <button class="up" name="mouseup" value="up" type="submit"></button>
                    </a>
                </form>
            </p>
            <p>
                <form accept-charset="utf-8" method="POST">
                    <button class="down" name="mousedown" value="down" type="submit"></button>
                    </a>
                </form>
            </p>
            <p>
                <form accept-charset="utf-8" method="POST">
                    <button class="left" name="mouseleft" value="left" type="submit"></button>
                    </a>
                </form>
            </p>
            <p>
                <form accept-charset="utf-8" method="POST">
                    <button class="right" name="mouseright" value="right" type="submit"></button>
                    </a>
                </form>
            </p>
            <p>
                <form accept-charset="utf-8" method="POST">
                    <button class="autoclick" name="autoclick" value="autoclick" type="submit">autoclick</button>
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
    global autoclick
    text = request.raw_request.decode("utf8")
    if "up" in text:
        m.move(0, -50)
    if "down" in text:
        m.move(0, 50)
    if "left" in text:
        m.move(-50, 0)
    if "right" in text:
        m.move(50, 0)
    if "autoclick" in text:
        autoclick = not autoclick
        print(f"Autoclick toggled: {autoclick}")
    return Response(request, f"{indexhtml()}", content_type="text/html")

def autoclicker():
    global autoclick
    if autoclick:
        m.press(Mouse.LEFT_BUTTON)
        time.sleep(0.03)
        m.release(Mouse.LEFT_BUTTON)
        time.sleep(0.03)

server.start()

while True:
    try:
        server.poll()
        autoclicker()
    except Exception as e:
        print(f"Error: {e}")


