#
##methods to detect where the mouse is!
#
import pygame
import math

##get distance
##assumes a,b have same number of entries
def get_dist_sq(a,b):
	return sum([(a[i] - b[i])**2 for i in range(len(a))])

##method to detect when mouse is over a circle
def detect_mouse_circle(center, radius):
	loc = pygame.mouse.get_pos()

	dist_sq = get_dist_sq(center, loc)
	#print(dist_sq)
	
	if dist_sq < radius**2:
		return True

	return False

##computes the distance from point to the line segment between a, b
def dist_to_line_sq(a, b, point):
	return (((b[0] - a[0])*(a[1] - point[1]) - (a[0] - point[0])*(b[1] - a[1]))**2)/((b[0] - a[0])**2 + (b[1] - a[1])**2)

def get_rect(a,b):
	bottom = max(a[1], b[1])
	top = min(a[1], b[1])
	right = max(a[0], b[0])
	left = min(a[0], b[0])

	return top, bottom, left, right

##detect whether a point is in the rectangle defined by two points a, b
def in_rect(a,b,point):
	y_min, y_max, x_min, x_max = get_rect(a,b)

	x = point[0]
	y = point[1]

	if x > x_min and x < x_max and y > y_min and y < y_max:
		return True

	return False

##given the start, end and thickness, detects whether 
def detect_mouse_line(start, end, thickness):
	loc = pygame.mouse.get_pos()

	##if the mouse is in the rectangle spanned by a,b
	if in_rect(start, end, loc):
		##then check to see if it's within the thickness
		if dist_to_line_sq(start, end, loc) < thickness**2:
			return True

	return False