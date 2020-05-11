from tkinter import *


class Application(Canvas):
    def leftclick(self, event):
        print("left click at", event.x, event.y)
        print(event)

    def rightclick(self, event):
        print("right click at", event.x, event.y)
        print(event)

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.bind("<Button-1>", self.leftclick)
        self.bind("<Button-3>", self.rightclick)
        self.pack()


root = Tk()
root.geometry("500x500")
app = Application(master=root)
app.mainloop()
