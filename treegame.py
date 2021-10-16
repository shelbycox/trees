import pygame
import sys
import math
import ast
from prufer import *
from tropicalLines import *
from drawTree import *
from mouseover import *

##test
#from drawTreeTest import verts, edges

##special starting trees
##gives an example of a line segment in codimension 1
u = {(1, 2): 40, (2, 1): 40, (1, 3): 40, (3, 1): 40, (1, 4): 40, (4, 1): 40, (1, 5): 40, (5, 1): 40, (2, 3): 30, (3, 2): 30, (2, 4): 30, (4, 2): 30, (2, 5): 30, (5, 2): 30, (3, 4): 20, (4, 3): 20, (3, 5): 20, (5, 3): 20, (4, 5): 10, (5, 4): 10}
v = {(1, 2): 1, (2, 1): 1, (1, 3): 2, (3, 1): 2, (1, 4): 3, (4, 1): 3, (1, 5): 4, (5, 1): 4, (2, 3): 2, (3, 2): 2, (2, 4): 3, (4, 2): 3, (2, 5): 4, (5, 2): 4, (3, 4): 3, (4, 3): 3, (3, 5): 4, (5, 3): 4, (4, 5): 4, (5, 4): 4}
# print(argmaxm(u))
# print(argmaxm(v))
# print(rec_tree_paren(u, [i+1 for i in range(6)]))
# print(rec_tree_paren(v, [i+1 for i in range(6)]))

line = normalize_heights(get_line_int(u,v), 2)

trees = [rec_vertices(T, 375/2, rec_tree_paren(T, [i+1 for i in range(5)]), 300/2, None, [], []) for T in line]

n = 5

##drawing methods
##draws the trees (i-1), i, (i+1) in a row (if they all exist)
def draw_trees(trees, i):
	##draws the tree i in the middle
	draw_tree(trees[i][0], trees[i][1], 1)

	if i - 1 >= 0:
		draw_tree(trees[i-1][0], trees[i-1][1], 0)

	if i + 1 < len(trees):
		draw_tree(trees[i+1][0], trees[i+1][1], 2)

##draws a tree, given the position of vertices and edges
##the box number 0, 1, or 2 puts it in the left, right or center box
def draw_tree(vt, ed, box):
	for e in ed:
		start, end = e
		if len(start) > 2:
			start = (start[0], 555)
		if len(end) > 2:
			end = (end[0], 555)
		start = (start[0] + box*350, start[1])
		end = (end[0] + box*350, end[1])
		pygame.draw.line(screen, black, start, end, 1)

	for v in vt:
		if v[1] == 0:
			##put the number of the vertex at 560
			v_label = font.render(str(v[2]), True, (0, 0, 0))
			screen.blit(v_label, dest=(v[0] - 5 + box*350, 555))
		else:
			pygame.draw.circle(screen, black, (v[0] + box*350, v[1]), 5, 0)

##generate a "picture" of the tropical line
##n is the number of turning points
def gen_line(n):
	x_values = [i*2*math.pi/(n-1) for i in range(n)]
	points = [(x*(625/(2*math.pi)) + 25, (math.sin(x) + 1.5)*100) for x in x_values]
	return points

