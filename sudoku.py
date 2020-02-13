"""
Name: Rifat Ralfi Salhon (Rifat.Salhon@tufts.edu)
Student ID: 1209440
Name: Jacob Kroner
Student ID: 1237221
Assignment 3: Constraint Satisfaction Problems
"""
import sys
import time

# In order to calculate time and display information on the output.
start = time.time()
attempts = 0

"""
This is a class representing the Constraint Satisfaction Problem
Variables: 
    Grid: A 2D representation of the 9x9 sudoku board
    Dict: All possible mappings of variables to domains
"""
class CSP:
    # the __init__ func gets called when a CSP is created
    def __init__(self, pattern):
        self.grid = self.patternToGrid(pattern)
        self.dict = self.createDict()
    
    def getDict(self):
        return self.dict
    
    def getGrid(self):
        return self.grid
    
    def setGrid(self, grid):
        self.grid = grid
    
    # Updates the state of the grid
    def setValue(self, row, col, val):
        self.grid[row][col] = str(val)
        changed = True
        # Fills all squares with only 1 possible value.
        while(changed == True):
            changed = self.fillForcedConstraints()

        # Recalls createDict to update the dict state.
        self.dict = self.createDict()
    
    # Turns a pattern (string of 81 chars) to 2D array
    def patternToGrid(self, pattern):
        inner_list = []
        outer_list = []
        for i in range(9):
            for j in range(9):
                inner_list.append(pattern[i*9+j])
            outer_list.append(inner_list)
            inner_list = []
        return outer_list
    
    # Turns a 2D array to a pattern (string of 81 chars)
    def gridToPattern(self, grid):
        pattern = ""
        for i in range(9):
            for j in range(9):
                pattern += str(grid[i][j])
        return pattern

    # Pretty printing for output
    def printBoard(self):
        print("-=-=-=-=-=-=-=-=-=-=-=-=-")
        for i in range(9):
            temp = "| "
            for j in range(9):
                temp += str(self.grid[i][j]) + " "
                if ((j+1) % 3 == 0):
                    temp += "| "
            
            print(temp)
            if ((i+1) % 3 == 0):
                print("-=-=-=-=-=-=-=-=-=-=-=-=-")
    
    # Returns an array of all possible values that a [*] square can take.
    # row and col values represent the position of the [*] relative to the grid.
    def possibleValues(self, row, col):
        # Start will all possible values, and check constrains one by one.
        possibleValues = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(1, 10):
            # Remove options where an equivalent value appears in the same row.
            for y in range(9):
                if (self.grid[row][y] == str(i) and i in possibleValues):
                    possibleValues.remove(i)
            
            # Remove options where an equivalent value appears in the same column.
            for y in range(9):
                if (self.grid[y][col] == str(i) and i in possibleValues):
                    possibleValues.remove(i)

            # Remove options where an equivalent value appears in the same 3x3 mini-square.
            if row == 0 or row == 1 or row == 2: startRowIndex = 0
            elif row == 3 or row == 4 or row == 5: startRowIndex = 3
            else: startRowIndex = 6
            if col == 0 or col == 1 or col == 2: startColIndex = 0
            elif col == 3 or col == 4 or col == 5: startColIndex = 3
            else: startColIndex = 6
            for y in range(3):
                for z in range(3):
                    if (self.grid[startRowIndex + y][startColIndex + z] == str(i) and i in possibleValues):
                        possibleValues.remove(i)

        return possibleValues
    
    # Sets all [*] squares with only 1 possible valuation to that value.
    def fillForcedConstraints(self):
        changed = False
        for i in range(9):
            for j in range(9):
                if (self.grid[i][j] == "*"):
                    posVals = self.possibleValues(i, j)
                    if (len(posVals) == 1):
                        changed = True
                        self.grid[i][j] = str(posVals[0])
        return changed
    
    # Creates and returns a dictionary where:
    #   keys="row+column" example: "01"
    #   values=[array of possible values]
    def createDict(self):
        keyValues = {}
        for i in range(9):
            for j in range(9):
                if (self.grid[i][j] == "*"):
                    key = str(i)+str(j) # concatenate indeces
                    posValues = self.possibleValues(i, j)
                    if len(posValues) >= 1:
                        keyValues[key] = posValues
        return keyValues

    # Returns the number of [*] squares in the sudoku board.
    def getNumBlank(self):
        num = 0
        for i in range(9):
            for j in range(9):
                if (self.grid[i][j] == "*"):
                    num += 1
        return num

    # Returns the solved 9x9 sudoku board as a 2D array.
    def getFinalAssignments(self):
        return self.grid

