# SudokuSolver.py

# Creates the SudokuSolver class, which has a recursive descent with 
# backtracking Sudoku solver

class SudokuSolver:
	def __init__(self, board, yieldLevel=0):
		self.board = board
		self.yieldLevel = yieldLevel
		self.positionsTried = 0

	def CanPlaceInRow(self, n, row):
		for col in range(9):
			if self.board[row][col] == n:
				return False
		return True;

	def CanPlaceInColumn(self, n, col):
		for row in range(9):
			if self.board[row][col] == n:
				return False
		return True

	def CanPlaceInSquare(self, n, row, col):
		firstRow = (row//3)*3
		firstCol = (col//3)*3
		for row in range(firstRow, firstRow+3):
			for col in range(firstCol, firstCol+3):
				if self.board[row][col] == n:
					return False
		return True;

	def CanPlace(self, n, row, col) :
		return (self.CanPlaceInRow(n, row) 
						and self.CanPlaceInColumn(n, col) 
						and self.CanPlaceInSquare(n, row, col))

	def Restart(self):
		self.positionsTried = 0

	def ConditionalYield(self, level, updateTried=True):
		if updateTried:
			self.positionsTried = self.positionsTried + 1
		if level > self.yieldLevel:
			yield level

	def Generate(self):
		for row in range(9):
			for col in range(9):
				if self.board[row][col] == 0:
					for trial in range(1, 10):
						if self.CanPlace(trial, row, col):
							self.board[row][col] = trial
							yield from self.ConditionalYield(1)
							yield from self.Generate()
					self.board[row][col] = 0
					yield from self.ConditionalYield(1, updateTried=False)
					return
		yield from self.ConditionalYield(2)
