# Default Modules
from typing import Tuple

class Coordinate():
    ''' Simple Coordinate class'''

    def __init__(self, x: int, y: int) -> None:
        '''Defines x and y variables'''
        self.X = x
        self.Y = y

    def getTuple(self) -> Tuple[int, int]:
        '''
        Transforms Coordinate into a tupe of x: [0] y: [1]

        :return: coordinate in tuple format
        :rtype: Tuple[int, int]
        '''        
        return (self.X, self.Y)

    def __str__(self) -> str:
        return f"X: {self.X}, Y: {self.Y}"

    def __add__(self, __o : object):
        ''' Override Coordinate addition. Adds the x and y positions of both objects and returns the result coordinate'''
        x = self.X + __o.X
        y = self.Y + __o.Y
        return Coordinate(x,y)

    def __sub__(self, __o : object):
        ''' Override Coordinate subtraction. Subtracts the x and y positions of both objects and returns the result coordinate'''
        x = self.X - __o.X
        y = self.Y - __o.Y
        return Coordinate(x,y)

    def __eq__(self, __o: object) -> bool:
        ''' 
        Equality checks are based on the X and Y values rather than instances 
        !if the compared object is member of the same class
        '''

        if isinstance(__o, Coordinate) or isinstance(__o, list):
            if isinstance(__o, list):
                __o = __o[0]
            return __o.X == self.X and __o.Y == self.Y
        else:
            return super(Coordinate, self).__eq__(__o)

    def __ne__(self, __o: object) -> bool:
        ''' 
        Not-Equality checks are based on the X and Y values rather than instances 
        !if the compared object is member of the same class
        '''
        
        if isinstance(__o, Coordinate):
            if isinstance(__o, list):
                __o = __o[0]
            return __o.X != self.X or __o.Y != self.Y
        else:
            return super(Coordinate, self).__ne__(__o)

class MinMax():
    ''' Simple class that holds two variables under the name of MIN and MAX.'''

    def __init__(self, min_val, max_val) -> None:
        '''Defines min and max variables'''
        self.MIN = min_val
        self.MAX = max_val

    def __str__(self) -> str:
        return f"MIN: {self.MIN}, MAX: {self.MAX}"

