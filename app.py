from tkinter import *
import time
import numpy



def has_collision(point, vector, wall):
    P = point
    v = vector
    A = wall.from_point
    B = wall.to_point
    t = 0 # ???
    s = 0 # ???

    Sx = A["x"] + t * (B["x"] - A["x"]) - (P["x"] + s * v["x"])
    Sy = A["y"] + t * (B["y"] - A["y"]) - (P["y"] + s * v["y"])

    S = Point({"x": Sx, "y": Sy})
    # check if point S is between point A to B

def compute_reflection(A, B, S, P):
    g = [B["x"] - A["x"], B["y"] - A["y"]]
    t = 0 # ???
    g3 = P + t * [g[0], -g[1]]

    # X calculate with g = g3

    # P' calculate

    # calculate P' to S to calculate new vector


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


    def mirror(self, point, wall):
        print(wall)
        print(point)


    def left_click(self, event):
        print("left click at", event.x, event.y)
        print(event)

        if self.temp_point is None:
            self.temp_point = Point({"x": event.x, "y": event.y})
        else:
            self.add_wall(self.temp_point, Point({"x": event.x, "y": event.y}))


        

    def cutpoint(self, a, b):
        m_a  = a.x / a.y
        c_a = a.y - a.x * m_a

        m_b  = b.x / b.y
        c_b = b.y - b.x * m_b

        x = (m_b - m_a)/(c_b - c_a)

        return Point({
            'x': x,
            'y': x * m_a + c_a,
        })




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


            m = point.factor()
            cutpoint()


            # todo we have to define how many steps we want to loop througth
            # a possible solution can be the diagonal length of the screen -> the ball will never run longer than that for one line
            for i in  numpy.arange(0, 1000, 0.5):

                x = i
                y = i * m

                print("( i = ",i, " n = ",n," x = ", x ," y = ", y,")")

                # todo: calculate collision and new course
                self.draw_ball(Point({'x': x, 'y':y }))


    def draw_ball(self, point):
        self.ball_point = point


        if self.ball is not None:
            time.sleep(0.2)
            self.move(self.ball, point.x, point.y)
            self.update()
        else:
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
