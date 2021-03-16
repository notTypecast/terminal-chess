from classes.Piece import Piece


class Pawn(Piece):

	#assumes square and color are correct values
	def __init__(self, square, color):
		super().__init__(square, color, "♟" if color == "white" else "♙")
		self.row_comp_op = lambda x, y: (x >= y if self.color == "white" else x <= y)
		self.attacking_row_op = lambda x: (x - 1 if self.color == "white" else x + 1)
		self.enPassantSquare = None
		self.enPassantUsed = False

	def validateMove(self, newSquare):
		#max row difference
		maxRowDiff = 0
		if self.square[0] == 6 and self.color == "white" or self.square[0] == 1 and self.color == "black":
			maxRowDiff = 2
		else:
			maxRowDiff = 1

		#if new row is further than allowed
		if abs(self.square[0] - newSquare[0]) > maxRowDiff:
			return False
		
		#if new row is behind old row, or is equal to old row
		if self.row_comp_op(newSquare[0], self.square[0]):
			return False

		freeSquares = []
		diagonalMove = False
		#if moving forward, destination square needs to be free
		if self.square[1] == newSquare[1]:
			if abs(self.square[0] - newSquare[0]) == 2:
				freeSquares.append((newSquare[0] + 1, newSquare[1],) if self.color == "white" else (newSquare[0] - 1, newSquare[1],))
			freeSquares.append(newSquare)
		#if moving diagonally, destination square needs to contain enemy piece
		elif abs(self.square[1] - newSquare[1]) == 1:
			diagonalMove = True
		#illegal move (more than 1 column apart)
		else:
			return False

		#if en passant was used
		if diagonalMove and newSquare == self.enPassantSquare:
			#set diagonalMove to False to allow move, even though destination square contains no piece
			diagonalMove = False
			#mark the fact that this move was used
			self.enPassantUsed = True

		self.enPassantSquare = None

		return freeSquares, diagonalMove

	#boardRepr is not used here
	#but is required because attacks implements abstract method of Piece
	def attacks(self, boardRepr):
		attackedRow = self.attacking_row_op(self.square[0])
		return set(((attackedRow, self.square[1] - 1), (attackedRow, self.square[1] + 1)),)

	def setSquare(self, newSquare):
		self.square = newSquare

	#PUBLIC
	#returns set: squares pawn can move to, including by capture
	def moves(self, boardRepr):
		row = self.attacking_row_op(self.square[0])

		validFrontRow = row >= 0 and row <= 7
		if not validFrontRow:
			return []

		squares = set()

		if not boardRepr[row][self.square[1]]:
			squares.add((row, self.square[1],))

		if self.square[1] - 1 >= 0 and boardRepr[row][self.square[1] - 1]:
			squares.add((row, self.square[1] - 1,))

		if self.square[1] + 1 <= 7 and boardRepr[row][self.square[1] + 1]:
			squares.add((row, self.square[1] + 1,))

		return squares
		

	#PUBLIC
	#sets new en passant square for next move
	def addEnPassant(self, square):
		self.enPassantSquare = square
