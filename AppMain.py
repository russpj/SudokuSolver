from os import name
from time import sleep
from SudokuSolver import SudokuSolver

def Main():
	solver = SudokuSolver()
	for result in solver.Generate():
		solver.PrintBoard()
		if result == 2:
			sleep(4)

if __name__ == '__main__':
	Main()
