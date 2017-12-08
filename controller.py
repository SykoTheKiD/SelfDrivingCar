import pyautogui as mv

TURN_TIME = 5

def forward():
	mv.keyUp('s')
	mv.keyDown('w')

def left(time=TURN_TIME):
	for i in range(time):
		mv.keyDown('a')
		mv.keyUp('a')

def right(time=TURN_TIME):
	for i in range(time):
		mv.keyDown('d')
		mv.keyUp('d')

def reverse():
	mv.keyUp('w')
	mv.keyDown('s')