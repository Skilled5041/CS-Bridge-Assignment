from graphics import *

win = GraphWin("drag", 500, 500)
point1 = Point(250, 250)
point1.draw(win)


def motion(event):
    x1, y1 = event.x, event.y
    point1 = Point(x1, y1)
    point1.setFill("red")
    point1.draw(win)


win.bind('<B1-Motion>', motion)
win.mainloop()