##draws the basic background, P is the list of points on the tropical line
def draw_background(P):
	##make the background color
	screen.fill(white)

	##draw the tropical line
	pygame.draw.lines(screen, black, False, P, 2)
	for p in P:
		pygame.draw.circle(screen, darkGreen, p, 10, 0)


	##draw a space for the tree display
	R = [(25,300), (350, 300), (350, 575), (25, 575)]
	pygame.draw.lines(screen, black, True, R, 1)
	R = [(a + 350, b) for (a,b) in R]
	pygame.draw.lines(screen, black, True, R, 1)
	R = [(a + 350, b) for (a,b) in R]
	pygame.draw.lines(screen, black, True, R, 1)

	##draw guide lines for the heights
	for i in range(n-2):
		h = 545 - (250/n)*i
		pygame.draw.line(screen, pink, (25, h), (350, h), 1)
		pygame.draw.line(screen, pink, (375, h), (375 + 325, h), 1)
		pygame.draw.line(screen, pink, (375 + 350, h), (375 + 675, h), 1)

	if current != None:
		##space for fine codim, coarse codim
		text_surface_1 = font.render('fcd: ' + str(get_fine_codim(line[2*current[-1] + current[0]])), True, (0, 0, 0))
		screen.blit(text_surface_1, dest=(400, 310))
		text_surface_2 = font.render('ccd:' + str(get_coarse_codim(line[2*current[-1] + current[0]])), True, (0, 0, 0))
		screen.blit(text_surface_2, dest=(400, 335))
		text_contribution = font.render('cont: ' + str(contribution(line[2*current[-1] + current[0]],n)), True, (0, 0, 0))
		screen.blit(text_contribution, dest=(400, 360))

		##write the prufer sequence under the middle tree
		text_prufer = font.render(str(get_prufer(get_adj(line[2*current[-1] + current[0]], n))), True, (0, 0, 0))
		screen.blit(text_prufer, dest=(400, 585))

		draw_trees(trees, 2*current[-1] + current[0])

		if current[0] == 0:
			pygame.draw.circle(screen, blue, current[1], 5, 0)

		if current[0] == 1:
			pygame.draw.circle(screen, blue, ((current[1][0] + current[2][0])/2, (current[1][1] + current[2][1])/2), 5, 0)

	##draw the generate random trees button
	pygame.draw.rect(screen, green, button)
	random_button_text = font.render('random trees', True, (0,0,0))
	screen.blit(random_button_text, dest=(735, 115))

	##draw the save button
	pygame.draw.rect(screen, lightBlue, save_button)
	save_button_text = font.render('save', True, (0,0,0))
	screen.blit(save_button_text, dest=(735, 190))

	##draw the load button
	pygame.draw.rect(screen, pink, load_button)
	load_button_text = font.render('load', True, (0,0,0))
	screen.blit(load_button_text, dest=(735, 40))

	##write the NNI distance
	text_nni_dist = font.render('NNI distance: ' + str(nni_distance(u,v,n)), True, (0, 0, 0))
	screen.blit(text_nni_dist, dest=(735, 265))

##color names
red = (255,0,0)
green = (0,255,0)
lightBlue = (10,255,255)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
darkGreen = (5, 146, 5)

##start the game
pygame.init()

font = pygame.font.Font(pygame.font.get_default_font(), 18)

##start the screen
screen = pygame.display.set_mode((1100, 620))

##button to generate some random trees
button = pygame.Rect(725, 100, 150, 50)

##button to save the current trees
save_button = pygame.Rect(725, 175, 150, 50)

##button to load an example
load_button = pygame.Rect(725, 25, 150, 50)

##get points
P = gen_line(int((len(line) + 1)/2))
lines = [(P[i], P[i+1]) for i in range(len(P) - 1)]

##center of tree display box
center = (375/2, 875/2)

##keeps track of the current tree being displayed
current = None

##make the background image
draw_background(P)

