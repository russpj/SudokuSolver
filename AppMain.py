from enum import Enum
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from SudokuSolver import SudokuSolver

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


class AppState(Enum):
	Ready = 1
	Running = 2
	Paused = 3
	Finished = 5

nextState={
	AppState.Ready: AppState.Running,
	AppState.Running: AppState.Paused,
	AppState.Paused: AppState.Running,
	AppState.Finished: AppState.Ready
	}


class Speed(Enum):
	Slow=1
	Medium=2
	Fast=3
	Ludicrous=4

nextSpeed={
	Speed.Slow: Speed.Medium,
	Speed.Medium: Speed.Fast,
	Speed.Fast: Speed.Ludicrous,
	Speed.Ludicrous: Speed.Slow
	}

class SpeedInfo:
	def __init__(self, statusText='', fps=0):
		self.statusText=statusText
		self.fps=fps

infoFromSpeed = {
	Speed.Slow: SpeedInfo(statusText='Slow', fps=1),
	Speed.Medium: SpeedInfo(statusText='Medium', fps=10),
	Speed.Fast: SpeedInfo(statusText='High', fps=100),
	Speed.Ludicrous: SpeedInfo(statusText='Ludicrous', fps=100)
	}


class ButtonInfo:
	def __init__(self, enabled=True, text=''):
		self.enabled = enabled
		self.text=text

class AppInfo:
	def __init__(self, statusText='', 
							startInfo=ButtonInfo(),
							difficultyInfo=ButtonInfo(),
							speedInfo=ButtonInfo()):
		self.statusText=statusText
		self.startInfo=startInfo
		self.difficultyInfo=difficultyInfo
		self.speedInfo=speedInfo

infoFromState = {
	AppState.Ready: AppInfo(statusText='{difficulty}', 
												 startInfo=ButtonInfo(text='Start', enabled=True),
												 difficultyInfo=ButtonInfo(text='Change difficulty', enabled=True),
												 speedInfo=ButtonInfo(text='Change Speed', enabled=True)),
	AppState.Running: AppInfo(statusText='{difficulty} Running', 
												 startInfo=ButtonInfo(text='Pause', enabled=True),
												 difficultyInfo=ButtonInfo(text='Change difficulty', enabled=False),
												 speedInfo=ButtonInfo(text='Change Speed', enabled=False)),
	AppState.Paused: AppInfo(statusText='{difficulty} Paused', 
												 startInfo=ButtonInfo(text='Resume', enabled=True),
												 difficultyInfo=ButtonInfo(text='Change difficulty', enabled=False),
												 speedInfo=ButtonInfo(text='Change Speed', enabled=True)),
	AppState.Finished: AppInfo(statusText='{difficulty} Done', 
												 startInfo=ButtonInfo(text='Reset', enabled=True),
												 difficultyInfo=ButtonInfo(text='Change difficulty', enabled=False),
												 speedInfo=ButtonInfo(text='Change Speed', enabled=False))
	}


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
		with self.canvas.after:
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
		with self.canvas.after:
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

	def Reset(self):
		pass

	def update_rect(self, instance, value):
		instance.rect.pos = instance.pos
		instance.rect.size = instance.size
		self.UpdateGridAndLines()


