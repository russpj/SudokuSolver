# SolveAll.py
# solve all of the puzzles and report the solutions

from time import time
from Puzzle import ParsePuzzleStrings
from SudokuSolver import SudokuSolver

def Main():
	puzzles = ParsePuzzleStrings()
	keySum = 0
	startTime = time()
	for puzzle in puzzles:
		board = puzzle[1]
		trials = 0
		solver = SudokuSolver(board, yieldLevel=0)
		generator = solver.Generate()
		for result in generator:
			# result = next(generator)
			trials += 1
			if result == 2:
				line = solver.board[0]
				key = line[0]*100 + line[1]*10 + line[2]
				keySum += key
				print("After {} trials, we found a solution for {} with a key: {}".format(trials, puzzle[0], key))
	endTime = time()
	print("After {} seconds, the final sum of keys is {}".format(endTime-startTime, keySum))	

if __name__ == '__main__':
	Main()
