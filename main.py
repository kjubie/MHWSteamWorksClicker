from pynput.keyboard import Key, Controller, Listener
import random
import time
import threading


keys = ["a", "w", "s"]

def resume():
    global thread
    thread.resume()

def pause():
    global thread
    thread.pause()
    
def stop():
    global thread
    thread.stop()

"""
def buttonPresser():
    keyboard = Controller()
    
    global looping
    
    print(looping)
    
    while(looping):
        for key in keys:
            keyboard.press(key)
            keyboard.release(key)
            time.sleep(0.5)
        
        random.shuffle(keys)
        
    return
"""  
  
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
                keyboard.press(key)
                keyboard.release(key)
                time.sleep(0.25)
        
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