import cv2
import numpy as np
import controller as cn
from PIL import ImageGrab
from lane_detection import draw_lines
import image_processing as ip

def process_image(image, colour=[0,255,0], thickness=30):
	original_image = image
	processed_image = ip.detect_yellow(image)
	processed_image = ip.grayscale(processed_image)
	processed_image = ip.gaussian_blur(processed_image)
	processed_image = ip.canny_transform(processed_image)
	processed_image = ip.view_region(processed_image, np.array([[200,320],[200,300],[300,220],[500,220],[600,300],[600,320]]))
	lines = ip.hough_lines(processed_image)
	original_image = ip.draw_lane_lines(original_image, ip.lane_lines(image, lines))
	return processed_image, original_image

def main():
	while True:
		screen = np.array(ImageGrab.grab(bbox=(0,40,800,640)))
		new_screen, original_image = process_image(screen)
		if new_screen is not None and original_image is not None:
			cv2.imshow('window', new_screen)
			cv2.imshow('window2',cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
			if cv2.waitKey(25) & 0xFF == ord('q'):
				cv2.destroyAllWindows()
				break

if __name__ == "__main__":
	main()
