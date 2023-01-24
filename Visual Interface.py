import tkinter as tk
import numpy as np
from random import randint
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

path = r'C:\Users\lopezb41\OneDrive - imec\Documents\Experiments\Data\Electrochemical\LSB_09\test.txt'
col = ['Capacity (mAh/cm$^3$)', 'Cycle', 'Sample']
df = pd.read_csv(path)
print(df)

# root = tk.Tk()
# root.wm_title('Rodrigo Lopez')
# lab = tk.Label(root)
# lab.pack()

fig, ax = plt.subplots(dpi = 100) # facecolor = 'white'
sns.scatterplot(data = df, x = col[1], y = col[0], hue = col[2], style = col[2], s = 150)
# sns.move_legend(ax, "lower center", ncol = 2, bbox_to_anchor=(0.5, 1), frameon = False, title = None)

# button_quit = tk.Button(master=root, text="Quit", command=root.destroy)
# button_save = tk.Button(master=root, text="Save", command=root.destroy)
# button_quit.pack(side=tk.BOTTOM)
# button_save.pack(side=tk.BOTTOM)


# canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
# canvas.draw()
# canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
# root.mainloop()




# root.after(1000, update) # run itself again after 1000 ms   
# update()
