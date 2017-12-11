import cv2
import numpy as np

def grayscale(img):
	return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def gaussian_blur(img, kernel_size=5):
	return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def canny_transform(img, low_threshold=250, high_threshold=400):
	return cv2.Canny(img, threshold1=low_threshold, threshold2=high_threshold)

def view_region(img):
	vertices = np.array([[150,500],[150,300], [300,250], [500,250], [650,300], [650,600]], np.int32)
	mask = np.zeros_like(img)
	cv2.fillPoly(mask, np.int32([vertices]), 255)
	return cv2.bitwise_and(img, mask)