# Checks if the 2D representation of a 9x9 sudoku board satisfies constraints.
def satisfies_constraints(array):
	return rows_satisfied(array) and cols_satisfied(array) and squares_satisfied(array)

# Checks a row in the array for constraints.
def rows_satisfied(array):
	for i in range(9):
		for j in range(9):
			for already_checked in range(j):
				if array[i][j] != '*' and array[i][j] == array[i][already_checked]:
					return False
	return True

# Checks a col in the array for constraints.
def cols_satisfied(array):
	for j in range(9):
		for i in range(9):
			for already_checked in range(i):
				if array[i][j] != '*' and array[i][j] == array[already_checked][j]:
					return False
	return True

# Checks a 3x3 mini square for constraints.
def squares_satisfied(array):
	temp2 = 0
	for i in range(3):
		temp = 0
		for j in range(3):
			for number in range(9):
				count = 0
				for x in range(temp, temp+3):
					for y in range(temp2, temp2+3):
						if array[x][y] == number + 1:
							count = count + 1

				if count > 1:
					return False
			temp += 3
		temp2 += 3
	return True

# Initiates the backtracking search for given CSP.
def backtrackingSearch(csp):
    return recursiveBacktracking(csp.getDict(), csp)

# Selects the next unassigned variable ([*] square)
def selectUnassignedVariable(assignment):
    temp = list(assignment)
    key = str(temp[0])

    variable = {}
    variable["row"] = int(key[0])
    variable["col"] = int(key[1])
    variable["key"] = key
    variable["possibleValues"] =  assignment[key]

    return variable

# Checks if given csp is still solvable.
def isConsistent(csp):
    assignment = csp.getDict()
    numBlank = csp.getNumBlank()
    if (numBlank != len(assignment)):
        return False

    return satisfies_constraints(csp.getGrid())

# Turns a pattern (string of 81 chars) to 2D array
def patternToGrid(self, pattern):
    inner_list = []
    outer_list = []
    for i in range(9):
        for j in range(9):
            inner_list.append(pattern[i*9+j])
        outer_list.append(inner_list)
        inner_list = []
    return outer_list

# Base case for recursive backtracking.
# Board is solved, no more assignments necessary.
def isComplete(assignment):
    return len(assignment) == 0

# Main recursive function for backtracking
def recursiveBacktracking(assignment, csp): #returns SOLUTION, or FAILURE 
    if isComplete(assignment):
        return assignment
    
    cspGrid = csp.getGrid()
    variable = selectUnassignedVariable(assignment)
    variable['pattern'] = csp.gridToPattern(csp.getGrid())

    for num in variable["possibleValues"]:
        csp.setGrid(csp.patternToGrid(variable['pattern']))
        csp.setValue(variable['row'], variable['col'], str(num))
        if isConsistent(csp):
            try:
                del assignment[variable['key']]
            except:
                if (csp.getGrid()[variable['row']][variable['col']] == "*"):
                    assignment[variable['key']] = csp.possibleValues(variable['row'], variable['col'])
            result = recursiveBacktracking(assignment, csp)
            if (result != False): 
                # Success! Solution found for the sudoku board.
                return csp.getFinalAssignments()
            
    return False

# Creates the CSP class, solves the sudoku board, and prints the result.
def main(pattern):
    global start
    global attempts

    csp = CSP(pattern)

    if (attempts == 0):
        print("")
        print ("Solving for pattern:", pattern)
        print("Starting condition of the board:")
        csp.printBoard()
    
    result = backtrackingSearch(csp)
    attempts += 1
    
    if (result == False):
        print ("No solution found.")
    elif (csp.getNumBlank() == 0):
        print ("Solution found in", time.time()-start, "seconds!")
        csp.printBoard()
        attempts = 0
    else:
        # Solution is incomplete, solve it
        main(csp.gridToPattern(csp.getGrid()))

# Checks for input and validates input
if __name__ == "__main__":
    if (len(sys.argv)==2) and (len(sys.argv[1]) == 81):
        main((sys.argv[1]))
    elif (len(sys.argv)==2):
        print("Wrong pattern entered.")
    else:
        main("6*87*21**4***1***2*254*****7*1*8*4*5*8*****7*5*9*6*3*1*****675*2***9***8**68*52*3")
        main("*7**42********861*39******7*****4**9**3***7**5**1*****8******76*548********61**5*")
    

# EASY pattern: 6*87*21**4***1***2*254*****7*1*8*4*5*8*****7*5*9*6*3*1*****675*2***9***8**68*52*3
# HARD pattern: *7**42********861*39******7*****4**9**3***7**5**1*****8******76*548********61**5*