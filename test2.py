from graphics import *
from graphics_extras import *

win = GraphWin("Test", 500, 500)
win.setBackground("white")

for i in range(255):
    r = Rectangle(Point(i, 0), Point(i + 1, 200))
    r.setFill(color_rgb(i, i, i))
    r.setOutline(color_rgb(i, i, i))
    r.draw(win)

s = Slider(Point(250, 250), 300, 10)
s.draw(win)


def drag(event):
    pt = Point(event.x, event.y)
    if s.inside_knob(pt):
        s.move_knob(event.x, win)
        win.master.attributes("-alpha", s.value)


win.bind("<B1-Motion>", drag)

win.mainloop()
