import numpy as np
from PIL import ImageGrab
from numpy.linalg import lstsq
import cv2
import time
import pyautogui as mv
from statistics import mean

kernel_size = 5
low_threshold = 200
high_threshold = 300

def view_region(img, vertices):
	mask = np.zeros_like(img)
	cv2.fillPoly(mask, vertices, 255)
	return cv2.bitwise_and(img, mask)

def grayscale(img):
	return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def gaussian_blur(img):
	return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def canny_transform(img):
	return cv2.Canny(img, threshold1=low_threshold, threshold2=high_threshold)

def average_lane(lane_data):
	x1s = []
	y1s = []
	x2s = []
	y2s = []
	for data in lane_data:
		x1s.append(data[2][0])
		y1s.append(data[2][1])
		x2s.append(data[2][2])
		y2s.append(data[2][3])
	return int(mean(x1s)), int(mean(y1s)), int(mean(x2s)), int(mean(y2s))

def forward():
	mv.keyUp('s')
	mv.keyDown('w')

def left():
	mv.keyDown('a')
	mv.keyUp('a')

def right():
	mv.keyDown('d')
	mv.keyUp('d')

def reverse():
	mv.keyUp('w')
	mv.keyDown('s')


def draw_lines(img, lines):
	try:
		ys = []
		for i in lines:
			for ii in i:
				ys += [ii[1], ii[3]]
		min_y = min(ys)
		max_y = 600
		line_dict = {}

		for idx, i in enumerate(lines):
			for xyxy in i:
				x_coords = (xyxy[0], xyxy[2])
				y_coords = (xyxy[1], xyxy[3])
				A = np.vstack([x_coords, np.ones(len(x_coords))]).T
				m, b = lstsq(A, y_coords)[0]
				
				x1 = (min_y-b) / m
				x2 = (max_y-b) / m

				line_dict[idx] = [m, b, [int(x1), min_y, int(x2), max_y]]

		final_lanes = {}

		for idx in line_dict:
			final_lanes_copy = final_lanes.copy()
			m = line_dict[idx][0]
			b = line_dict[idx][1]
			line = line_dict[idx][2]

			if len(final_lanes) == 0:
				final_lanes[m] = [ [m,b,line] ]

			else:
				found_copy = False

				for other_ms in final_lanes_copy:

					if not found_copy:
						if abs(other_ms*1.2) > abs(m) > abs(other_ms*0.8):
							if abs(final_lanes_copy[other_ms][0][1]*1.2) > abs(b) > abs(final_lanes_copy[other_ms][0][1]*0.8):
								final_lanes[other_ms].append([m,b,line])
								found_copy = True
								break
							else:
								final_lanes[m] = [ [m,b,line] ]

		line_counter = {}
		for lanes in final_lanes:
			line_counter[lanes] = len(final_lanes[lanes])

		top_lanes = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]

		lane1_id = top_lanes[0][0]
		lane2_id = top_lanes[1][0]

		l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
		l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])

		return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], lane1_id, lane2_id
	
	except Exception as e:
		print("DRAW LINES", str(e))


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
		# print("ORIGINAL ERROR", str(e))
		pass
	
	try:
		for coords in lines:
			coords = coords[0]
			try:
				cv2.line(processed_image, (coords[0], coords[1]), (coords[2], coords[3]), [255,0,111], 3)
			except Exception as e:
				# print(str(e))
				pass
	except Exception as e:
		# print(str(e))
		pass

	return processed_image, original_image, m1, m2

def main():
	while True:
		screen = np.array(ImageGrab.grab(bbox=(0,40,800,640)))
		new_screen, original_image, m1, m2 = process_image(screen)
		cv2.imshow('window', new_screen)
		forward()
		cv2.imshow('window2',cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
		print(m1, m2)
		if m1 < 0 and m2 < 0:
			for i in range(3):
				right()
		if m1 > 0 and m2 > 0:
			for i in range(3):
				left()
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break

if __name__ == "__main__":
	main()