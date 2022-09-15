# SudokuSolver.py

# Creates the SudokuSolver class, which has a recursive descent with 
# backtracking Sudoku solver

from random import shuffle
from math import sqrt

class Square:
	def __init__(self, row, column):
		self.row = row
		self.col = column


def ScoreRow(board, row):
	score = set()
	for col in range(len(board[0])):
		if board[row][col] != 0:
			score.add(board[row][col])
	return score


def ScoreColumn(board, col):
	score = set()
	for row in range(len(board)):
		if board[row][col] != 0:
			score.add(board[row][col])
	return score


def ScoreSection(board, square):
	score = set()
	sizeSection = int(sqrt(len(board))+0.5)
	firstRow = (square.row//sizeSection)*3
	firstCol = (square.col//sizeSection)*3
	for row in range(firstRow, firstRow+sizeSection):
		for col in range(firstCol, firstCol+sizeSection):
			if board[row][col] != 0:
				score.add(board[row][col])
	return score


def ScoreSquare(board, square):
	if board[square.row][square.col] != 0:
		return 0

	score = set()
	score |= ScoreRow(board, square.row)
	score |= ScoreColumn(board, square.col)
	score |= ScoreSection(board, square)
	return len(score)


def BringMaxToFront(board, squares, first, last):
	if first >= last:
		return
	firstScore = ScoreSquare(board, squares[first])
	for index in range(first, last):
		thisScore = ScoreSquare(board, squares[index])
		if thisScore > firstScore:
			squares[first], squares[index] = squares[index], squares[first]
			firstScore = thisScore

def EmptySquares(board):
	squares = []
	for row in range(len(board)):
		for col in range(len(board[0])):
			if board[row][col] == 0:
				squares.append(Square(row, col))

	# squares.sort(key = lambda square: -ScoreSquare(board, square))
	BringMaxToFront(board, squares, 0, len(squares))
	return squares

class SudokuSolver:
	def __init__(self, board, yieldLevel=0):
		self.board = board
		self.yieldLevel = yieldLevel
		self.positionsTried = 0
		self.squares = EmptySquares(board)

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
		for index in range(len(self.squares)):
			square = self.squares[index]
			row = square.row
			col = square.col
			if self.board[row][col] == 0:
				for trial in range(1, 10):
					if self.CanPlace(trial, row, col):
						self.board[row][col] = trial
						yield from self.ConditionalYield(1)
						BringMaxToFront(self.board, self.squares, index+1, len(self.squares))
						yield from self.Generate()
				self.board[row][col] = 0
				yield from self.ConditionalYield(1, updateTried=False)
				return
		yield from self.ConditionalYield(2)
