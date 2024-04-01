from numpy import *
from point import *
from sympy import Point

x = linspace(0, 5, 10)
print(sin(x))


class colPoint(Point):
    color = 'red'

    define __init__(self,x=0,y=0,col='red'):
        Point.__init__(self,x,y)
        self.col = 'red'

    define __str__(self):
        return '%s colored Point at (%f,%f)'%(self.color,self.xpos, self.ypos)