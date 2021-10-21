from tkinter import *
from tkinter.filedialog import askopenfilename
import ast

window = Tk()

n = 0
line = [0,1]
u = 0
v = 1

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

##button to save a pair of trees --> later save the whole path?
button_save = Button(window, text="save", width=5, bg="white", fg="black", command=click_save)
button_save.grid(row=3, column=1)

##button to load a pair of trees/path
button_load = Button(window, text="load", width=5, bg="white", fg="black", command=click_load)
button_load.grid(row=2, column=1)

window.mainloop()