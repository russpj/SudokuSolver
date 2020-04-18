from os import system


simpleSudoku = [
	[1, 2, 3, 4, 5, 6, 7, 8, 9],
	[4, 5, 6, 7, 8, 9, 1, 2, 3],
	[7, 8, 9, 1, 2, 3, 4, 5, 6],
	[2, 3, 4, 5, 6, 7, 8, 9, 1],
	[5, 6, 7, 8, 9, 1, 2, 3, 4],
	[8, 9, 1, 2, 3, 4, 5, 6, 7],
	[3, 4, 5, 6, 7, 8, 9, 1, 2],
	[6, 7, 8, 9, 1, 2, 3, 4, 5],
	[9, 1, 2, 3, 4, 5, 6, 7, 8],
	]

hardBoard = [
	[0,0,0,4,0,6,0,0,0],
	[7,0,0,2,0,0,0,9,0],
	[0,0,0,0,5,3,0,0,4],
	[0,1,3,0,0,0,0,4,9],
	[0,0,0,0,0,0,0,0,0],
	[0,0,4,5,0,0,0,0,2],
	[3,7,0,0,6,0,0,1,0],
	[5,0,0,0,0,0,0,0,0],
	[0,2,0,0,0,0,7,0,0]
	]

easyBoard = [
	[0,0,0,0,0,4,6,7,0],
	[0,0,9,2,0,0,8,0,1],
	[0,0,7,6,1,3,0,4,9],
	[0,5,0,1,0,0,2,8,4],
	[0,1,0,0,0,0,3,9,6],
	[4,9,6,8,0,0,0,5,0],
	[3,0,0,0,6,1,0,2,0],
	[0,8,5,4,0,0,0,6,0],
	[9,0,0,0,7,8,0,0,0],
	]


class SudokuSolver:
	def __init__(self):
		global easyBoard
		self.board = easyBoard

	def PrintRow(self, row):
		for col in range(9):
			if self.board[row][col] == 0:
				print('.', end='')
			else:
				print(self.board[row][col], end='')
			if col == 5 or col == 2:
				print('|', end='')
		print()

	def PrintBoard(self):
		system("cls")
		for row in range(9):
			self.PrintRow(row)
			if row==2 or row==5:
				print("---+---+---")

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

	def Solve(self):
		for row in range(9):
			for col in range(9):
				if self.board[row][col] == 0:
					for trial in range(1, 10):
						if self.CanPlace(trial, row, col):
							self.board[row][col] = trial
							self.PrintBoard()
							self.Solve()
					self.board[row][col] = 0
					return
		self.PrintBoard()
		sleep(4)

	def Generate(self):
		for row in range(9):
			for col in range(9):
				if self.board[row][col] == 0:
					for trial in range(1, 10):
						if self.CanPlace(trial, row, col):
							self.board[row][col] = trial
							# self.PrintBoard()
							yield 1
							yield from self.Generate()
					self.board[row][col] = 0
					return
		# self.PrintBoard()
		yield 2
