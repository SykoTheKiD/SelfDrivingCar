import numpy as np
from PIL import ImageGrab
import cv2
import time
import pyautogui


def view_region(img, vertices):
	mask = np.zeros_like(img)
	cv2.fillPoly(mask, vertices, 255)
	masked = cv2.bitwise_and(img, mask)
	return masked

def process_image(original_image):
	processed_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
	processed_image = cv2.Canny(processed_image, threshold1=200, threshold2=300)
	vertices = np.array([[10,320],[10,300],[300,200],[500,200],[800,300],[800,320]])
	processed_image = view_region(processed_image, [vertices])
	return processed_image

def main():
	while True:
		screen = np.array(ImageGrab.grab(bbox=(0,40,800,640)))
		new_screen = process_image(screen)
		# cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
		cv2.imshow('window2', new_screen)
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break

if __name__ == "__main__":
	main()