class HeaderLayout(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(orientation='horizontal', **kwargs)
		self.PlaceStuff()
		self.bind(pos=self.update_rect, size=self.update_rect)

	def PlaceStuff(self):
		with self.canvas.before:
			Color(0.6, .6, 0.1, 1)  # yellow; colors range from 0-1 not 0-255
			self.rect = Rectangle(size=self.size, pos=self.pos)
		
		self.fpsLabel = Label(text='0 fps', color=[0.7, 0.05, 0.7, 1])
		self.add_widget(self.fpsLabel)
		self.positionsLabel = Label(text='0 positions tried', color=[0.7, 0.05, 0.7, 1])
		self.add_widget(self.positionsLabel)

	def UpdateText(self, fps, positions):
		self.fpsLabel.text = '{fpsValue:.0f} fps'.format(fpsValue=fps)
		self.positionsLabel.text = '{positionsValue:.0f} positions tried'.format(positionsValue=positions)

	def update_rect(self, instance, value):
		instance.rect.pos = instance.pos
		instance.rect.size = instance.size


class FooterLayout(BoxLayout):
	def __init__(self, start_button_callback=None, **kwargs):
		super().__init__(orientation='horizontal', padding=10, **kwargs)
		self.start_button_callback=start_button_callback
		self.PlaceStuff()
		self.bind(pos=self.update_rect, size=self.update_rect)

	def PlaceStuff(self):
		with self.canvas.before:
			Color(0.4, .1, 0.4, 1)  # purple; colors range from 0-1 not 0-255
			self.rect = Rectangle(size=self.size, pos=self.pos)
		
		self.startButton = Button(text='')
		self.add_widget(self.startButton)
		self.startButton.bind(on_press=self.start_button_callback)
		self.UpdateButtons()

	def update_rect(self, instance, value):
		instance.rect.pos = instance.pos
		instance.rect.size = instance.size

	def UpdateButtons(self, appInfo=infoFromState[AppState.Ready]):
		startInfo = appInfo.startInfo
		self.startButton.text = startInfo.text
		self.startButton.disabled = not startInfo.enabled


class Sudoku(App):
	def build(self):
		self.root = layout = BoxLayout(orientation = 'vertical')

		# header
		self.header = HeaderLayout(size_hint=(1, .1))
		layout.add_widget(self.header)

		# board
		self.boardLayout = boardLayout = BoardLayout()
		layout.add_widget(boardLayout)

		# footer
		self.footer = FooterLayout(size_hint=(1, .2), start_button_callback=self.StartButtonCallback)
		layout.add_widget(self.footer)

		global easyBoard
		global hardBoard
		self.solver = SudokuSolver(easyBoard, yieldLevel=0)
		board = self.solver.board
		self.boardLayout.InitBoard(board)

		self.speed = Speed.Fast
		self.state=AppState.Ready

		return layout

	def FrameN(self, dt):
		if self.generator is None:
			return
		if (self.state==AppState.Finished or self.state==AppState.Ready):
			return
		if self.state==AppState.Paused:
			return
		if dt != 0:
			fpsValue = 1/dt
		else:
			fpsValue = 0

		try:
			result = next(self.generator)
			if result == 2:
				self.state = AppState.Paused
				self.clock.cancel()
			self.UpdateUX(fps=fpsValue)
		except StopIteration:
			self.state=AppState.Finished
			self.clock.cancel()
			self.generator=None
			self.UpdateUX(fps=fpsValue)
			

	def StartClock(self):
		self.clock = Clock.schedule_interval(self.FrameN, 1.0/infoFromSpeed[self.speed].fps)

	def UpdateUX(self, fps=0):
		state = self.state
		speed = self.speed
		appInfo = infoFromState[self.state]
		self.UpdateText(fps=fps, positions=self.solver.positionsTried)
		self.footer.UpdateButtons(appInfo=appInfo)

	def UpdateText(self, fps, positions=True):
		self.boardLayout.UpdateText(self.solver.board)
		self.header.UpdateText(fps=fps, positions=self.solver.positionsTried)

	def StartButtonCallback(self, instance):
		if self.state==AppState.Ready:
			self.generator = self.solver.Generate()
			self.StartClock()
		if self.state==AppState.Running:
			self.clock.cancel()
		if self.state==AppState.Paused:
			self.StartClock()
		if self.state==AppState.Finished:
			self.boardLayout.Reset()
		self.state = nextState[self.state]
		self.UpdateUX()


def Main():
	Sudoku().run()

if __name__ == '__main__':
	Main()
