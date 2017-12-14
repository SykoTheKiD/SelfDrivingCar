import time
import win32api
import win32con
import pyautogui as mv

def forward():
	mv.keyUp('s')
	mv.keyDown('w')

def left(turn_time):
	mv.keyDown('a')
	time.sleep(turn_time)
	mv.keyUp('a')

def right(turn_time):
	mv.keyDown('d')
	time.sleep(turn_time)
	mv.keyUp('d')

def reverse():
	mv.keyUp('w')
	mv.keyDown('s')

def clear_keys():
	mv.keyUp('w')
	mv.keyUp('a')
	mv.keyUp('s')
	mv.keyUp('d')