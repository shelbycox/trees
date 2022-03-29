from tkinter import *
from tkinter.filedialog import askopenfilename
import ast
import drawTreeTk as dt
import tropicalLines as tl
import os
from PIL import Image, ImageDraw

#set num of leaves
n = 8

##colors for PIL
white = (255, 255, 255)
black = (0, 0, 0)

window = Tk()

u = tl.tree_to_dict([10,200,200,2,10,200,200,200,200,10,6,200,200,12,200,200,4,12,200,200,12,8,10,200,200,200,200,12], n)
v = tl.tree_to_dict([200,400,600,800,800,800,800,400,600,800,800,800,800,600,800,800,800,800,800,800,800,800,600,600,600,400,400,200], n)

# u = tl.tree_to_dict([9,13,13,15,15,13,13,15,15,10,15,15,15,15,12], 6)
# v = tl.tree_to_dict([11,8,11,14,15,11,7,14,15,11,14,15,14,15,15], 6)

# u = tl.tree_to_dict([3,3,2], n)
# v = tl.tree_to_dict([1,3,3], n)

# u = tl.tree_to_dict([3,4,4,4,4,1], n)
# v = tl.tree_to_dict([3,2,3,3,1,3], n)

# u = tl.tree_to_dict([3,3,3,2,2,1], n)
# v = tl.tree_to_dict([8,8,8,3,3,1], n)

width = height = 275

# u = {(1, 2): 10, (2, 1): 10, (1, 3): 10, (3, 1): 10, (1, 4): 10, (4, 1): 10, (1, 5): 10, (5, 1): 10, (2, 3): 4, (3, 2): 4, (2, 4): 8, (4, 2): 8, (2, 5): 8, (5, 2): 8, (3, 4): 8, (4, 3): 8, (3, 5): 8, (5, 3): 8, (4, 5): 5, (5, 4): 5}
# v = {(1, 2): 9, (2, 1): 9, (1, 3): 9, (3, 1): 9, (1, 4): 9, (4, 1): 9, (1, 5): 10, (5, 1): 10, (2, 3): 7, (3, 2): 7, (2, 4): 7, (4, 2): 7, (2, 5): 10, (5, 2): 10, (3, 4): 6, (4, 3): 6, (3, 5): 10, (5, 3): 10, (4, 5): 10, (5, 4): 10}

line = tl.normalize_heights(tl.get_tropical_line(u,v), 2)
mus = tl.get_mu(u,v)
trees = [dt.rec_vertices(T, 275/2, tl.rec_tree_paren(T, [i+1 for i in range(n)]), 275/2, None, [], []) for T in line]
heights = [tl.get_heights(x) for x in line]

global left_index, curr_index, right_index, mu

left_index = 0
curr_index = 1
right_index = 2

left = trees[left_index]
curr = trees[curr_index]
right = trees[right_index]

mu = mus[curr_index]

# u_info = dt.rec_vertices(u, 275/2, tl.rec_tree_paren(u, [i+1 for i in range(5)]), 275/2, None, [], [])
def get_bounding_box(x,y,r):
	x0 = x - r
	x1 = x + r
	y0 = y - r
	y1 = y + r
	return [(x0,y0), (x1,y1)]

def draw_circle(x,y,r, canvas_name, f="black"):
	x0 = x - r
	x1 = x + r
	y0 = y - r
	y1 = y + r
	return canvas_name.create_oval(x0,y0,x1,y1,fill=f)

def print_trees(folder_name):
	i=1
	for t in trees:
		print_tree_latex(i, t[0], t[1], tl.get_heights(line[i-1]), folder_name)
		i = i + 1

def print_tree(i, vt, ed, folder_name):
	##PIL image to draw in parallel and save
	image1 = Image.new('RGB', (width, height), white)
	draw = ImageDraw.Draw(image1)

	for e in ed:
		start, end = e
		if len(start) > 2:
			start = (start[0], 255)
		if len(end) > 2:
			end = (end[0], 255)
		start = (start[0], start[1])
		end = (end[0], end[1])
		draw.line([start[0],start[1],end[0],end[1]], fill=black)
		#draw.text(((start[0] + end[0])/2 - 2, (start[1] + end[1])/2), 'l', (0,0,0))

	for v in vt:
		if v[1] == -1:
			##put the number of the leaf at (v[0], 5)
			draw.text((v[0]-2, 260), str(v[2]), (0,0,0))

		else:
			##if it's an internal vertex, draw a node
			draw.ellipse(get_bounding_box(v[0], v[1], 3), fill=black)

	filename = folder_name + '/tree_' + str(i) + '.jpg'
	image1.save(filename)

