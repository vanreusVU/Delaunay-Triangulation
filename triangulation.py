# Default Modules
from typing import List

# Custom Modules
from utilities import Coordinate, MinMax


class Edge():
    ''' An edge consisting of the verticies '''
    
    def __init__(self, point1 : Coordinate, point2 : Coordinate) -> None:
        self.p1 = point1
        self.p2 = point2

    def __eq__(self, __o: object) -> bool:
        ''' 
        Equality checks are based on the P1 and P2 values rather than instances 
        !if the compared object is member of the same class
        '''

        if isinstance(__o, Edge):
            if isinstance(__o, list):
                __o = __o[0]
            return (__o.p1 == self.p1 and __o.p2 == self.p2) or (__o.p1 == self.p2 and __o.p2 == self.p1)
        else:
            return super(Edge, self).__eq__(__o)

    def __ne__(self, __o: object) -> bool:
        ''' 
        Equality checks are based on the P1 and P2 values rather than instances 
        !if the compared object is member of the same class
        '''

        if isinstance(__o, Edge):
            if isinstance(__o, list):
                __o = __o[0]
            return (__o.p1 != self.p1 or __o.p2 != self.p2) and (__o.p1 != self.p2 or __o.p2 != self.p1)
        else:
            return super(Edge, self).__ne__(__o)

    def __str__(self) -> str:
        return f"Edge P1: {self.p1}, P2: {self.p2}"

class Triangle():        
    ''' Triangle object to be used for triangulation '''

    def __init__(self, triangle_verticies) -> None:     
        self.verticies : List[Coordinate] = triangle_verticies
        self.edges : List[Edge] = [
            Edge(self.verticies[0], self.verticies[1]),
            Edge(self.verticies[1], self.verticies[2]),
            Edge(self.verticies[2], self.verticies[0])
            ]

    def __eq__(self, __o: object) -> bool:
        ''' 
        Equality checks are based on the verticies and edges rather than instances 
        !if the compared object is member of the same class
        '''

        if isinstance(__o, Triangle):
            if isinstance(__o, list):
                __o = __o[0]
            return __o.edges == self.edges and __o.verticies == self.verticies
        else:
            return super(Triangle, self).__eq__(__o)

    def __ne__(self, __o: object) -> bool:
        ''' 
        Equality checks are based on the verticies and edges rather than instances 
        !if the compared object is member of the same class
        '''

        if isinstance(__o, Triangle):
            if isinstance(__o, list):
                __o = __o[0]
            return __o.edges != self.edges or __o.verticies != self.verticies
        else:
            return super(Triangle, self).__ne__(__o)

    def __str__(self) -> str:
        return f"Triangle: \nP1: {self.verticies[0]}\nP2: {self.verticies[1]}\nP3: {self.verticies[2]}"

def determinant(matrix : List[List[int]]):
    '''
    Return the determinant of the given 2d matrix
    https://mathworld.wolfram.com/Determinant.html

    :param matrix: Determinant input, a square matrix with integars 
    :type matrix: List[List[int]]
    :return: result from the determinant of the input
    :rtype: int
    '''      
    determinants = []

    # Final stage where you return the determinant of the given 2x2
    if len(matrix) == 2:
        return (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])

    # Go thourgh the first row and take their detarminants
    for i in range(len(matrix)):
        # Quick list comprehension to remove the needed rows and columns
        new_matrix = [[matrix[y][x] for x in range(len(matrix[y])) if x != i] for y in range(len(matrix)) if y != 0]
        new_determinant = determinant(new_matrix)

        # Tuple [0] = main element
        # Tuple [1] = resulting determinant of that element
        determinants.append((matrix[0][i] , new_determinant))

    if len(determinants) == 0:
        print("ERROR in matrix")
        return -1

    total = determinants[0][0] * determinants[0][1]
    for i in range(1, len(determinants)):
        if i % 2 != 0:
            total -= determinants[i][0] * determinants[i][1]
        else:
            total += determinants[i][0] * determinants[i][1] 

    return total

def isWithinCircumcircle(point : Coordinate, triangle : Triangle):
    '''
    Returns true if the given point is within the circumcircle of the given triangle.
    IMPORTANT: Give the triangle points in counterclockwise order

    :param point: point to check
    :type point: Coordinate
    :param triangle: triangle to form the circumcircle from
    :type triangle: Triangle
    :return: weather the point is within the circumcircle of the given triangle
    :retval True: point within circumcircle
    :retval False: point is not within circumcircle
    :rtype: boolean
    '''    
    
    determ_matrix = []
    points_to_work = [point]
    points_to_work[:0] = triangle.verticies[:]

    for tri_point in points_to_work:
        x = tri_point.X
        y = tri_point.Y

        sum_squared = pow(x,2) + pow(y,2)

        determ_matrix.append([x,y,sum_squared,1])

    # If the determinant is positive it means the point is within circumcircle of the given points
    # https://mathworld.wolfram.com/Circumcircle.html
    return determinant(determ_matrix) >= 0


