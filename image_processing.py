import cv2
import numpy as np

def grayscale(img):
	return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def gaussian_blur(img, kernel_size=5):
	return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def canny_transform(img, low_threshold=200, high_threshold=300):
	return cv2.Canny(img, threshold1=low_threshold, threshold2=high_threshold)

def view_region(img, vertices):
	mask = np.zeros_like(img)
	cv2.fillPoly(mask, vertices, 255)
	return cv2.bitwise_and(img, mask)