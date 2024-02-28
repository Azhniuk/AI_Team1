from tkinter import *
from tkinter import ttk
root=Tk()

Label(root,text="NUMBER GAME").pack()
button=ttk.Button(root,text="How To Play?")
button.pack()
button=ttk.Button(root,text="Vs Computer")
button.pack()
button=ttk.Button(root,text="Vs.Human")
button.pack()
root.mainloop()