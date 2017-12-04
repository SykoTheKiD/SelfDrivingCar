import cv2
import numpy as np
import controller as cn
from lane_detection import draw_lines
from screen_grabber import grab_screen
from image_processing import grayscale, canny_transform, gaussian_blur, view_region

def process_image(image, colour=[0,255,0], thickness=30):
	original_image = image
	processed_image = grayscale(image)
	processed_image = canny_transform(processed_image)
	processed_image = gaussian_blur(processed_image)
	
	vertices = np.array([[200,320],[200,300],[300,220],[500,220],[600,300],[600,320]], np.int32)
	processed_image = view_region(processed_image, [vertices])

	lines = cv2.HoughLinesP(processed_image, 1, np.pi/180, 180, 20, 15)
	m1 = 0
	m2 = 0
	try:
		l1, l2, m1, m2 = draw_lines(original_image, lines)
		cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), colour, thickness)
		cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), colour, thickness)
	except Exception as e:
		print("process_image()", str(e))
	
	try:
		for coords in lines:
			coords = coords[0]
			try:
				cv2.line(processed_image, (coords[0], coords[1]), (coords[2], coords[3]), [255,0,111], 3)
			except Exception as e:
				print("process_image(): ", str(e))
	except Exception as e:
		print("process_image(): ", str(e))

	return processed_image, original_image, m1, m2

def main():
	while True:
		screen = grab_screen()
		new_screen, original_image, m1, m2 = process_image(screen)
		cv2.imshow('window', new_screen)
		cn.forward()
		cv2.imshow('window2',cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
		print(m1, m2)
		if m1 < 0 and m2 < 0:
			cn.right()
		if m1 > 0 and m2 > 0:
			cn.left()
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break

if __name__ == "__main__":
	main()
