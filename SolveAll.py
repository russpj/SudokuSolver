#!/usr/bin/python3
# 
# SolveAll.py
# solve all of the puzzles and report the solutions

from sys import argv
from getopt import getopt, GetoptError
from time import time
from Puzzle import ParsePuzzleStrings
from SudokuSolver import SudokuSolver

def Main(arguments):
	puzzles = ParsePuzzleStrings()
	keySum = 0
	command_line_documentation = "SolveAll.py -h -f"
	fast = False

	try: 
		opts, args = getopt(arguments, "hf", ("help", "fast"))
	except GetoptError:
		print(f'Invalid arguments: {command_line_documentation}')
		exit(2)

	for opt, arg in opts:
		if opt in ('-h', '--help'):
			print(command_line_documentation)
			exit(0)

		if opt in ('-f', '--fast'):
			fast = True
			
	startTime = time()
	for puzzle in puzzles:
		board = puzzle[1]
		trials = 0
		solver = SudokuSolver(board, fast, yieldLevel=0)
		generator = solver.Generate()
		for result in generator:
			# result = next(generator)
			trials += 1
			if result == 2:
				line = solver.board[0]
				key = line[0]*100 + line[1]*10 + line[2]
				keySum += key
				print(f"After {trials} trials, we found a solution for {puzzle[0]} with a key: {key}")
	endTime = time()
	print(f"After {endTime-startTime} seconds, the final sum of keys is {keySum}")	

if __name__ == '__main__':
	Main(argv[1:])
