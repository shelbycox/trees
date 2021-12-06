import matplotlib.pyplot as plt
import re
import ast as ast
import math

with open('my_data.txt', 'r') as the_file:
	data = ast.literal_eval(the_file.readline())

fig, ax = plt.subplots()
ax.plot([data[i][0] for i in range(len(data))], [math.log((data[i][1])) for i in range(len(data))])
plt.show()