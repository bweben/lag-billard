import numpy
import time
from tkinter import *


def check_collision(s):
    return 1 >= s > 0


def collide(point, vector, wall):
    A = wall.from_point
    B = wall.to_point
    v = vector
    P = point

    equation = numpy.array([
        [B.x - A.x, -v["x"]],
        [B.y - A.y, -v["y"]]
    ])

    solution = numpy.array([
        P.x - A.x,
        P.y - A.y
    ])

    solved = numpy.linalg.solve(equation, solution)
    t = solved[0]
    s = solved[1]

    # t can be used to check how far apart P and the collision are

    S = numpy.array([P.x, P.y]) + s * numpy.array([v["x"], v["y"]])

    return {"point": Point({"x": S[0], "y": S[1]}), "s": s, "t": t}


def calculate_direction_vector(point_a, point_b):
    direction = point_b - point_a
    return numpy.linalg.norm(direction, ord=1)


def compute_reflection(A, B, S, P):
    g = [B["x"] - A["x"], B["y"] - A["y"]]
    t = 0  # ???
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
        return Point({
            'x': self.x - point.x,
            'y': self.y - point.y,
        })

    def add(self, point):
        self.x = self.x + point.x
        self.y = self.y + point.y

    def multiply(self, point):
        self.x = self.x * point.x
        self.y = self.y * point.y

    def factor(self):
        return self.y / self.x

    def print(self, msg=""):
        print("Point ", msg, " ( x = ", self.x, " ,y = ", self.y, " )")

    def minimalVector(self):
        x = abs(self.x) / self.x
        y = self.y / abs(self.x)

        return Point({
            "x": x,
            "y": y
        })