def getCoveringSquare(points : List[Coordinate]) -> MinMax(Coordinate, Coordinate):
    '''
    Returns bottom left and top right corner of a square that contains all of the points withing

    :param points: points to get the edge points of
    :type points: List[Coordinate]
    :return: MIN is for bottom left corner, MAX is for top right corner
    :rtype: MinMax(Coordinate, Coordinate)
    '''    
    
    if len(points) <= 0:
        print("ERROR: Empty list")
        return None


    place_holder = points[0]
    top_right : Coordinate = Coordinate(place_holder.X, place_holder.Y)
    bottom_left : Coordinate = Coordinate(place_holder.X, place_holder.Y)

    for point in points:
        if point.X > top_right.X:
            top_right.X = point.X
        
        if point.Y > top_right.Y:
            top_right.Y = point.Y
        
        if point.X < bottom_left.X:
            bottom_left.X = point.X
        
        if point.Y < bottom_left.Y:
            bottom_left.Y = point.Y

    return MinMax(bottom_left,top_right)

def getSuperTriangle(edgePoints : MinMax) -> Triangle:
    '''
    Returns a triangle that covers the given edge points

    :param edgePoints: a MinMax object with min and max X,Y locations that forms a square around the whole triangle
    :type edgePoints: MinMax(Coordinate, Coordinate)
    :return: a triangle that covers all of the edge points
    :rtype: Triangle
    '''    

    safetey_length = 1500

    p1 : Coordinate =  Coordinate(edgePoints.MAX.X + safetey_length, edgePoints.MIN.Y - safetey_length)
    p2 : Coordinate =  Coordinate(edgePoints.MAX.X + safetey_length, edgePoints.MAX.Y + abs(edgePoints.MAX.Y - edgePoints.MIN.Y) + safetey_length)
    p3 : Coordinate =  Coordinate(edgePoints.MIN.X - abs(edgePoints.MAX.X - edgePoints.MIN.X) - safetey_length, edgePoints.MIN.Y - safetey_length)

    return Triangle([p1,p2,p3])

def delaunayTriangulation(points : List[Coordinate]) -> List[Triangle]:
    '''
    Creates delaunay triangulation using bowyer and watson algorithm 
    https://en.wikipedia.org/wiki/Delaunay_triangulation
    https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm

    :param points: list of points to form the delanuay triangulation with
    :type points: List[Coordinate]
    :return: a list of triangles that forms the delaunay triangulation
    :rtype: List[Triangle]
    '''    
    
    # points is a list of coordinates defining the points to be triangulated
    triangulation : List[Triangle] = []
    
    # Create a super triangle that contains all of the points within it
    super_triangle = getSuperTriangle(getCoveringSquare(points))

    # Add the super triangle to the triangulation list
    triangulation.append(super_triangle)

    # One by one add the given point to all the triangles
    for point in points:
        bad_triangles : List[Triangle] = []

        # Find triangles that the point intercepts with their circumcircle
        for triangle in triangulation:
            if isWithinCircumcircle(point, triangle):
                bad_triangles.append(triangle)

        polygon : List[Edge] = []
        
        # Find the boundary of the polygonal hole
        for triangle1 in bad_triangles:
            for edge in triangle1.edges:
                edge_shared = False
                for triangle2 in bad_triangles:
                    if triangle1 == triangle2:
                        continue
                    
                    if edge in triangle2.edges:
                        edge_shared = True
                
                if edge_shared == False:
                    polygon.append(edge)
        
        # Remove broken triangles from the triangulation list
        for triangle in bad_triangles:
            triangulation.remove(triangle)

        # Create triangles with the newly created edges
        for edge in polygon:
            new_triangle = Triangle([edge.p1,edge.p2,point])
            triangulation.append(new_triangle)

    # Remove the triangles that has connection to the super-triangle
    super_verticies = super_triangle.verticies
    for i in range(len(triangulation)-1, -1, -1):
        triangle = triangulation[i]
        
        has_common = False
        for vertex1 in triangle.verticies:
            for vertex2 in super_verticies:
                if vertex1 == vertex2:
                    has_common = True
        
        if has_common == True:
            triangulation.remove(triangle)

    # Return the delaunay triangulation
    return triangulation
