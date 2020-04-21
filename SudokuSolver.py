from time import sleep
from os import system
from collections import deque


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

class SudokuSolver:
	def __init__(self, board):
		self.board = board
		self.yieldLevel = 0
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

	def ConditionalYield(self, level):
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
					yield from self.ConditionalYield(1)
					return
		yield from self.ConditionalYield(2)
