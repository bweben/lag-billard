from tkinter import *


class Wall:
    from_point = None
    to_point = None

    def __init__(self, from_point, to_point):
        self.from_point = from_point
        self.to_point = to_point


class Point:
    x = 0
    y = 0

    def __init__(self, dict):
        self.x = dict["x"]
        self.y = dict["y"]


class Billard(Canvas):
    walls = list()

    temp_point = None

    def left_click(self, event):
        print("left click at", event.x, event.y)
        print(event)

        if self.temp_point is None:
            self.temp_point = Point({"x": event.x, "y": event.y})
        else:
            self.add_wall(self.temp_point, Point({"x": event.x, "y": event.y}))

    def right_click(self, event):
        print("right click at", event.x, event.y)
        print(event)

    def add_wall(self, from_point, to_point):
        wall = Wall(from_point, to_point)
        self.temp_point = None
        self.walls.append(wall)
        self.draw_wall(wall)

    def draw_wall(self, wall):
        self.create_line(wall.from_point.x, wall.from_point.y, wall.to_point.x, wall.to_point.y)
        self.pack()

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.bind("<Button-1>", self.left_click)
        self.bind("<Button-3>", self.right_click)

        self.add_wall(Point({"x": 0, "y": 0}), Point({"x": self.winfo_width(), "y": 0}))
        self.add_wall(Point({"x": self.winfo_width(), "y": 0}),
                      Point({"x": self.winfo_width(), "y": self.winfo_height()}))
        self.add_wall(Point({"x": self.winfo_width(), "y": self.winfo_height()}),
                      Point({"x": 0, "y": self.winfo_height()}))
        self.add_wall(Point({"x": 0, "y": self.winfo_height()}), Point({"x": 0, "y": 0}))

        self.create_oval(20, 20, 30, 30)

        self.pack()


root = Tk()
root.geometry("500x500")
app = Billard(master=root, width=500, height=500)
app.mainloop()
