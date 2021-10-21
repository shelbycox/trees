from tkinter import *

window = Tk()

##define button clicks
def click_n():
	entered_n = enter_n.get()
	output_n.delete(0.0, END)
	output_n.insert(END, 'n = ' + entered_n)

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
button_n = Button(window, text="update", width=6, bg="white", fg="black", command=click_n)
button_n.grid(row=1, column=1)

##keep track of n
output_n = Text(window, width=6, height=1, bg="white", fg='black')
output_n.grid(row=0, column=1)

window.mainloop()