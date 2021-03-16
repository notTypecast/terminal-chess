from classes.Piece import Piece
from classes.Rook import Rook
from classes.Bishop import Bishop

class Queen(Piece):

	#assumes square and color are correct values
	def __init__(self, square, color):
		super().__init__(square, color, "♛" if color == "white" else "♕")
		self.internalBishop = Bishop(self.square, self.color)
		self.internalRook = Rook(self.square, self.color)

	def validateMove(self, newSquare):
		self._updateInternalPiecesSquare()

		#ask internal bishop if move is possible
		returnVal = self.internalBishop.validateMove(newSquare)

		#if move is impossible for a bishop, ask internal rook
		if not returnVal:
			returnVal = self.internalRook.validateMove(newSquare)

		return returnVal

	def attacks(self, boardRepr):
		self._updateInternalPiecesSquare() 

		attackedSquares = set()

		#attacked squares are the ones internal bishop attacks
		#and the ones internal rook attacks
		attackedSquares = attackedSquares.union(self.internalBishop.attacks(boardRepr))
		attackedSquares = attackedSquares.union(self.internalRook.attacks(boardRepr))

		return attackedSquares

	def setSquare(self, newSquare):
		self.square = newSquare

	#PRIVATE
	#updates the square of the internal pieces to current square
	#no return value
	def _updateInternalPiecesSquare(self):
		self.internalBishop.square = self.square
		self.internalRook.square = self.square