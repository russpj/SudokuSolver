from os import system, name
from time import sleep
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

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


class Sudoku(App):
	def build(self):
		self.root = layout = AnchorLayout(anchor_x = 'center', anchor_y='center')
		layout.bind(size=self._update_rect, pos=self._update_rect)
		self.grid = GridLayout(cols=9)
		layout.add_widget(self.grid)

		with layout.canvas.before:
			Color(0.1, .9, 0.1, 1)  # green; colors range from 0-1 not 0-255
			self.rect = Rectangle(size=layout.size, pos=layout.pos)
			Color(0.1, .1, .9, 1)
			self.square = Rectangle(size=layout.size, pos=layout.pos)
			
			# create 81 text input boxes for the values
			self.labels = []
			for row in range(9):
				rowLabels = []
				for col in range(9):
					number = str(board[row][col])
					if number == "0":
						number = " "
					squareValue = Label(text=number)
					rowLabels.append(squareValue)
					self.grid.add_widget(squareValue)
				self.labels.append(rowLabels)

			Color(0.1, .9, 0.1, 1)  # green; colors range from 0-1 not 0-255
			self.vline1 = Line()
			self.vline2 = Line()
			self.hline1 = Line()
			self.hline2 = Line()

			Clock.schedule_once(self.Solve, 1)

		return layout

	def updateGrid(self, pos, size):
		instanceX = pos[0]
		instanceY = pos[1]
		instanceWidth = size[0]
		instanceHeight = size[1]
		if instanceWidth < instanceHeight:
			squareSize = [instanceWidth, instanceWidth]
			squarePos = [instanceX, instanceY - (instanceWidth-instanceHeight)/2]
			paddingWidth = 0
			paddingHeight = (instanceHeight-instanceWidth)/2
		else:
			squareSize = [instanceHeight, instanceHeight]
			squarePos = [instanceX - (instanceHeight-instanceWidth)/2, instanceY]
			paddingWidth = (instanceWidth - instanceHeight)/2
			paddingHeight = 0
		self.square.pos = squarePos
		self.square.size = squareSize
		self.root.padding = (paddingWidth, paddingHeight)

		self.vline1.points = (squarePos[0] + squareSize[0]/3, squarePos[1], squarePos[0] + squareSize[0]/3, squarePos[1]+squareSize[1])
		self.vline2.points = (squarePos[0] + 2*squareSize[0]/3, squarePos[1], squarePos[0] + 2*squareSize[0]/3, squarePos[1]+squareSize[1])
		self.hline1.points = (squarePos[0], squarePos[1] + squareSize[1]/3, squarePos[0]+squareSize[0], squarePos[1] + squareSize[1]/3)
		self.hline2.points = (squarePos[0], squarePos[1] + 2*squareSize[1]/3, squarePos[0]+squareSize[0], squarePos[1] + 2*squareSize[1]/3)

	def _update_rect(self, instance, value):
		self.root.canvas.clear()
		self.rect.pos = instance.pos
		self.rect.size = instance.size
		self.updateGrid(instance.pos, instance.size)


	def UpdateText(self):
		grid=self.grid
		ids = grid.ids
		for row in range(9):
			for col in range(9):
				number = str(board[row][col])
				if number == "0":
					number = " "
				label = self.labels[row][col]
				label.text = number

	def PrintBoard(self):
		self.UpdateText()

	def Solve(self, dt):
		global board
		for row in range(9):
			for col in range(9):
				if board[row][col] == 0:
					for trial in range(1, 10):
						if CanPlace(trial, row, col):
							board[row][col] = trial
							self.PrintBoard()
							self.Solve(self)
					board[row][col] = 0
					return
		self.PrintBoard()
		sleep(4)


def Main():
	Sudoku().run()

if __name__ == '__main__':
	Main()
