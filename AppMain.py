from os import name
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from SudokuSolver import SudokuSolver


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
			
			self.solver = SudokuSolver()
			board = self.solver.board

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

			self.generator = self.solver.Generate()

			# Clock.schedule_once(self.Frame0, 1)
			Clock.schedule_interval(self.FrameN, 1.0)

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

	def Frame0(self, dt):
		self.solver.Solve()
		self.UpdateText(self.solver.solvedBoard)

	def FrameN(self, dt):
		stop = False
		try:
			result = next(self.generator)
			self.UpdateText(self.solver.board)
			self.root.canvas.ask_update()
		except StopIteration:
			# kill the timer
			stop = True


	def UpdateText(self, board):
		grid=self.grid
		ids = grid.ids
		for row in range(9):
			for col in range(9):
				number = str(board[row][col])
				if number == "0":
					number = " "
				label = self.labels[row][col]
				label.text = number
		self.root.canvas.ask_update()


def Main():
	Sudoku().run()

if __name__ == '__main__':
	Main()
