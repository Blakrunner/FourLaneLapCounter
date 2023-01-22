''' 
    Four lane lap counter and lap timer
    
    Shapes for use in Four Lane Lap Counter and Lap Timer 
    
'''
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen

class Shape():
    ''' A base class for creating different shapes '''
    def __init__(self, width, height, position, color, pensize=4, angle=10, anglelength=20):
        self.pensize = pensize
        self.anglelenght = anglelength
        self.angle = angle
        self.color = color
        self.position = position
        self.height = height
        self.width = width

    def paint(self, painter):
        ''' we pass this on to shape paint '''
        pass

class Circle(Shape):
    ''' Circle class with Shape as base to draw circles '''
    def paint(self, painter):
        if not painter.isActive():
            return
        painter.save()
        painter.setPen(QPen(self.color,  self.pensize , Qt.SolidLine))
        x, y = self.position.x(), self.position.y()
        painter.drawEllipse(x, y, self.height, self.height)
        painter.restore()

class Line(Shape):
    ''' Line class with Shape as base to draw lines '''
    def paint(self, painter):
        if not painter.isActive():
            return
        painter.save()
        painter.setPen(QPen(self.color, self.pensize, Qt.SolidLine))
        x, y = self.position.x(), self.position.y()
        painter.drawLine(x, y, self.width, self.height)
        painter.restore()

class Pie(Shape):
    ''' Pie class with Shape as base to draw pies '''
    def paint(self, painter):
        if not painter.isActive():
            return
        painter.save()
        painter.setPen(QPen(self.color, self.pensize, Qt.SolidLine))
        x, y = self.position.x(), self.position.y()
        painter.drawPie(x, y, self.width, self.height, self.angle, self.anglelenght)
        painter.restore()

class Rectangle(Shape):
    ''' Rectangle class with Shape as base to draw rectangles '''
    def paint(self, painter):
        if not painter.isActive():
            return
        painter.save()
        painter.setPen(QPen(self.color, self.pensize, Qt.SolidLine))
        x_pos, y_pos = self.position.x(), self.position.y()
        painter.drawRect(x_pos, y_pos, self.width, self.height)
        painter.restore()
