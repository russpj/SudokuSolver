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

board = [
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

def PrintRow(row):
	global board
	for col in range(9):
		if board[row][col] == 0:
			print('.', end='')
		else:
			print(board[row][col], end='')
	print()

def PrintBoard():
	for row in range(9):
		PrintRow(row)

def CanPlaceInRow(n, row):
	global board
	for col in range(9):
		if board[row][col] == n:
			return False
	return True;

def CanPlaceInColumn(n, col):
	global board
	for row in range(9):
		if board[row][col] == n:
			return False
	return True

def CanPlaceInSquare(n, row, col):
	global board
	firstRow = (row//3)*3
	firstCol = (col//3)*3
	for row in range(firstRow, firstRow+3):
		for col in range(firstCol, firstCol+3):
			if board[row][col] == n:
				return False
	return True;

def CanPlace(n, row, col) :
	return CanPlaceInRow(n, row) and CanPlaceInColumn(n, col) and CanPlaceInSquare(n, row, col)

def Solve():
	global board
	for row in range(9):
		for col in range(9):
			if board[row][col] == 0:
				for trial in range(1, 10):
					if CanPlace(trial, row, col):
						board[row][col] = trial
						Solve()
				board[row][col] = 0
				return
	PrintBoard()

PrintBoard()
print("Solving...")
Solve()