def print_tree_latex(i, vt, ed, heights, folder_name):
	with open('{}/tree_{}.txt'.format(folder_name, i), 'w') as file:

		##want to divide all the numbers by 100 probably -- will that scale???

		file.write('\\begin{minipage}{.333333\\textwidth}\n')
		file.write('\t\\centering\n')
		file.write('\t\\begin{tikzpicture}\n')

		for e in ed:
			start, end = e
			if len(start) > 2:
				start = (start[0], 280)
			if len(end) > 2:
				end = (end[0], 280)
			start = (start[0], start[1])
			end = (end[0], end[1])
			file.write('\t\t\\draw ({},{})--({},{});\n'.format(start[0]/100, -start[1]/100, end[0]/100, -end[1]/100))

		vert_heights = []

		for v in vt:
			if v[1] == -1:
				##put the number of the leaf at (v[0], -2.8)
				file.write('\t\t\\node[below] at ({},-2.8){{${}$}};\n'.format((v[0]-2)/100, str(v[2])))

			else:
				##if it's an internal vertex, draw a circle
				file.write('\t\t\\filldraw ({},{}) circle (1.5pt);\n'.format(v[0]/100, -v[1]/100))
				vert_heights.append(-v[1]/100)

		vert_heights = sorted(list(set(vert_heights)))

		##dashed lines for the heights
		##draw them at the height of the drawn internal vertices
		for j in range(len(vert_heights)):
			v = vert_heights[j]
			m = min(heights)
			file.write('\t\t\\draw[dashed] (-.05,{})--(2.48,{});\n'.format(v,v))
			file.write('\t\t\\node[left] at (-.05,{}){{\\tiny{}}};\n'.format(v,heights[j]-m+1))

		file.write('\t\\end{tikzpicture}\n')
		file.write('\\end{minipage}')

		##close file

def draw_tree(vt, ed, canvas_name):
	##PIL image to draw in parallel and save
	image1 = Image.new('RGB', (width, height), white)
	draw = ImageDraw.Draw(image1)

	for e in ed:
		start, end = e
		if len(start) > 2:
			start = (start[0], 255)
		if len(end) > 2:
			end = (end[0], 255)
		start = (start[0], start[1])
		end = (end[0], end[1])
		canvas_name.create_line(start[0],start[1],end[0],end[1],fill="black")
		# draw.line([start[0],start[1],end[0],end[1]],fill=black)

	for v in vt:
		if v[1] == -1:
			##put the number of the leaf at (v[0], 5)
			canvas_name.create_text(v[0], 265, text=str(v[2]))
			# draw.text(xy=(v[0], 265), text=str(v[2]))
		else:
			##if it's an internal vertex, draw a node
			draw_circle(v[0], v[1], 3, canvas_name)
			# draw.ellipse(get_bounding_box(v[0], v[1], 3), fill=black)

##define print button
def click_print():
	print_trees('example')

##define button clicks
def click_n():
	entered_n = enter_n.get()

	try:

		temp_n = int(float(entered_n))

		if temp_n <= 2:
			print('n must be at least 3!')

		else: ##if n is valid
			n = temp_n
			output_n.delete(0.0, END) ##delete what was in the textbox
			output_n.insert(END, 'n = ' + str(n)) ##write the new n in the textbox

	except ValueError:
		pass

def click_save():
	##save the first and last trees!
	u = line[0]
	v = line[-1]
	
	with open('tree_example.txt', 'w') as f:
		f.write(str(u))
		f.write('\n')
		f.write(str(v))

def click_load():
	load_file = askopenfilename()

	##load the trees as the first and last
	examples = []
	try:
		with open(load_file, 'r') as f:
			s = f.readline()
			while s:
				t = ast.literal_eval(s)
				examples.append(t)
				s = f.readline()

		##set the trees
		u, v = examples
		print(u, v)

		##remove the placeholder
		current = None

	except FileNotFoundError:
		print('No file to load!')

def click_right():
	global left_index, curr_index, right_index

	##if we're already at the end of the line, do nothing
	if right_index >= len(trees) - 1:
		pass

	else:
		##if the left button was disabled, enable it
		if left_index == 0:
			toggle_left(1)

		##increment the indices
		left_index = left_index + 1
		curr_index = curr_index + 1
		right_index = right_index + 1

		##update canvas
		update_canvas()

		##if we're at the end of the line, disable the right button
		if right_index == len(trees) - 1:
			toggle_right(0)

