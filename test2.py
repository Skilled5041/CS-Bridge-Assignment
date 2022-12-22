from graphics import *
from graphics_extras import *


def on_click(event):
    pt = Point(event.x, event.y)
    if check.inside(pt):
        check.toggle()


win = GraphWin("Test", 500, 500)
win.bind("<Button-1>", on_click)

check = Checkbox(Point(100, 100), Point(200, 200))
check.set_checked_colour("green")
check.set_unchecked_colour("red")
check.draw(win)

win.mainloop()
