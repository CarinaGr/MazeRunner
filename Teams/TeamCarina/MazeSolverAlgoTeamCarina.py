
"""
This class is the template class for the Maze solver
"""

import sys
from math import sqrt
import numpy
import queue

class MazeSolverAlgoTeamCarina:

    EMPTY = 0       # empty cell
    OBSTACLE = 1    # cell with obstacle / blocked cell
    START = 2       # the start position of the maze (red color)
    TARGET = 3      # the target/end position of the maze (green color)

    def __init__(self):
        self.dimCols = 0 
        self.dimRows = 0 
        self.startCol = 0 
        self.startRow = 0 
        self.endCol = 0 
        self.endRow = 0
        self.grid=[[]] 
        print("Main Solver TeamCarina initialisiert")

    # Setter method for the maze dimension of the rows
    def setDimRows(self, rows):
         self.dimRows = rows
        

    # Setter method for the maze dimension of the columns
    def setDimCols(self, cols):
          self.dimColumns = cols
   
        
    # Setter method for the column of the start position 
    def setStartCol(self, col):
        self.startCol = col
       

    # Setter method for the row of the start position 
    def setStartRow(self, row):
        self.startRow = row
       

    # Setter method for the column of the end position 
    def setEndCol(self, col):
        self.endCol = col
        

    # Setter method for the row of the end position 
    def setEndRow(self, row):
        self.endRow = row
         

    # Setter method for blocked grid elements
    def setBlocked(self,row ,col):
        self.grid[row][col] = self.OBSTACLE

    # Start to build up a new maze
    # HINT: don't forget to initialize all member variables of this class (grid, start position, end position, dimension,...)
    def startMaze(self, columns, rows):
        if rows == 0 and columns == 0:
            self.startCols = 0 
            self.startRows = 0 
            self.endCols = 0 
            self.endRows = 0 


        self.grid=[[]] 

        #HINT: populate grid with dimension row,column with zeros
        if columns>0 and rows>0:
            self.grid = numpy.empty((rows, columns), dtype=int)
            for i in range(rows):
                for j in range(columns):
                    self.grid[i][j]= self.EMPTY

    # Define what shall happen after the full information of a maze has been received
    def endMaze(self):
        self.grid[self.startRow][self.startCol] = self.START
        self.grid[self.endRow][self.endCol] = self.TARGET

        # HINT: did you set start position and end position correctly?

    # just prints a maze on the command line
    def printMaze(self):
        print(self.grid)

    # loads a maze from a file pathToConfigFile
    def loadMaze(self,pathToConfigFile):
        self.grid=numpy.loadtxt(pathToConfigFile, delimiter=',',dtype=int)
        self.dimCols=self.grid.shape[0]
        self.dimRows=self.grid.shape[1]

        start_arr = numpy.where(self.grid == 2)
        self.startRow=int(start_arr[0][0])
        self.startCol=int(start_arr[1][0])

        end_arr = numpy.where(self.grid == 3)
        self.endRow=int(end_arr[0][0])
        self.endCol=int(end_arr[1][0])
        

    # clears the complete maze 
    def clearMaze(self):
        self.dimCols = 0
        self.dimRows = 0
        self.startMaze(0,0)
  
    # Decides whether a certain row,column grid element is inside the maze or outside
    def isInGrid(self,row,column):
        if row < 0:
            return False

        if column < 0:
            return False

        if row >= self.grid.shape[0]:
            return False

        if column >= self.grid.shape[1]:
            return False

        return True


    # Returns a list of all grid elements neighboured to the grid element row,column
    def getNeighbours(self,row,column):
        neighbours = []

        # no neighbours for out-of-grid elements
        if self.isInGrid(row,column) == False:
            return neighbours

        # no neighbours for blocked grid elements
        if self.grid[row,column] == self.OBSTACLE:
            return neighbours
    
        nextRow = row + 1    
        if (self.isInGrid(nextRow,column) is True and self.grid[nextRow][column] != self.OBSTACLE):
            neighbours.append([nextRow,column])

        previousRow = row - 1    
        if (self.isInGrid(previousRow,column) is True and self.grid[previousRow][column] != self.OBSTACLE):
            neighbours.append([previousRow,column])

        nextColumn = column + 1    
        if (self.isInGrid(row,nextColumn) is True and self.grid[row][nextColumn] != self.OBSTACLE):
            neighbours.append([row,nextColumn])

        previousColumn = column - 1    
        if (self.isInGrid(row,previousColumn) is True and self.grid[row][previousColumn] != self.OBSTACLE):
            neighbours.append([row,previousColumn])

        return neighbours

    # Gives a grid element as string, the result should be a string row,column
    def gridElementToString(self,row,col):
        # HINT: this method is used as primary key in a lookup table
        result = ""
        result += str(row)
        result += ","
        result += str(col)
        return result
        
    
    # check whether two different grid elements are identical
    # aGrid and bGrid are both elements [row,column]
    # ist row and column the same
    def isSameGridElement(self, aGrid, bGrid):
        if (aGrid[0] == bGrid[0] and aGrid[1] == bGrid[1]):
            return True

        return False


    # Defines a heuristic method used for A* algorithm
    # aGrid and bGrid are both elements [row,column]
    # Abstand zum Ziel
    def heuristic(self, aGrid, bGrid):
        return abs(aGrid[0] - bGrid[0]) + abs(aGrid[1] - bGrid[1])
        # HINT: a good heuristic could be the distance between to grid elements aGrid and bGrid

    # Generates the resulting path as string from the came_from list
    def generateResultPath(self,came_from):
        result_path = []
        # HINT: this method is a bit tricky as you have to invert the came_from list (follow the path from end to start)


        #############################
        # Here Creation of Path starts
        #############################
        startKey = self.gridElementToString(self.startRow , self.startCol)
        currentKey = self.gridElementToString(self.endRow , self.endCol)
        path = []
        while currentKey != startKey: 
            path.append(currentKey)
            current = came_from[currentKey]
            currentKey = self.gridElementToString(current[0],current[1])

        path.append(startKey)
        path.reverse()
        #############################
        # Here Creation of Path ends
        #############################        




    #############################
    # Definition of Maze solver algorithm
    #
    # implementation taken from https://www.redblobgames.com/pathfinding/a-star/introduction.html
    #############################
    def myMazeSolver(self):

        #############################
        # Here Breadth First starts
        #############################
        start = [self.startRow,self.startCol]
        frontier = queue.Queue()
        frontier.put(start)
        startKey = self.gridElementToString(self.startRow , self.startCol)

        came_from = {}
        came_from[startKey] = None
        while not frontier.empty():
            current = frontier.get()

            for next in self.getNeighbours(current[0],current[1]):
                nextKey = self.gridElementToString(next[0] , next[1])
                if nextKey not in came_from:
                    frontier.put(next)
                    came_from[nextKey] = current

        #############################
        # Here Breadth First ends
        #############################

        current = [self.endRow , self.endCol]
        start = [self.startRow , self.startCol]
        path = []
        while current != start:
            path.append(current)
            current = came_from[self.gridElementToString(current[0],current[1])]

        path.append(start)
        path.reverse()
        print(path)
        
        return path



    # Command for starting the solving procedure
    def solveMaze(self):
        return self.myMazeSolver()


if __name__ == '__main__':
    mg = MazeSolverAlgoTeamCarina()


    # HINT: in case you want to develop the solver without MQTT messages and without always
    #       loading new different mazes --> just load any maze you would like from a file

    mg.loadMaze("..\\..\\MazeExamples\\Maze1.txt")
    mg.printMaze()

    neighbours = mg.getNeighbours(2,4)
    print(neighbours)
    mg.myMazeSolver()
    #solutionString = mg.solveMaze()
    #print(solutionString)
   
