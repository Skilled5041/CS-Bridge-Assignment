from graphics import *


class Button:
    def __init__(self, p1: Point, p2: Point, label: str):
        self.body = Rectangle(p1, p2)
        self.label = Text(Point((p1.getX() + p2.getX()) / 2, (p1.getY() + p2.getY()) / 2), label)
        self.enabled = True

    def draw(self, window: GraphWin):
        self.body.draw(window)
        self.label.draw(window)
        window.items.append(self)

    def undraw(self, window: GraphWin):
        self.body.undraw()
        self.label.undraw()
        window.items.remove(self)

    def inside(self, click: Point) -> bool:
        p1x = min(self.body.getP1().getX(), self.body.getP2().getX())
        p1y = min(self.body.getP1().getY(), self.body.getP2().getY())
        p2x = max(self.body.getP1().getX(), self.body.getP2().getX())
        p2y = max(self.body.getP1().getY(), self.body.getP2().getY())
        return p1x < click.getX() < p2x and p1y < click.getY() < p2y


class Slider:
    def __init__(self, center: Point, length: int, thickness: int):
        self.track = Rectangle(Point(center.getX() - length / 2, center.getY() - thickness / 2),
                               Point(center.getX() + length / 2, center.getY() + thickness / 2))
        self.track.setFill(color_rgb(156, 156, 156))
        self.track.setOutline(color_rgb(156, 156, 156))

        self.round_l = Circle(Point(center.getX() - length / 2, center.getY()), thickness / 2)
        self.round_l.setFill(color_rgb(0, 0, 0))
        self.round_l.setOutline(color_rgb(0, 0, 0))

        self.round_r = Circle(Point(center.getX() + length / 2, center.getY()), thickness / 2)
        self.round_r.setFill(color_rgb(156, 156, 156))
        self.round_r.setOutline(color_rgb(156, 156, 156))

        self.knob = Circle(Point(center.getX(), center.getY()), thickness)
        self.knob.setFill(color_rgb(0, 0, 0))
        self.knob.setOutline(color_rgb(0, 0, 0))

        self.track_top = Rectangle(Point(center.getX() - length / 2, center.getY() - thickness / 2),
                                   Point(self.knob.getCenter().getX(), center.getY() + thickness / 2))
        self.track_top.setFill(color_rgb(0, 0, 0))
        self.track_top.setOutline(color_rgb(0, 0, 0))

        self.value = 0

    def draw(self, window: GraphWin):
        self.track.draw(window)
        self.round_l.draw(window)
        self.round_r.draw(window)
        self.knob.draw(window)
        self.track_top.draw(window)
        window.items.append(self)

    def undraw(self, window: GraphWin):
        self.track.undraw()
        self.round_l.undraw()
        self.round_r.undraw()
        self.knob.undraw()
        self.track_top.undraw()
        window.items.remove(self)

    def set_track_color(self, color: color_rgb):
        self.track.setFill(color)
        self.track.setOutline(color)
        self.round_r.setFill(color)
        self.round_r.setOutline(color)

    def set_knob_color(self, color: color_rgb):
        self.knob.setFill(color)
        self.knob.setOutline(color)
        self.track_top.setFill(color)
        self.track_top.setOutline(color)
        self.round_l.setFill(color)
        self.round_l.setOutline(color)

    def inside_knob(self, click: Point) -> bool:
        return self.knob.getCenter().getX() - self.knob.getRadius() < click.getX() < self.knob.getCenter().getX() + \
            self.knob.getRadius() and \
            self.knob.getCenter().getY() - self.knob.getRadius() < click.getY() < self.knob.getCenter().getY() + \
            self.knob.getRadius()

    def move_knob(self, x_pos, window: GraphWin):
        if self.round_l.getCenter().getX() < x_pos < self.round_r.getCenter().getX():
            self.knob.move(x_pos - self.knob.getCenter().getX(), 0)

            window.coords(self.track_top.id, self.track_top.getP1().getX(), self.track_top.getP1().getY(), x_pos,
                          self.track_top.getP2().getY())

            self.value = (self.knob.getCenter().getX() - self.track.getP1().getX()) / \
                         (self.track.getP2().getX() - self.track.getP1().getX())


class Checkbox:
    def __init__(self, p1: Point, p2: Point):
        self.box = Rectangle(p1, p2)
        self.checked_colour = color_rgb(0, 0, 0)
        self.unchecked_colour = color_rgb(156, 156, 156)
        self.box.setFill(self.unchecked_colour)
        self.box.setOutline(self.unchecked_colour)
        self.checked = False

    def draw(self, window: GraphWin):
        self.box.draw(window)
        window.items.append(self)

    def undraw(self, window: GraphWin):
        self.box.undraw()
        window.items.remove(self)

    def inside(self, click: Point) -> bool:
        p1x = min(self.box.getP1().getX(), self.box.getP2().getX())
        p1y = min(self.box.getP1().getY(), self.box.getP2().getY())
        p2x = max(self.box.getP1().getX(), self.box.getP2().getX())
        p2y = max(self.box.getP1().getY(), self.box.getP2().getY())
        return p1x < click.getX() < p2x and p1y < click.getY() < p2y

    def set_unchecked_colour(self, color: color_rgb):
        self.unchecked_colour = color
        if not self.checked:
            self.box.setFill(color)
            self.box.setOutline(color)

    def set_checked_colour(self, color: color_rgb):
        self.checked_colour = color
        if self.checked:
            self.box.setFill(color)
            self.box.setOutline(color)

    def toggle(self):
        if self.checked:
            self.box.setFill(self.unchecked_colour)
            self.box.setOutline(self.unchecked_colour)
            self.checked = False
        else:
            self.box.setFill(self.checked_colour)
            self.box.setOutline(self.checked_colour)
            self.checked = True
