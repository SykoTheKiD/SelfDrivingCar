import sys
import cv2
import math
import numpy as np
import car_errors as ce
import race_track as rt

LOWER_TOLERANCE = 200
UPPER_TOLERANCE = 400

def sigmoid(x):
  return math.fabs(1 / (1 + math.exp(-x)))

def valid_lane(distance):
	return LOWER_TOLERANCE <= distance <= UPPER_TOLERANCE

def detect_yellow(image):
	# sand mask (brown)
	lower = np.uint8([154, 163, 152])
	upper = np.uint8([179, 158, 121])
	brown_mask = cv2.inRange(image, lower, upper)
	# lane line mask (yellow)
	lower = np.uint8([181, 168, 80])
	upper = np.uint8([255, 240, 140])
	yellow_mask = cv2.inRange(image, lower, upper)
	mask = cv2.bitwise_or(yellow_mask, brown_mask)
	return cv2.bitwise_and(image, image, mask=mask)

def hough_lines(image):
    return cv2.HoughLinesP(image, rho=1, theta=np.pi/180, threshold=20, minLineLength=30, maxLineGap=300)

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
	    left_lane  = np.dot(left_weights,  left_lines) / np.sum(left_weights)  if len(left_weights) > 0 else None
	    right_lane = np.dot(right_weights, right_lines) / np.sum(right_weights) if len(right_weights) > 0 else None
	    print(__name__, "Left", left_lane, "Right", right_lane)
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

def distance(left_lane, right_lane):
	return math.sqrt(math.pow((right_lane[0] - left_lane[0]), 2) + math.pow((right_lane[1] - left_lane[1]), 2))

def min_distance(left, right):
	lower = distance(left[0], right[0])
	upper = distance(left[1], right[1])
	return min(lower, upper)

def lane_lines(image, lines):
	if lines is not None:
		left_lane, right_lane = average_slope_intercept(lines)
		turn = rt.STRAIGHT
		if(left_lane is not None and right_lane is not None):
			y1 = image.shape[0] # bottom of the image
			y2 = y1*0.6         # slightly lower than the middle
			if left_lane[0] < 0:
				turn = rt.LEFT_TURN
				turn_time = sigmoid(left_lane[0])
			elif right_lane[0] < 0:
				turn = rt.RIGHT_TURN
				turn_time = sigmoid(right_lane[0])
			left_line  = make_line_points(y1, y2, left_lane)
			right_line = make_line_points(y1, y2, right_lane)
			distance = min_distance(left_line, right_line)
			return left_line, right_line, distance, turn, turn_time

def draw_lane_lines(image, lines, color=[255, 0, 0], thickness=20):
	if lines is not None:
		if not valid_lane(lines[2]):
			return image, ce.ERROR_VALUES[ce.INVALID_LANES], ce.INVALID_LANES, lines[3], lines[4]
		for line in lines[0:2]:
			if line is not None:
				try:
					cv2.line(image, *line,  color, thickness)
				except Exception as e:
					print(__name__, str(e))
		return image, ce.ERROR_VALUES[ce.VALID], ce.VALID, lines[3], lines[4]
	else:
		return image, ce.ERROR_VALUES[ce.NO_LANES], ce.NO_LANES, rt.STRAIGHT, 0.0