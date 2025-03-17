import usb_hid
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

m = Mouse(usb_hid.devices)
k = Keyboard(usb_hid.devices)
l = KeyboardLayoutUS(k)

l_to_k = {
        "a": Keycode.A, "b": Keycode.B, "c": Keycode.C, "d": Keycode.D, "e": Keycode.E,
        "f": Keycode.F, "g": Keycode.G, "h": Keycode.H, "i": Keycode.I, "j": Keycode.J,
        "k": Keycode.K, "l": Keycode.L, "m": Keycode.M, "n": Keycode.N, "o": Keycode.O,
        "p": Keycode.P, "q": Keycode.Q, "r": Keycode.R, "s": Keycode.S, "t": Keycode.T,
        "u": Keycode.U, "v": Keycode.V, "w": Keycode.W, "x": Keycode.X, "y": Keycode.Y,
        "z": Keycode.Z, "f1": Keycode.F1, "f2": Keycode.F2, "f3": Keycode.F3, "f4": Keycode.F4,
        "f5": Keycode.F5, "f6": Keycode.F6, "f7": Keycode.F7, "f8": Keycode.F8, "f9": Keycode.F9,
        "f10": Keycode.F10, "f11": Keycode.F11, "f12": Keycode.F12
    }

def move(x: int, y: int, s: int = 0):
    m.move(x, y, s)
    
def write(t: str):
    l.write(t)
    
def super(key):
    global l_to_k
    k.send(Keycode.WINDOWS, l_to_k[key.lower()])
    
def alt(key):
    global l_to_k
    k.send(Keycode.ALT, l_to_k[key.lower()])
    
def arrow(key):
    key = key.lower()
    if key == "up":
        k.send(Keycode.UP_ARROW)
    elif key == "down":
        k.send(Keycode.DOWN_ARROW)
    elif key == "left":
        k.send(Keycode.LEFT_ARROW)
    elif key == "right":
        k.send(Keycode.RIGHT_ARROW)