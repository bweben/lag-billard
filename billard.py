from tkinter import Canvas
from tkinter.tix import Tk
import numpy
import time


class Wall:
    from_point = None
    to_point = None

    def __init__(self, from_point, to_point):
        self.from_point = from_point
        self.to_point = to_point

class Calculation:
    @staticmethod
    def check_collision(s):
        return 1 >= s > 0

    @staticmethod
    def collide(point, vector, wall):
        A = wall.from_point
        B = wall.to_point
        v = vector
        P = point

        equation = numpy.array([
            [B[0] - A[0], -v[0]],
            [B[1] - A[1], -v[1]]
        ])

        solution = numpy.array([
            P[0] - A[0],
            P[1] - A[1]
        ])

        solved = numpy.linalg.solve(equation, solution)
        t = solved[0]
        s = solved[1]

        # t can be used to check how far apart P and the collision are

        S = numpy.array([P[0], P[1]]) + s * numpy.array([v[0], v[1]])

        return {"point": S, "s": s, "t": t}


    @staticmethod
    def mirror(point_p, point_s):
        P = numpy.array([point_p[0], point_p[1]])
        S = numpy.array([point_s[0], point_s[1]])

        equation = numpy.array([
            [point_s[0], -point_s[0]],
            [-point_s[1], -point_s[1]]
        ])

        solution = numpy.array([-point_p[0], -point_p[1]])

        t = numpy.linalg.solve(equation, solution)[1]

        X = t * S

        # is the mirrored from where we have to draw a line through S to get to the new vector
        return P + (2 * (X - P))

    @staticmethod
    def calculate_direction_vector(point_a, point_b):
        direction = point_b - point_a
        return numpy.linalg.norm(direction, ord=1)


class Billard:
    walls = list()
    running = True
    app = None
    current_position = None
    current_direction = None
    ball = None

    def __init__(self, width, height, app):
        self.app = app

        self.add_wall(numpy.array([0, 0]), numpy.array([width, 0]))
        self.add_wall(numpy.array([width, 0]),
                      numpy.array([width, height]))
        self.add_wall(numpy.array([width, height]),
                      numpy.array([0, height]))
        self.add_wall(numpy.array([0, height]), numpy.array([0, 0]))

        self.ball = self.app.create_oval(0, 0, 5, 5)

        self.set_position(numpy.array([5, 5]))

    def add_wall(self, from_point, to_point):
        wall = Wall(from_point, to_point)
        self.walls.append(wall)
        self.draw_wall(wall)

    def set_position(self, point):
        self.current_position = point
        self.app.move(self.ball, point[0], point[1])
        self.app.update()

    def set_direction(self, direction):
        self.current_direction = direction

    def draw_wall(self, wall):
        self.app.create_line(wall.from_point[0], wall.from_point[1], wall.to_point[0], wall.to_point[1])
        self.app.pack()

    def start(self):
        while self.running:
            time.sleep(0.2)
            if self.current_direction is not None:
                nearest_wall = None
                nearest = None
                nearest_result = None

                for wall in self.walls:
                    result = Calculation.collide(self.current_position, self.current_direction, wall)

                    if Calculation.check_collision(result["s"]) and nearest is not None and nearest >= result["t"]:
                        nearest = result["t"]
                        nearest_wall = wall
                        nearest_result = result

                if nearest_wall is not None:
                    mirror_result = Calculation.mirror(self.current_position, nearest_result["point"])

                    if nearest <= 1:
                        self.set_direction(Calculation.calculate_direction_vector(self.current_position, mirror_result))

                self.set_position(self.current_position + self.current_direction)

class App(Canvas):
    billard = None
    temp_point = None

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.bind("<Button-1>", self.left_click)
        self.bind("<Button-3>", self.right_click)

        self.billard = Billard(self.winfo_width(), self.winfo_height(), self)

    def start(self):
        self.billard.start()

    def left_click(self, event):
        if self.temp_point is None:
            self.temp_point = numpy.array([event.x, event.y])
        else:
            self.billard.add_wall(self.temp_point, numpy.array([event.x, event.y]))
            self.temp_point = None

    def right_click(self, event):
        self.billard.set_direction(numpy.array([event.x, event.y]))
        self.start()


root = Tk()
root.geometry("500x500")
app = App(master=root, width=500, height=500)
app.mainloop()