class Billard(Canvas):
    walls = list()

    ball_point = None
    temp_point = None

    current_position = None
    current_direction = None

    ball = None

    ball_radius = 5

    move_locker = False

    def left_click(self, event):
        print("left click at", event.x, event.y)
        print(event)

        if self.temp_point is None:
            self.temp_point = Point({"x": event.x, "y": event.y})
        else:
            self.add_wall(self.temp_point, Point({"x": event.x, "y": event.y}))

    def cutpoint(self, a1, a2, b1, b2):

        delta_a = a2.sub(a1)

        if delta_a.x == 0:
            return delta_a

        m_a = delta_a.y / delta_a.x
        c_a = a1.y - a1.x * m_a

        delta_b = b2.sub(b1)

        if delta_b.x == 0:
            return delta_b

        m_b = delta_b.y / delta_b.x
        c_b = b1.y - b1.x * m_b

        x = (c_b - c_a) / (m_a - m_b)

        result = Point({
            'x': x,
            'y': x * m_b + c_b
        })
        # self.create_oval(result.x - 5, result.y - 5, result.x + 5, result.y + 5)

        return result

    def mirrorpoint(self, a1, a2, p):

        delta_a = a2.sub(a1)

        m_a = delta_a.y / delta_a.x
        c_a = a1.y - a1.x * m_a

        m_a_mir = (-1 / m_a)
        c_a_mir = p.y - a1.x * m_a_mir

        cut_x = (c_a_mir - c_a) / (m_a - m_a_mir)

        mir_x = ((2*cut_x) + p.x)
        mir_y = mir_x * m_a_mir + c_a_mir

        self.create_oval(mir_x - 5, mir_y - 5, mir_x + 5, mir_y + 5)
        self.create_oval(p.x - 5, p.y - 5, p.x + 5, p.y + 5)
        self.create_line(p.x, p.y, mir_x, mir_y)

        return Point({
            "x": mir_x,
            "y": mir_y
        })

    def movingVector(self, p1, p2):
        v_res = p1.sub(p2)
        return v_res.minimalVector()



    def right_click(self, event):
        print("right click at", event.x, event.y)
        print(event)

        if (not self.move_locker):
            self.move_locker = True
            self.move_ball(Point({"x": event.x, "y": event.y}))

    def is_n_beween(self, n, p1, p2):
        return (n <= p1 and n >= p2) or (n >= p1 and n <= p2)

    def isBetweenPoints(self, p, p_from, p_to):
        return self.is_n_beween(p.x, p_from.x, p_to.x) and self.is_n_beween(p.y, p_from.y, p_to.y)

    def nearestWall(self, point, vector):
        cutpoints = list()

        print("--------------nearest wall-----------------")
        for wall in self.walls:
            cut = self.cutpoint(wall.from_point, wall.to_point, vector, point)
            wall.from_point.print()
            wall.to_point.print()
            cut.print("cut")
            self.ball_point.print("ballpoint")
            if self.isBetweenPoints(cut, wall.from_point, wall.to_point):
                cut.print("2")

                if point.x > 0 and point.y > 0:
                    if cut.x > vector.x and cut.y > vector.y:
                        cutpoints.append({"cut": cut, "wall": wall})
                        cut.print("cut 1 1")

                if point.x < 0 and point.y < 0:
                    if cut.x < vector.x and cut.y < vector.y:
                        cutpoints.append({"cut": cut, "wall": wall})
                        cut.print("cut -1 1")

                if point.x > 0 and point.y < 0:
                    if cut.x > vector.x and cut.y < vector.y:
                        cutpoints.append({"cut": cut, "wall": wall})
                        cut.print("cut 1 -1")

                if point.x < 0 and point.y > 0:
                    if cut.x < vector.x and cut.y > vector.y:
                        cutpoints.append({"cut": cut, "wall": wall})
                        cut.print("cut -1 -1")

        cutpoints.sort(key=lambda x: x['cut'].x, reverse=False)
        return cutpoints[0]['wall']

    def move_ball(self, point):
        print("------------move_ball------------------")
        # wall = self.walls[4]

        startpoint = Point({'x': 5, 'y': 5})

        # for i in numpy.arange(0,2,1):
        v_mov = point.sub(startpoint).minimalVector()


        while True:
            wall = self.nearestWall(point, startpoint)

            cutpoint = self.cutpoint(wall.from_point, wall.to_point, self.ball_point, point)

            for i in numpy.arange(0, cutpoint.x - (2 * self.ball_radius), 1):
                self.draw_ball(v_mov)

            mir = self.mirrorpoint(wall.from_point, wall.to_point, startpoint)
            v_mov = self.movingVector(cutpoint, mir)

            self.create_line(cutpoint.x, cutpoint.y, mir.x, mir.y)




        print("------------end move_ball------------------")

        # todo: calculate collision and new course
        # self.draw_ball(Point({'x': x, 'y': y}))

    def draw_ball(self, point):
        self.ball_point = point

        if self.ball is not None:

            time.sleep(0.01)
            self.move(self.ball, point.x, point.y)
            self.update()
        else:
            self.ball = self.create_oval(point.x - self.ball_radius, point.y -
                                         self.ball_radius, point.x + self.ball_radius, point.y + self.ball_radius)
            self.pack()

    def add_wall(self, from_point, to_point):
        wall = Wall(from_point, to_point)
        self.temp_point = None
        self.walls.append(wall)
        self.draw_wall(wall)

    def draw_wall(self, wall):
        self.create_line(wall.from_point.x, wall.from_point.y,
                         wall.to_point.x, wall.to_point.y)
        self.pack()

    def __init__(self, master=None, **kw):

        window_with = 500
        window_heigth = 500

        super().__init__(master, **kw)
        self.bind("<Button-1>", self.left_click)
        self.bind("<Button-3>", self.right_click)

        self.add_wall(Point({"x": 0, "y": 0}), Point({"x": window_with, "y": 0}))
        self.add_wall(Point({"x": window_with, "y": 0}),
                      Point({"x": window_with, "y": window_heigth}))
        self.add_wall(Point({"x": window_with, "y": window_heigth}),
                      Point({"x": 0, "y": window_heigth}))
        self.add_wall(
            Point({"x": 0, "y": window_heigth}), Point({"x": 0, "y": 0}))

        self.draw_ball(Point({"x": 5, "y": 5}))


root = Tk()
root.geometry("500x500")
app = Billard(master=root, width=500, height=500)
app.mainloop()
