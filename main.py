from classes.Board import Board
from classes.InvalidSquareException import InvalidSquareException
from time import sleep
from os import system
from random import randint


def automove(DEBUG = True, playAfter = False):
	sleepTime = .2
	board = Board()

	#BUG GAME
	moves = [
		("c2", "c4", "white"),
		("a7", "a6", "black"),
		("c4", "c5", "white"),
		("a6", "a5", "black"),
		("c5", "C6", "white"),
		("a5", "a4", "black"),
		("c6", "d7", "white"),
		("d8", "d7", "black"),
		("d2", "d4", "white"),
		("d7", "d8", "black"),
		("d4", "d5", "white"),
		("a4", "a3", "black"),
		("d5", "d6", "white"),
		("b7", "b6", "black"),
		("d6", "e7", "white"),
		("b6", "b5", "black"),
	]

	if not DEBUG:
		system("clear")
	print(board)
	sleep(sleepTime)

	for move in moves:
		if not DEBUG:
			system("clear")
		board.makeMove(*move)
		print(board)
		sleep(sleepTime)
	
	if playAfter:
		play(board)

def singlePieceChecks():
	board = Board()
	print(board)

	bra = [[False]*8 for _ in range(8)]
	bra[3][3] = True

	print(board.board_arr[3][3].attacks(bra))


def stupidAI():
	board = Board()
	
	curr_player = "white"
	running = True

	while running:

		while True:
			system("clear")
			print(board)

			if board.CHECKMATE:
				print(f"It's checkmate! {board.LASTPLAYERCOLOR.capitalize()} has won!")
				running = False
				break
			elif board.STALEMATE:
				print(f"It's stalemate! The game is a draw.")
				running = False
				break

			if curr_player == "white":

				move = input(f"{curr_player.capitalize()} to move: ")
				try:
					move = move.split(" ")
					l = len(move)
					if l not in (2, 3):
						raise InvalidSquareException

					if l == 2:
						result = board.makeMove(move[0], move[1], curr_player)
					else:
						result = board.makeMove(move[0], move[1], curr_player, promotionTo = move[2])

					if not result:
						print("Invalid move!")
						sleep(2)
						continue

					break

				except InvalidSquareException:
					print("Invalid input!")
					sleep(2)

			else:
				while True:
					s_square = randint(0, 7), randint(0, 7)
					d_square = randint(0, 7), randint(0, 7)

					result = board.makeMove(s_square, d_square, curr_player)

					if result:
						break

				break



		curr_player = "black" if curr_player == "white" else "white"


def play(board = None):
	if not board:
		board = Board()
	
	curr_player = "black" if board.LASTPLAYERCOLOR == "white" else "white"
	running = True

	while running:

		while True:
			system("clear")
			print(board)

			if board.CHECKMATE:
				print(f"It's checkmate! {board.LASTPLAYERCOLOR.capitalize()} has won!")
				running = False
				break
			elif board.STALEMATE:
				print(f"It's stalemate! The game is a draw.")
				running = False
				break

			move = input(f"{curr_player.capitalize()} to move: ")
			try:
				move = move.split(" ")
				l = len(move)
				if l not in (2, 3):
					raise InvalidSquareException

				if l == 2:
					result = board.makeMove(move[0], move[1], curr_player)
				else:
					result = board.makeMove(move[0], move[1], curr_player, promotionTo = move[2])

				if not result:
					print("Invalid move!")
					sleep(2)
					continue

				break

			except InvalidSquareException:
				print("Invalid input!")
				sleep(2)

		curr_player = "black" if curr_player == "white" else "white"


if __name__ == "__main__":
	#automove(False, True)
	#play()

	stupidAI()