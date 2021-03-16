from classes.Piece import Piece

class Knight(Piece):

	#assumes square and color are correct values
	def __init__(self, square, color):
		super().__init__(square, color, "♞" if color == "white" else "♘")
		self.opposite_diff_value = lambda x: 2 if abs(x) == 1 else 1 #get opposite value for row/column difference (if one is 2, other is 1, vice versa)
		self.row_difference_values = (-2, -1, 1, 2)

	def validateMove(self, newSquare):
		#calculate column and row difference
		rowDiff = abs(self.square[0] - newSquare[0])
		columnDiff = abs(self.square[1] - newSquare[1])

		if not (rowDiff == 2 and columnDiff == 1 or rowDiff == 1 and columnDiff == 2):
			return False

		return [], False

	#boardRepr is not used here
	#but is required because attacks implements abstract method of Piece
	def attacks(self, boardRepr):
		attackedSquares = set()

		#append all squares with an absolute row difference with current square of 2 and
		#an absolute column difference with current square of 1, and vice versa
		for val in self.row_difference_values:
			squares = ((self.square[0] + val, self.square[1] + self.opposite_diff_value(val)), 
				(self.square[0] + val, self.square[1] - self.opposite_diff_value(val)))

			for square in squares:
				valid = True
				for value in square:
					if value < 0 or value > 7:
						valid = False
						break
				if valid:
					attackedSquares.add(square)

		return attackedSquares

	def setSquare(self, newSquare):
		self.square = newSquare

