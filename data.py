L = [(5, 0.73), (6, 0.7166666666666667), (7, 0.5904761904761905), (8, 0.6017857142857144), (9, 0.5277777777777778), (10, 0.518888888888889), (11, 0.4890909090909091), (12, 0.4787878787878788), (13, 0.45), (14, 0.4483516483516483), (15, 0.4157142857142857), (16, 0.405), (17, 0.3669117647058823), (18, 0.37254901960784315), (19, 0.362280701754386), (20, 0.36289473684210527), (21, 0.34547619047619044), (22, 0.33722943722943727), (23, 0.32055335968379445), (24, 0.327536231884058), (25, 0.304), (26, 0.28338461538461535), (27, 0.2873219373219373), (28, 0.28465608465608466), (29, 0.27992610837438425), (30, 0.2771264367816092), (31, 0.25763440860215053), (32, 0.2555443548387097), (33, 0.25018939393939393), (34, 0.23288770053475938), (35, 0.2402521008403361), (36, 0.2400793650793651), (37, 0.2361861861861862), (38, 0.22773826458036983), (39, 0.23542510121457488)]

import matplotlib.pyplot as plt
import math

fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot([L[i][0] for i in range(len(L))], [L[i][1] for i in range(len(L))])  # Plot some data on the axes.
plt.show()