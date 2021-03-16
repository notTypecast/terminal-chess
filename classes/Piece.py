import abc
'''
Abstract class representing a chess piece
'''
class Piece(metaclass = abc.ABCMeta):
	
	#assumes passed square and color are correct values
	def __init__(self, square, color):
		self.square = square #tuple of board array indexes
		self.color = color #"white" or "black"

	#PUBLIC
	#accepts new square
	#returns:
	#tuple: (list: squares that need to be empty so move can be made, bool: whether destination needs to contain enemy piece), if move can be made
	#bool: False, if move cannot be made
	@abc.abstractmethod
	def validateMove(self, newSquare):
		pass

	#PUBLIC
	#accepts 2D array of boolean values
	#True represents corresponding square is occupied
	#False represents that it is free
	#returns set: squares that are under attack by this piece
	@abc.abstractmethod
	def attacks(self, boardRepr):
		pass


	#PUBLIC
	#accepts a square in index representation
	#sets that as the piece's new square
	#no return value
	@abc.abstractmethod
	def setSquare(self, newSquare):
		pass