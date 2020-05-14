from tkinter import *
import time
import numpy


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

    def setCoordinates(self, x, y):
        self.x = x
        self.y = y
    
    def sub(self, point):
        self.x = self.x - point.x
        self.y = self.y - point.y
    
    def add(self, point):
        self.x = self.x + point.x
        self.y = self.y + point.y
    
    def multiply(self, point):
        self.x = self.x * point.x
        self.y = self.y * point.y

    def factor(self):
        return self.y / self.x
    
    def print(self):
        print("Point ( x = ", self.x, " ,y = ", self.y  ," )")


class Billard(Canvas):
    walls = list()

    ball_point = None
    temp_point = None
    ball = None

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
        self.move_ball(Point({"x": event.x, "y": event.y}))


    def move_ball(self, point, instant=False):
        if instant:
            self.draw_ball(point)
        else:

            point.sub(self.ball_point)
            point.sub(self.ball_point)

            n = point.factor()

            
            for i in  numpy.arange(0, 1000, 0.2):
                print()

                x = i
                y = i * n



                print("( i = ",i, " n = ",n," x = ", x ," y = ", y,")")

                self.draw_ball(Point({'x': x, 'y':y }))

                
            

#            while int(point.x) != int(self.ball_point.x) or int(point.y) != int(self.ball_point.y):
#                step += 1
#                print(point.x, point.y)
#                print(self.ball_point.x, self.ball_point.y)
#                # todo: calculate collision and new course
#                self.draw_ball(Point({"x": self.ball_point.x + x_step, "y": self.ball_point.y + y_step}))
#
#            # self.draw_ball(Point({"x": int(point.x), "y": int(point.y)}))


    def draw_ball(self, point):
        self.ball_point = point


        if self.ball is not None:
            
            self.move(self.ball, point.x, point.y)
            time.sleep(0.2)
            self.update()
        else:
            print("--------------------------------------------------")
            self.ball = self.create_oval(point.x - 5, point.y - 5, point.x + 5, point.y + 5)
            self.pack()

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

        self.move_ball(Point({"x": 5, "y": 5}), True)


root = Tk()
root.geometry("500x500")
app = Billard(master=root, width=500, height=500)
app.mainloop()
