from classes.Piece import Piece

class King(Piece):

	#assumes square and color are correct values
	def __init__(self, square, color):
		super().__init__(square, color)
		self.piece_chr = "♚" if self.color == "white" else "♔"
		self.difference_values = (-1, 0, 1)

		self.HASMOVED = False

	def __repr__(self):
		return self.piece_chr

	def validateMove(self, newSquare):
		#calculate column and row difference
		rowDiff = abs(self.square[0] - newSquare[0])
		columnDiff = abs(self.square[1] - newSquare[1])

		if rowDiff > 1 or columnDiff > 1:
			return False

		return [], False

	#boardRepr is not used here
	#but is required because attacks implements abstract method of Piece
	def attacks(self, boardRepr):
		attackedSquares = set()

		#get all valid row and column values
		#that king attacks
		row_values = []
		column_values = []
		for val in self.difference_values:
			rval = self.square[0] + val
			cval = self.square[1] + val

			if rval >= 0 and rval <= 7:
				row_values.append(rval)
			if cval >= 0 and cval <= 7:
				column_values.append(cval)

		#append all combinations of above row and column values
		for rval in row_values:
			for cval in column_values:
				if not (self.square[0] == rval and self.square[1] == cval):
						attackedSquares.add((rval, cval,))

		return attackedSquares

	def setSquare(self, newSquare):
		self.square = newSquare
		if not self.HASMOVED:
			self.HASMOVED = True

