import time
import win32api
import win32con
import pyautogui as mv

TURN_TIME = 0.9

def forward():
	mv.keyUp('s')
	mv.keyDown('w')

def left(time=TURN_TIME):
	mv.keyDown('a')
	time.sleep(TURN_TIME)
	mv.keyUp('a')

def right(time=TURN_TIME):
	mv.keyDown('d')
	time.sleep(TURN_TIME)
	mv.keyUp('d')

def reverse():
	mv.keyUp('w')
	mv.keyDown('s')

def center_car(left_lane, right_lane):
	pass
