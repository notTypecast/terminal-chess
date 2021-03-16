from classes.Piece import Piece

class Bishop(Piece):

	#assumes square and color are correct values
	def __init__(self, square, color):
		super().__init__(square, color)
		self.piece_chr = "♝" if self.color == "white" else "♗"
		self.INCR = lambda x: x+1
		self.DECR = lambda x: x-1

	def __repr__(self):
		return self.piece_chr

	def validateMove(self, newSquare):
		#calculate column and row difference
		rowDiff = self.square[0] - newSquare[0]
		columnDiff = self.square[1] - newSquare[1]

		if (abs(columnDiff) != abs(rowDiff)):
			return False

		#moving upwards
		if rowDiff > 0:
			rowOperation = self.DECR
		#moving downwards
		else:
			rowOperation = self.INCR

		#moving left
		if columnDiff > 0:
			columnOperation = self.DECR
		#moving right
		else:
			columnOperation = self.INCR

		freeSquares = []
		#add all diagonal squares between initial and destination square to freeSquares
		currSquare = rowOperation(self.square[0]), columnOperation(self.square[1])
		while currSquare != newSquare:
			freeSquares.append(currSquare)
			currSquare = rowOperation(currSquare[0]), columnOperation(currSquare[1])

		return freeSquares, False

	def attacks(self, boardRepr):
		attackedSquares = set()

		#add attacked squares to the top right of piece
		currentSquare = self.square[0] - 1, self.square[1] + 1
		while currentSquare[0] >= 0 and currentSquare[1] <= 7:
			attackedSquares.add(currentSquare)
			#stop if current square contains piece
			if boardRepr[currentSquare[0]][currentSquare[1]]:
				break

			currentSquare = currentSquare[0] - 1, currentSquare[1] + 1

		#add attacked squares to the top left of piece
		currentSquare = self.square[0] - 1, self.square[1] - 1
		while currentSquare[0] >= 0 and currentSquare[1] >= 0:
			attackedSquares.add(currentSquare)
			if boardRepr[currentSquare[0]][currentSquare[1]]:
				break

			currentSquare = currentSquare[0] - 1, currentSquare[1] - 1

		#add attacked squares to the bottom right of piece
		currentSquare = self.square[0] + 1, self.square[1] + 1
		while currentSquare[0] <= 7 and currentSquare[1] <= 7:
			attackedSquares.add(currentSquare)
			if boardRepr[currentSquare[0]][currentSquare[1]]:
				break

			currentSquare = currentSquare[0] + 1, currentSquare[1] + 1

		#add attacked squares to the bottom left of piece
		currentSquare = self.square[0] + 1, self.square[1] - 1
		while currentSquare[0] <= 7 and currentSquare[1] >= 0:
			attackedSquares.add(currentSquare)
			if boardRepr[currentSquare[0]][currentSquare[1]]:
				break

			currentSquare = currentSquare[0] + 1, currentSquare[1] - 1

		return attackedSquares

	def setSquare(self, newSquare):
		self.square = newSquare

