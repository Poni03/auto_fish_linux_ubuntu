import time
import cv2
import numpy as np
import pyautogui  # Cross-platform, works on Ubuntu as well
import mss

import Xlib.display

# Constants for mouse events
ButtonPress = 4
ButtonRelease = 5

display = Xlib.display.Display()
root = display.screen().root

# 800x600 game window (based on 3440x1440 screen resolution)
# mon = {"top": 420, "left": 1320, "width": 800, "height": 600}

title = "Terraria Auto-Fishing"
sct = mss.mss()

print("STARTING after 15 seconds, please adjust your rod!")
time.sleep(15)
print("Started ...")

click()
print("Rod dropped ...")
last_time = time.time() # time last fish was catched


def get_mouse_position():
    """Gets the current mouse position using Xlib."""
    data = root.query_pointer()._data
    return data["root_x"], data["root_y"]

def click():
    """Simulates a mouse click using Xlib."""
    x, y = get_mouse_position()
    root.warp_pointer(x, y)
    root.send_event(Xlib.event.ButtonPress(None, ButtonPress, 1, x, y, 0))
    root.send_event(Xlib.event.ButtonRelease(None, ButtonRelease, 1, x, y, 0))
    root.flush()


while True:
    # must be at least 2 seconds before last catch
    if time.time() - last_time < 2:
        continue
 
    cur_x, cur_y = get_mouse_position()
    mon = {"top": cur_y -5, "left": cur_x -5, "width": 10, "height": 10}
    img = np.asarray(sct.grab(mon))
 
    #cv2.imshow(title, img)
    #if cv2.waitKey(25) & 0xFF == ord("q"):
    #   cv2.destroyAllWindows()
    #   quit()
 
    # create hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
 
    # define masks
    # lower mask (0-10)
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask0 = cv2.inRange(hsv, lower_red, upper_red)
 
    # upper mask (170-180)
    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
 
    # join masks
    mask = mask0+mask1
 
    # check
    hasRed = np.sum(mask)
    if hasRed > 0:
        print("RED detected!") # do nothing
        pass
    else:
        print("RED NOT detected!") # catch!
 
        # get the stuff
        print("Catch! ...")
        time.sleep(0.3)
        click()
 
        time.sleep(1) # wait some
        print("New rod dropped ...")
        click()
 
        last_time = time.time() # time last fish was catched
