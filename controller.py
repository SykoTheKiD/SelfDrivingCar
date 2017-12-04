import pyautogui as mv

def forward():
	mv.keyUp('s')
	mv.keyDown('w')

def left(time=50):
	for i in range(time):
		mv.keyDown('a')
		mv.keyUp('a')

def right(time=50):
	for i in range(time):
		mv.keyDown('d')
		mv.keyUp('d')

def reverse():
	mv.keyUp('w')
	mv.keyDown('s')