while True:
	for event in pygame.event.get():
		##check for quit events
		if event.type == pygame.QUIT:
			pygame.quit(); sys.exit();

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = event.pos  # gets mouse position
			# checks if mouse position is over the button
			if button.collidepoint(mouse_pos):
				# prints current location of mouse
				T1 = gen_tree(n+1)
				up = get_metric(T1)
				u = {(i,j) : up[(i,j)] for (i,j) in up.keys() if i != 0 and j != 0}
				
				T2 = gen_tree(n+1)
				vp = get_metric(T2)
				v = {(i,j) : vp[(i,j)] for (i,j) in vp.keys() if i != 0 and j != 0}

				line = normalize_heights(get_line_int(u,v), 2)

				trees = [rec_vertices(T, 375/2, rec_tree_paren(T, [i+1 for i in range(n)]), 300/2, None, [], []) for T in line]

				##get points
				P = gen_line(int((len(line) + 1)/2))
				lines = [(P[i], P[i+1]) for i in range(len(P) - 1)]

				current = None

				draw_background(P)


			if save_button.collidepoint(mouse_pos):
				##save the first and last trees!
				u = line[0]
				v = line[-1]
				
				with open('tree_example.txt', 'w') as f:
					f.write(str(u))
					f.write('\n')
					f.write(str(v))

			if load_button.collidepoint(mouse_pos):
				##load the trees as the first and last
				examples = []
				try:
					with open('tree_example.txt', 'r') as f:
						s = f.readline()
						while s:
							t = ast.literal_eval(s)
							examples.append(t)
							s = f.readline()

					##get the line between the two trees
					u, v = examples
					line = normalize_heights(get_line_int(u,v), 2)
					trees = [rec_vertices(T, 375/2, rec_tree_paren(T, [i+1 for i in range(n)]), 300/2, None, [], []) for T in line]

					##get points
					P = gen_line(int((len(line) + 1)/2))
					lines = [(P[i], P[i+1]) for i in range(len(P) - 1)]

					##reset the background for this example
					draw_background(P)

					##remove the blue placeholder
					current = None

				except FileNotFoundError:
					print('No file to load!')

		##check for arrow presses
		elif event.type == pygame.KEYDOWN:
			if current == None:
				pass
			elif event.key == pygame.K_LEFT:
				i = current[-1]
				if i == 0 and current[0] == 0:
					pass

				##if we're currently on a circle
				elif current[0] == 0:
					i = i - 1
					a = lines[i][0]
					b = lines[i][1]
					current = (not current[0], a, b, i)
					# verts, edges = trees[2*i + 1]
					# draw_tree(verts, edges, 1)
					draw_trees(trees, 2*i + 1)
				##otherwise we're on a line
				else:
					current = (not current[0], P[i], i)
					# verts, edges = trees[2*i]
					# draw_tree(verts, edges, 1)
					draw_trees(trees, 2*i)

			elif event.key == pygame.K_RIGHT:
				i = current[-1]
				if current[0] == 0 and i == len(P) - 1:
					pass

				##FOR k = -1 ONLY!!!
				##if we're currently on a circle
				elif current[0] == 0:
					a = lines[i][0]
					b = lines[i][1]
					current = (not current[0], a, b, i)
					# verts, edges = trees[2*i + 1]
					# draw_tree(verts, edges, 1)
					draw_trees(trees, 2*i + 1)
				##otherwise we're on a line
				else:
					i = i + 1
					current = (not current[0], P[i], i)
					# verts, edges = trees[2*i]
					# draw_tree(verts, edges, 1)
					draw_trees(trees, 2*i)

			draw_background(P)


	##check if the mouse is over one of the circles
	over_circle = -1
	r = 10
	for i in range(len(P)):
		p = P[i]
		if detect_mouse_circle(p, r):
			over_circle = i
			current = (0, p, i)
			break

	if over_circle != -1:
		draw_background(P)
		# verts, edges = trees[2*over_circle]
		# draw_tree(verts, edges, 1)
		draw_trees(trees, 2*over_circle)

	else:
		##check if the mouse is over one of the lines
		over_line = -1
		for i in range(len(lines)):
			a, b = lines[i]
			if detect_mouse_line(a,b, 10):
				over_line = i
				##record the type of current is a line (1), start and end points, and the index of the line
				current = (1, a, b, i)
				break

		if over_line != -1:
			draw_background(P)
			# verts, edges = trees[2*over_line + 1]
			# draw_tree(verts, edges, 1)
			draw_trees(trees, 2*over_line + 1)

		else:
			draw_background(P)

	##update the display
	pygame.display.update()