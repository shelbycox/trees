from tkinter import *
from tkinter.filedialog import askopenfilename
import ast
import drawTreeTk as dt
import tropicalLines as tl

window = Tk()

n = 5
line = [0,1]
u = {(1, 2): 40, (2, 1): 40, (1, 3): 40, (3, 1): 40, (1, 4): 40, (4, 1): 40, (1, 5): 40, (5, 1): 40, (2, 3): 30, (3, 2): 30, (2, 4): 30, (4, 2): 30, (2, 5): 30, (5, 2): 30, (3, 4): 20, (4, 3): 20, (3, 5): 20, (5, 3): 20, (4, 5): 10, (5, 4): 10}
v = {(1, 2): 1, (2, 1): 1, (1, 3): 2, (3, 1): 2, (1, 4): 3, (4, 1): 3, (1, 5): 4, (5, 1): 4, (2, 3): 2, (3, 2): 2, (2, 4): 3, (4, 2): 3, (2, 5): 4, (5, 2): 4, (3, 4): 3, (4, 3): 3, (3, 5): 4, (5, 3): 4, (4, 5): 4, (5, 4): 4}

line = tl.normalize_heights(tl.get_line_int(u,v), 2)

trees = [dt.rec_vertices(T, 275/2, tl.rec_tree_paren(T, [i+1 for i in range(5)]), 275/2, None, [], []) for T in line]

left = trees[0]
curr = trees[1]
right = trees[2]

# u_info = dt.rec_vertices(u, 275/2, tl.rec_tree_paren(u, [i+1 for i in range(5)]), 275/2, None, [], [])

def draw_circle(x,y,r, canvas_name, f="black"):
	x0 = x - r
	x1 = x + r
	y0 = y - r
	y1 = y + r
	return canvas_name.create_oval(x0,y0,x1,y1,fill=f)

def draw_tree(vt, ed, canvas_name):
	for e in ed:
		start, end = e
		if len(start) > 2:
			start = (start[0], 255)
		if len(end) > 2:
			end = (end[0], 255)
		start = (start[0], start[1])
		end = (end[0], end[1])
		canvas_name.create_line(start[0],start[1],end[0],end[1],fill="black")

	for v in vt:
		if v[1] == -1:
			##put the number of the leaf at (v[0], 5)
			canvas_name.create_text(v[0], 265, text=str(v[2]))
		else:
			##if it's an internal vertex, draw a node
			draw_circle(v[0], v[1], 3, canvas_name)

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

##change the title of the window
window.title("Tree Game")

##change the background color, using presets or hex
window.configure(background="white")

##put some words on the screen
Label(window, text='Tree Game', bg="white", fg="black", font="none 24").grid(row=0, column=0)

##text entry box
enter_n = Entry(window, width=5)
enter_n.grid(row=1, column=0)

##create a button
button_n = Button(window, text="update n", width=8, bg="white", fg="black", command=click_n)
button_n.grid(row=1, column=1)

##keep track of n
output_n = Text(window, width=7, height=1, bg="white", fg='black')
output_n.grid(row=0, column=1)

output_n.insert(END, "n = " + str(n))

##button to save a pair of trees --> later save the whole path?
button_save = Button(window, text="save", width=5, bg="white", fg="black", command=click_save)
button_save.grid(row=3, column=1)

##button to load a pair of trees/path
button_load = Button(window, text="load", width=5, bg="white", fg="black", command=click_load)
button_load.grid(row=2, column=1)

tree_canvas_middle = Canvas(window, width=275, height=275, bg="white")
tree_canvas_middle.grid(row=4, column=1)

tree_canvas_left = Canvas(window, width=275, height=275, bg="white")
tree_canvas_left.grid(row=4, column=0)

tree_canvas_right = Canvas(window, width=275, height=275, bg="white")
tree_canvas_right.grid(row=4, column=2)

##draw a line
# tree_canvas.create_line(0,100,300,100,fill="black")
# tree_canvas.create_line(150,0,150,200,fill="black")
# tree_canvas.create_rectangle(50, 150, 250, 50, fill="pink")
# draw_circle(150,100,10,tree_canvas,f="red")

##draw a tree
draw_tree(left[0], left[1], tree_canvas_left)
draw_tree(curr[0], curr[1], tree_canvas_middle)
draw_tree(curr[0], curr[1], tree_canvas_right)

window.mainloop()