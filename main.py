from pynput.keyboard import Key, Controller, Listener
import random
import time
import threading
import ctypes

SendInput = ctypes.windll.user32.SendInput
keys = [0x1E, 0x11, 0x20]

PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Actuals Functions
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0,
                        ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def resume():
    global thread
    thread.resume()

def pause():
    global thread
    thread.pause()
    
def stop():
    global thread
    thread.stop()

class buttonClicker(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(buttonClicker, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.clear()
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        keyboard = Controller()
    
        while self.__running.isSet():
            self.__flag.wait()
            
            if not self.__running.isSet():
                return
            
            for key in keys:
                PressKey(key)
                time.sleep(0.5)
                ReleaseKey(key)
                time.sleep(0.5)
        
            random.shuffle(keys)
        return

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def stop(self):
        self.__flag.set()
        self.__running.clear()
    
def on_press(key):
    return

def on_release(key):
    if key == Key.page_up:
        resume()
        
    if key == Key.page_down:
        pause()
    
    if key == Key.end:
        pause()
        stop()
        return False

thread = buttonClicker()
thread.start()

with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()