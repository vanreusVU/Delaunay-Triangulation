# Default Modules
import sys
from random import randint
from typing import List

# Copyrighted Modules
import pygame

# Custom Modules
from triangulation import Triangle, delaunayTriangulation
from utilities import Coordinate

# Constants
SCREEN_WIDTH, SCREEN_HIGHT = 720, 720 # Screen width and height
NUM_POINTS = 50 # How many points to place
BORDER_MARGIN = 25 # Distance from the borders to not to place points at

class DelaunayTest():

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
        self.clock = pygame.time.Clock()

        self.triangles : List[Triangle] = []
        self.points : List[Coordinate] = []

        # Create points
        self.createRandomPoints()

        # Get triangles
        self.getTriangulation()

        self.begin()
        

    def circle(self, pos : Coordinate, color = (255,255,255)):
        '''
        Draw Circle

        :param pos: center point of the circle
        :type pos: Coordinate
        :param color: color of the circle, defaults to (255,255,255) -> white
        :type color: tuple, optional
        '''        
        pygame.draw.circle(self.screen , color, pos.getTuple(), 5)

    def line(self, from_cord : Coordinate, to_cord : Coordinate, color = (255, 0, 0)):
        '''
        Draw line

        :param from_cord: start of the line
        :type from_cord: Coordinate
        :param to_cord: end of the line
        :type to_cord: Coordinate
        :param color:  color of the line, defaults to (255, 0, 0) -> red
        :type color: tuple, optional
        '''        
        pygame.draw.line(self.screen, color, from_cord.getTuple(), to_cord.getTuple(), 3)

    
    def getTriangulation(self):
        ''' Get Triangles based on the given algorithm '''
        self.triangles = delaunayTriangulation(self.points)

    def createRandomPoints(self):
        ''' Create random points within the given bounds and add them to self.points '''
        for _ in range(NUM_POINTS):
            x = randint(BORDER_MARGIN, SCREEN_WIDTH - BORDER_MARGIN)
            y = randint(BORDER_MARGIN, SCREEN_HIGHT - BORDER_MARGIN)

            point = Coordinate(x, y)

            if point in self.points:
                continue

            self.points.append(point)


    def draw(self):
        ''' Draw triangles and points '''

        for triangle in self.triangles:
            for i in range(len(triangle.verticies)):
                if triangle.verticies[i] == None:
                    continue
                
                if i < len(triangle.verticies) - 1:
                    self.line(triangle.verticies[i], triangle.verticies[i + 1])
                else:
                    self.line(triangle.verticies[0], triangle.verticies[i])
        
        for point in self.points:
            self.circle(point)

        return

    def begin(self):
        # Start the instance

        while True:
            pygame.time.delay(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Fill screen with black color
            self.screen.fill((0,0,0))

            # Call the drawing function
            self.draw()
        
            pygame.display.update()


if __name__ == "__main__":
    DelaunayTest()