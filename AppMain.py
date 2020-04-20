from os import name
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from SudokuSolver import SudokuSolver

class SudokuLayout(GridLayout):
	def __init__(self):
		super().__init__(cols=9)
		self.PlaceStuff()
		self.bind(pos=self.update_rect, size=self.update_rect)

	def PlaceStuff(self):
		with self.canvas.before:
			Color(0.1, .1, .5, 0.1)
			self.square = Rectangle(size=self.size, pos=self.pos)

			# Let's make some lines
			# bold = Color(0.1, .9, 0.1, 1)  # green; colors range from 0-1 not 0-255
			# light = Color(0.1, 0.9, 0.1, .25) #green, but translucent
			bold = [0.1, 0.9, 0.1, 1]
			light = [0.1, 0.9, 0.1, .25]
			self.vlines = []
			self.hlines = []
			for ticks in range(8):
				if ticks%3 == 2:
					Color(0.1, 0.9, 0.1, 1)
				else:
					Color(0.1, 0.9, 0.1, .25)
				self.vlines.append(Line())
				self.hlines.append(Line())

	def InitBoard(self, board):
		# create 81 text input boxes for the values
		self.labels = []
		for row in range(9):
			rowLabels = []
			for col in range(9):
				number = str(board[row][col])
				if number == "0":
					textColor = [1, 0, 0, 1]
					number = " "
				else:
					textColor = [0, 1, 0, 1]
				squareValue = Label(text=number, color=textColor)
				rowLabels.append(squareValue)
				self.add_widget(squareValue)
			self.labels.append(rowLabels)

	def UpdateText(self, board):
		grid=self
		for row in range(9):
			for col in range(9):
				number = str(board[row][col])
				if number == "0":
					number = " "
				label = self.labels[row][col]
				label.text = number
		self.canvas.ask_update()

	def update_rect(self, instance, value):
		# background square
		instance.square.pos = instance.pos
		instance.square.size = instance.size

		# grid lines
		xMin = instance.pos[0]
		dx = instance.size[0]
		xMax = xMin + dx
		yMin = instance.pos[1]
		dy = instance.size[1]
		yMax = yMin + dy
		for ivline in range(len(self.vlines)):
			x = xMin + dx*(ivline+1)/(len(self.vlines)+1)
			self.vlines[ivline].points=(x, yMin, x, yMax)
		for ihline in range(len(self.hlines)):
			y = yMin + dy*(ihline+1)/(len(self.hlines)+1)
			self.hlines[ihline].points = (xMin, y, xMax, y)


# BoardLayout encapsulates the playing board
class BoardLayout(BoxLayout):
	def __init__(self):
		super().__init__()
		self.PlaceStuff()
		self.bind(pos=self.update_rect, size=self.update_rect)

	def PlaceStuff(self):
		with self.canvas.before:
			Color(0.1, .3, 0.1, 1)  # green; colors range from 0-1 not 0-255
			self.rect = Rectangle(size=self.size, pos=self.pos)
			self.sudokuLayout = SudokuLayout()

	def UpdateGridAndLines(self):
		pos = self.pos
		size = self.size
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
		self.sudokuLayout.pos = squarePos
		self.sudokuLayout.size = squareSize
		self.padding = (paddingWidth, paddingHeight)

	def InitBoard(self, board):
		self.sudokuLayout.InitBoard(board)

	def UpdateText(self, board):
		self.sudokuLayout.UpdateText(board)

	def update_rect(self, instance, value):
		instance.rect.pos = instance.pos
		instance.rect.size = instance.size
		self.UpdateGridAndLines()


class HeaderLayout(BoxLayout):
	def __init__(self):
		super().__init__(orientation='horizontal')
		self.PlaceStuff()
		self.bind(pos=self.update_rect, size=self.update_rect)

	def PlaceStuff(self):
		with self.canvas.before:
			Color(0.6, .6, 0.1, 1)  # yellow; colors range from 0-1 not 0-255
			self.rect = Rectangle(size=self.size, pos=self.pos)
			self.fpsLabel = Label(text='0 fps', color=[0.7, 0.05, 0.7, 1])
			self.add_widget(self.fpsLabel)

	def UpdateFPS(self, fps):
		self.fpsLabel.text = '{fpsValue:.0f} fps'.format(fpsValue=fps)

	def update_rect(self, instance, value):
		instance.rect.pos = instance.pos
		instance.rect.size = instance.size


class FooterLayout(BoxLayout):
	def __init__(self):
		super().__init__(orientation='horizontal')
		self.PlaceStuff()
		self.bind(pos=self.update_rect, size=self.update_rect)

	def PlaceStuff(self):
		with self.canvas.before:
			Color(0.4, .1, 0.4, 1)  # purple; colors range from 0-1 not 0-255
			self.rect = Rectangle(size=self.size, pos=self.pos)

	def update_rect(self, instance, value):
		instance.rect.pos = instance.pos
		instance.rect.size = instance.size


class Sudoku(App):
	def build(self):
		self.root = layout = BoxLayout(orientation = 'vertical')

		# header
		self.header = HeaderLayout()
		layout.add_widget(self.header)

		# board
		self.boardLayout = boardLayout = BoardLayout()
		layout.add_widget(boardLayout)

		# footer
		self.footer = FooterLayout()
		layout.add_widget(self.footer)

		self.solver = SudokuSolver()
		board = self.solver.board
		self.boardLayout.InitBoard(board)

		self.generator = self.solver.Generate()
		self.pause = 0.0
		Clock.schedule_interval(self.FrameN, 0.1)

		return layout

	def FrameN(self, dt):
		if dt != 0:
			fps = 1/dt
		else:
			fps = 0
		if self.pause > 0.0:
			self.pause = self.pause-dt
			self.UpdateText(self.solver.board, fps)
			return
		try:
			result = next(self.generator)
			self.UpdateText(self.solver.board, fps)
			if result == 2:
				self.pause = 4.0
		except StopIteration:
			# kill the timer
			self.UpdateText(self.solver.board, fps)

	def UpdateText(self, board, fps):
		self.boardLayout.UpdateText(board)
		self.header.UpdateFPS(fps)


def Main():
	Sudoku().run()

if __name__ == '__main__':
	Main()
