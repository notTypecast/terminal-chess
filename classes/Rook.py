from classes.Piece import Piece

class Rook(Piece):

	#assumes square and color are correct values
	def __init__(self, square, color):
		super().__init__(square, color, "♜" if color == "white" else "♖")

		self.HASMOVED = False

	def validateMove(self, newSquare):
		#ensure either column, or row is same, but not both
		if not ((self.square[0] == newSquare[0]) ^ (self.square[1] == newSquare[1])):
			return False

		freeSquares = []
		sameRow = self.square[0] == newSquare[0]
		if sameRow:
			varIndex = 1
		else:
			varIndex = 0


		if self.square[varIndex] > newSquare[varIndex]:
			newSquareIndexRange = range(newSquare[varIndex] + 1, self.square[varIndex])
		else:
			newSquareIndexRange = range(self.square[varIndex] + 1, newSquare[varIndex])
		
		if varIndex:
			for c in newSquareIndexRange:
				freeSquares.append((self.square[0], c))
		else:
			for c in newSquareIndexRange:
				freeSquares.append((c, self.square[1]))

		return freeSquares, False

	def attacks(self, boardRepr):
		attackedSquares = set()

		#add attacked squares above piece
		currentSquare = self.square[0] - 1, self.square[1]
		while currentSquare[0] >= 0:
			attackedSquares.add(currentSquare)
			#stop if current square contains piece
			if boardRepr[currentSquare[0]][currentSquare[1]]:
				break

			currentSquare = currentSquare[0] - 1, currentSquare[1]

		#add attacked squares below piece
		currentSquare = self.square[0] + 1, self.square[1]
		while currentSquare[0] <= 7:
			attackedSquares.add(currentSquare)
			if boardRepr[currentSquare[0]][currentSquare[1]]:
				break

			currentSquare = currentSquare[0] + 1, currentSquare[1]

		#add attacked squares to the right of piece
		currentSquare = self.square[0], self.square[1] + 1
		while currentSquare[1] <= 7:
			attackedSquares.add(currentSquare)
			if boardRepr[currentSquare[0]][currentSquare[1]]:
				break

			currentSquare = currentSquare[0], currentSquare[1] + 1

		#add attacked squares to the left of piece
		currentSquare = self.square[0], self.square[1] - 1
		while currentSquare[1] >= 0:
			attackedSquares.add(currentSquare)
			if boardRepr[currentSquare[0]][currentSquare[1]]:
				break

			currentSquare = currentSquare[0], currentSquare[1] - 1

		return attackedSquares

	def setSquare(self, newSquare):
		self.square = newSquare
		if not self.HASMOVED:
			self.HASMOVED = True