def click_left():
	global left_index, curr_index, right_index

	##if we're already at the start of the line, do nothing
	if left_index == 0:
		pass

	else:
		##if the right button was disabled, enable it
		if right_index == len(trees) - 1:
			toggle_right(1)

		##decrement the indices
		left_index = left_index - 1
		curr_index = curr_index - 1
		right_index = right_index - 1

		##update the canvas
		update_canvas()
		
		##if we're at the start of the line, disable the left button
		if left_index == 0:
			toggle_left(0)

def toggle_left(t):
	pass

def toggle_right(t):
	pass

def update_canvas():
	global tree_canvas_middle, tree_canvas_left, tree_canvas_right
	global curr_index, right_index, left_index, mu

	##delete old canvases
	tree_canvas_middle.delete("all")
	tree_canvas_left.delete("all")
	tree_canvas_right.delete("all")
	output_lambda.delete(0.0, END)

	##generate new clean canvases
	tree_canvas_middle = Canvas(window, width=275, height=275, bg="white")
	tree_canvas_middle.grid(row=4, column=1)

	tree_canvas_left = Canvas(window, width=275, height=275, bg="white")
	tree_canvas_left.grid(row=4, column=0)

	tree_canvas_right = Canvas(window, width=275, height=275, bg="white")
	tree_canvas_right.grid(row=4, column=2)

	##update the trees
	left = trees[left_index]
	curr = trees[curr_index]
	right = trees[right_index]
	mu = mus[curr_index]

	##draw updated trees
	draw_tree(left[0], left[1], tree_canvas_left)
	draw_tree(curr[0], curr[1], tree_canvas_middle)
	draw_tree(right[0], right[1], tree_canvas_right)
	output_lambda.insert(END, str(mu))

##change the title of the window
window.title("Tree Game")

##change the background color, using presets or hex
window.configure(background="white")

##put some words on the screen
Label(window, text='Tree Game', bg="white", fg="black", font="none 24").grid(row=0, column=0)

##text entry box
# enter_n = Entry(window, width=5)
# enter_n.grid(row=1, column=0)

##button to print trees to png
button_print = Button(window, text="print", width=5, bg="white", fg="black", command=click_print)
button_print.grid(row=1,column=0)

##create a button
button_n = Button(window, text="update n", width=8, bg="white", fg="black", command=click_n)
button_n.grid(row=1, column=1)

##keep track of n
output_n = Text(window, width=7, height=1, bg="white", fg='black')
output_n.grid(row=0, column=1)

output_n.insert(END, "n = " + str(n))

##button to save a pair of trees --> later save the whole path?
button_save = Button(window, text="save", width=5, bg="white", fg="black", command=click_save)
button_save.grid(row=1, column=2)

##button to load a pair of trees/path
button_load = Button(window, text="load", width=5, bg="white", fg="black", command=click_load)
button_load.grid(row=0, column=2)

tree_canvas_middle = Canvas(window, width=275, height=275, bg="white")
tree_canvas_middle.grid(row=4, column=1)

tree_canvas_left = Canvas(window, width=275, height=275, bg="white")
tree_canvas_left.grid(row=4, column=0)

tree_canvas_right = Canvas(window, width=275, height=275, bg="white")
tree_canvas_right.grid(row=4, column=2)

button_right = Button(window, text="+", width=2, bg="white", fg="black", command=click_right)
button_right.grid(row=3, column=2)

button_left = Button(window, text="-", width=2, bg="white", fg="black", command=click_left)
button_left.grid(row=3, column=0)

output_lambda = Text(window, width=6, height=1, bg="white", fg="black")
output_lambda.grid(row=3, column=1)
output_lambda.insert(END, str(mu))

##draw a line
# tree_canvas.create_line(0,100,300,100,fill="black")
# tree_canvas.create_line(150,0,150,200,fill="black")
# tree_canvas.create_rectangle(50, 150, 250, 50, fill="pink")
# draw_circle(150,100,10,tree_canvas,f="red")

##draw a tree
draw_tree(left[0], left[1], tree_canvas_left)
draw_tree(curr[0], curr[1], tree_canvas_middle)
draw_tree(right[0], right[1], tree_canvas_right)

window.mainloop()