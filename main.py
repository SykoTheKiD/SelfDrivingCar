import cv2
import time
import numpy as np
from PIL import ImageGrab
import race_track as rt
from car_status import Car
import lane_detection as ld
import car_controller as cc
import game_controller as gc
import image_processing as ip

DISPLAY_CAR_VIEW = False
DISPLAY_MAIN_VIEW = True

def process_image(image):
	original_image = image
	processed_image = ld.detect_yellow(image)
	processed_image = ip.grayscale(processed_image)
	processed_image = ip.gaussian_blur(processed_image)
	processed_image = ip.canny_transform(processed_image)
	processed_image = ip.view_region(processed_image)
	lines = ld.hough_lines(processed_image)
	original_image, error, message, turn, turn_time = ld.draw_lane_lines(original_image, ld.lane_lines(image, lines))
	return processed_image, original_image, error, message, turn, turn_time

def main():
	car = Car()
	while True:
		screen_image = ImageGrab.grab(bbox=(0,40,800,640))
		screen = np.array(screen_image)
		new_screen, original_image, error, message, turn, turn_time = process_image(screen)
		car.update_car(error, message, turn)
		cc.forward()
		if new_screen is not None and original_image is not None:
			print(__name__, turn)
			if turn == rt.LEFT_TURN:
				cc.left(turn_time)
			elif turn == rt.RIGHT_TURN:
				cc.right(turn_time)
			if car.crashed:
				cc.clear_keys()
				gc.restart_game()
			if DISPLAY_CAR_VIEW:
				cv2.imshow('Car View', new_screen)
			if DISPLAY_MAIN_VIEW:
				cv2.imshow('Lane Lines', cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
			if cv2.waitKey(25) & 0xFF == ord('q'):
				cv2.destroyAllWindows()
				break

if __name__ == "__main__":
	main()
