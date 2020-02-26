from os import system, name
from time import sleep
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse, Rectangle, Line

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

board = easyBoard

def PrintRow(row):
	global board
	for col in range(9):
		if board[row][col] == 0:
			print('.', end='')
		else:
			print(board[row][col], end='')
		if col == 5 or col == 2:
			print('|', end='')
	print()

def PrintBoard():
	system("cls")
	for row in range(9):
		PrintRow(row)
		if row==2 or row==5:
			print("---+---+---")

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
	return (CanPlaceInRow(n, row) 
				 and CanPlaceInColumn(n, col) 
				 and CanPlaceInSquare(n, row, col))

def Solve():
	global board
	for row in range(9):
		for col in range(9):
			if board[row][col] == 0:
				for trial in range(1, 10):
					if CanPlace(trial, row, col):
						board[row][col] = trial
						PrintBoard()
						Solve()
				board[row][col] = 0
				return
	PrintBoard()
	sleep(4)


class Sudoku(App):
	def build(self):
		self.root = layout = FloatLayout()
		layout.bind(size=self._update_rect, pos=self._update_rect)

		with layout.canvas.before:
			Color(0.1, .9, 0.1, 1)  # green; colors range from 0-1 not 0-255
			self.rect = Rectangle(size=layout.size, pos=layout.pos)
			Color(0.1, .1, .9, 1)
			self.ellipse = Ellipse(size=layout.size, pos=layout.pos)

		return layout

	def updateGrid(self, instance):
		instanceX = instance.pos[0]
		instanceY = instance.pos[1]
		instanceWidth = instance.size[0]
		instanceHeight = instance.size[1]
		if instanceWidth < instanceHeight:
			ellipseSize = [instanceWidth, instanceWidth]
			ellipsePos = [instanceX, instanceY - (instanceWidth-instanceHeight)/2]
		else:
			ellipseSize = [instanceHeight, instanceHeight]
			ellipsePos = [instanceX - (instanceHeight-instanceWidth)/2, instanceY]
		self.ellipse.pos = ellipsePos
		self.ellipse.size = ellipseSize


	def _update_rect(self, instance, value):
		self.root.canvas.clear()
		self.rect.pos = instance.pos
		self.rect.size = instance.size
		self.updateGrid(instance)

def Main():
	Sudoku().run()

if __name__ == '__main__':
	Main()
