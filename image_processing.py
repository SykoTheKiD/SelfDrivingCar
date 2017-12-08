import sys
import cv2
import numpy as np

def grayscale(img):
	return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def gaussian_blur(img, kernel_size=5):
	return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def canny_transform(img, low_threshold=250, high_threshold=400):
	return cv2.Canny(img, threshold1=low_threshold, threshold2=high_threshold)

def view_region(img, vertices):
	vertices = np.array([[150,500],[150,300], [300,250], [500,250], [650,300], [650,600]], np.int32)
	mask = np.zeros_like(img)
	cv2.fillPoly(mask, np.int32([vertices]), 255)
	return cv2.bitwise_and(img, mask)

def detect_yellow(image):
	# sand mask
	lower = np.uint8([154, 163, 152])
	upper = np.uint8([179, 158, 121])
	brown_mask = cv2.inRange(image, lower, upper)
	# lane mask
	lower = np.uint8([181, 168, 80])
	upper = np.uint8([255, 240, 140])
	yellow_mask = cv2.inRange(image, lower, upper)
	mask = cv2.bitwise_or(yellow_mask, brown_mask)
	return cv2.bitwise_and(image, image, mask=mask)

def hough_lines(image):
    return cv2.HoughLinesP(image, rho=1, theta=np.pi/180, threshold=20, minLineLength=30, maxLineGap=300)

def draw_lines(image, lines, colour=[255,0,0], thickness=2):
	if lines is not None:
		for line in lines:
			for x1, y1, x2, y2 in line:
				cv2.line(image, (x1, y1), (x2, y2), colour, thickness)
	return image

def average_slope_intercept(lines):
    left_lines    = [] # (slope, intercept)
    left_weights  = [] # (length,)
    right_lines   = [] # (slope, intercept)
    right_weights = [] # (length,)
    if lines is not None:
	    for line in lines:
	        for x1, y1, x2, y2 in line:
	            if x2==x1:
	                continue # ignore a vertical line
	            slope = (y2-y1)/(x2-x1)
	            intercept = y1 - slope*x1
	            length = np.sqrt((y2-y1)**2+(x2-x1)**2)
	            if slope < 0: # y is reversed in image
	                left_lines.append((slope, intercept))
	                left_weights.append((length))
	            else:
	                right_lines.append((slope, intercept))
	                right_weights.append((length))
	    
	    # add more weight to longer lines    
	    left_lane  = np.dot(left_weights,  left_lines) /np.sum(left_weights)  if len(left_weights) > 0 else None
	    right_lane = np.dot(right_weights, right_lines)/np.sum(right_weights) if len(right_weights) > 0 else None
	    
	    return left_lane, right_lane # (slope, intercept), (slope, intercept)

def make_line_points(y1, y2, line):
    """
    Convert a line represented in slope and intercept into pixel points
    """
    if line is None:
        return None
    
    slope, intercept = line
    inf = sys.maxsize // 2
    # make sure everything is integer as cv2.line requires it
    try:
    	x1 = int((y1 - intercept)/slope)
    except OverflowError:
    	x1 = inf
    try:
    	x2 = int((y2 - intercept)/slope)
    except OverflowError:
    	x2 = inf
    y1 = int(y1)
    y2 = int(y2)
    
    return ((x1, y1), (x2, y2))

def lane_lines(image, lines):
	if lines is not None:
		left_lane, right_lane = average_slope_intercept(lines)
		if(left_lane is not None and right_lane is not None):
			y1 = image.shape[0] # bottom of the image
			y2 = y1*0.6         # slightly lower than the middle

			left_line  = make_line_points(y1, y2, left_lane)
			right_line = make_line_points(y1, y2, right_lane)

			return left_line, right_line

    
def draw_lane_lines(image, lines, color=[255, 0, 0], thickness=20):
	# make a separate image to draw lines and combine with the orignal later
	line_image = np.zeros_like(image)
	if lines is not None:
		for line in lines:
			if line is not None:
				try:
					cv2.line(line_image, *line,  color, thickness)
				except Exception as e:
					print(str(e))
		# image1 * α + image2 * β + λ
		# image1 and image2 must be the same shape.
		return cv2.addWeighted(image, 1.0, line_image, 0.95, 0.0)
	else:
		print("No Lanes")
		return image