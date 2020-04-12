from os import name
from SudokuSolver import SudokuSolver

def Main():
	solver = SudokuSolver()
	solver.Generate()

if __name__ == '__main__':
	Main()
