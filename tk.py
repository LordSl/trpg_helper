from tkinter import *
from PIL import Image,ImageTk

width=260
height=400

root = Tk()
root.attributes('-alpha',0.75)
img = ImageTk.PhotoImage(Image.open('img/bg.png').resize((width,height)))
l = Label(root,image=img)
l.grid()
Label(root,text='hi baby').grid(row=0,column=0)
root.mainloop()