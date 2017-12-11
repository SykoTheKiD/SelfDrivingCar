import time
import win32api
import win32con
import pyautogui as mv
from PIL import ImageOps, ImageGrab

def start_game():
	mouse_move(400, 324)
	left_mouse_click()

def restart_game():
	mv.keyDown('esc')
	mv.keyUp('esc')
	time.sleep(0.1)
	start_game()

def mouse_move(x, y):
	win32api.SetCursorPos((x, y))

def left_mouse_click():
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
	time.sleep(.1)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def get_cords():
	x, y = win32api.GetCursorPos()
	return x, y

def screenGrab():
    im = ImageGrab.grab(bbox=(0,40,800,640))
    return im