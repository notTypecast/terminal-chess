from classes.Piece import Piece
from classes.Pawn import Pawn
from classes.Rook import Rook
from classes.Knight import Knight
from classes.Bishop import Bishop
from classes.Queen import Queen
from classes.King import King
from classes.TableBuilder import TableBuilder
from classes.InvalidSquareException import InvalidSquareException

'''
Initializes a new board object
'''
class Board:

	def __init__(self):
		self.tb = TableBuilder()
		self._initBoardArr()
		self._initBoardBoolRepr()
		self.LASTPLAYERCOLOR = None
		self.MOVES = 0
		self.ENPASSANTSQUARE = None
		self.ENPASSANTMOVENUM = None

		self.STALEMATE = False
		self.CHECKMATE = False

		self.PROMOTIONDICT = {
			"Q": Queen,
			"B": Bishop,
			"N": Knight,
			"R": Rook
		}

	#PUBLIC
	#makes a move from square1 to square2
	#currentPlayerColor: color of player who made move
	#revertMove: bool, False by default; if True, move will not be made, but
	# 	False or True will still be returned depending on whether move was valid
	#returns bool: whether move was made
	#can raise InvalidSquareException if squares are invalid
	def makeMove(self, square1, square2, currPlayerColor, promotionTo = None, revertMove = False):

		if self.STALEMATE or self.CHECKMATE:
			return False

		if type(square1) is str:
			square1 = square1.upper()
		elif type(square1) is tuple:
			try:
				square1 = Board._convertToSquareNotation(square1)
			except:
				raise InvalidSquareException

		if type(square2) is str:
			square2 = square2.upper()
		elif type(square2) is tuple:
			try:
				square2 = Board._convertToSquareNotation(square2)
			except:
				raise InvalidSquareException

		if not (Board._validateSquare(square1) and Board._validateSquare(square2)):
			raise InvalidSquareException

		#convert squares passed to board_arr tuples
		s1, s2 = Board._convertSquare(square1.lower()), Board._convertSquare(square2.lower())

		if s1 == s2:
			return False
		
		pieceToMove = self.board_arr[s1[0]][s1[1]]

		#if there is no allied piece in that square
		if pieceToMove == "" or pieceToMove.color != currPlayerColor:
			return False

		enemyPlayerColor = "black" if currPlayerColor == "white" else "white"

		#if there is potential en passant and piece is pawn, set en passant square
		if type(pieceToMove) is Pawn and self.ENPASSANTSQUARE:
			pieceToMove.addEnPassant(self.ENPASSANTSQUARE)
		#check for castling
		elif type(pieceToMove) is King and s1[0] == s2[0] and abs(s1[1] - s2[1]) == 2:
			#make sure king hasn't moved before
			if pieceToMove.HASMOVED:
				return False

			#get rook
			kingsideCastle = s1[1] < s2[1]
			castlingRook = self.board_arr[pieceToMove.square[0]][7 if kingsideCastle else 0]

			#make sure rook is in intended position and has not moved before
			if type(castlingRook) is not Rook or castlingRook.HASMOVED:
				return False

			#get squares between king and rook
			squaresInBetween = Board._getSquaresBetween(pieceToMove.square, castlingRook.square)

			#determine if those squares are free
			for square in squaresInBetween:
				if self.bool_board[square[0]][square[1]]:
					return False

			#determine which squares enemy attacks
			enemyAttacks = self._getAttackingDict(enemyPlayerColor)[0]
			squaresAttackedByEnemy = [square for pieceSquares in enemyAttacks.values() for square in pieceSquares]

			#determine if any of the squares king passes through are attacked by enemy
			kingMoveSquares = Board._getSquaresBetween(s1, s2)
			#include s1 and s2 in those, because king can't castle if he is in check before or after move
			kingMoveSquares.union(set((s1, s2,)))

			#if any of those squares are attacked, castling isn't allowed
			for square in kingMoveSquares:
				if square in squaresAttackedByEnemy:
					return False

			if revertMove:
				return True

			newRookSquare = pieceToMove.square[0], s2[1] - 1 if kingsideCastle else s2[1] + 1

			#move pieces on board
			self.board_arr[s1[0]][s1[1]] = ""
			self.bool_board[s1[0]][s1[1]] = False

			self.board_arr[s2[0]][s2[1]] = pieceToMove
			self.bool_board[s2[0]][s2[1]] = True

			self.board_arr[castlingRook.square[0]][castlingRook.square[1]] = ""
			self.bool_board[castlingRook.square[0]][castlingRook.square[1]] = False

			self.board_arr[newRookSquare[0]][newRookSquare[1]] = castlingRook
			self.bool_board[newRookSquare[0]][newRookSquare[1]] = True

			#change piece squares
			pieceToMove.setSquare(s2)
			castlingRook.setSquare(newRookSquare)

			#here, enemyAttacks is not passed to _finishMove
			#this is because it was created before move was made
			#it needs to be recreated (will be done by below function)
			self._finishMove(currPlayerColor)

			return True

		#validate move based on piece's movement
		squareValidation = pieceToMove.validateMove(s2)
		
		#illegal move for chosen piece
		if not squareValidation:
			return False

		#mark potential en passant if pawn moved two spaces
		if type(pieceToMove) is Pawn and abs(s1[0] - s2[0]) == 2:
			self.ENPASSANTSQUARE = (s2[0] + 1 if currPlayerColor == "white" else s2[0] - 1, s2[1])
			self.ENPASSANTMOVENUM = self.MOVES
		
		#check if all squares between original square and destination are empty
		for square in squareValidation[0]:
			if self.board_arr[square[0]][square[1]] != "":
				return False

		#check if destination square is occupied by allied piece
		destinationPiece = self.board_arr[s2[0]][s2[1]]
		if destinationPiece != "" and destinationPiece.color == currPlayerColor:
			return False

		#for pawns; disallow diagonal move if there is no enemy piece to take
		if squareValidation[1] and self.board_arr[s2[0]][s2[1]] == "":
			return False

		#for pawns moving to final row
		promotionNeeded = False
		promotionClass = None
		if type(pieceToMove) is Pawn:
			finalRowIndex = 0 if currPlayerColor == "white" else 7
			if type(promotionTo) is str:
				promotionTo = promotionTo.upper()
			#if pawn is moving to final row
			if s2[0] == finalRowIndex:
				promotionNeeded = True
				if promotionTo in ("Q", "B", "N", "R"):
					promotionClass = self.PROMOTIONDICT[promotionTo]

		#change boolean board array's values to those it will have after move is performed
		#in order to check whether king is attacked after this move
		enPassantUsed = False
		if type(pieceToMove) is Pawn:
			enPassantUsed = pieceToMove.enPassantUsed

		if enPassantUsed:
			capturedPawnRow = s2[0] + 1 if currPlayerColor == "white" else s2[0] - 1
			self.bool_board[capturedPawnRow][s2[1]] = False

		self.bool_board[s2[0]][s2[1]] = True
		self.bool_board[s1[0]][s1[1]] = False

		#keep these in case move must be reverted
		sourceSquarePiece = self.board_arr[s1[0]][s1[1]]
		destSquarePiece = self.board_arr[s2[0]][s2[1]]

		#move piece to new square
		self.board_arr[s2[0]][s2[1]] = self.board_arr[s1[0]][s1[1]] if not promotionClass else promotionClass(s2, currPlayerColor)
		self.board_arr[s1[0]][s1[1]] = ""

		#if en passant was used, remove taken pawn from board
		if enPassantUsed:
			#keep captured pawn in case move must be reverted
			capturedPawn = self.board_arr[capturedPawnRow][s2[1]]
			self.board_arr[capturedPawnRow][s2[1]] = ""
			pieceToMove.enPassantUsed = False

		#keys: enemy pieces, values: squares corresponding piece attacks
		enemyAttacks, alliedKing = self._getAttackingDict(enemyPlayerColor)

		squaresAttackedByEnemy = [square for pieceSquares in enemyAttacks.values() for square in pieceSquares]

		#if allied king is attacked after move, move is not allowed
		#this includes the possibility that allied king was attacked before move was made and still is
		kingAttacked = (alliedKing.square if type(pieceToMove) is not King else s2) in squaresAttackedByEnemy

		#revert the move if:
		#	1) King attacked after move, so it is illegal
		#	2) revertMove was True
		#	3) promotion is needed, but incorrect/no promotion class was specified
		invalidPromotion = promotionNeeded and not promotionClass
		if kingAttacked or revertMove or invalidPromotion:
			#move illegal

			#revert boolean board back to previous state
			self.bool_board[s2[0]][s2[1]] = False
			self.bool_board[s1[0]][s1[1]] = True

			#revert regular board array back to previous state
			self.board_arr[s1[0]][s1[1]] = sourceSquarePiece
			self.board_arr[s2[0]][s2[1]] = destSquarePiece

			#revert en passant if used
			if enPassantUsed:
				self.bool_board[capturedPawnRow][s2[1]] = True
				self.board_arr[capturedPawnRow][s2[1]] = capturedPawn

			return not (invalidPromotion or kingAttacked)
			

		#remove ability for en passant if it was not used
		if self.ENPASSANTSQUARE and self.ENPASSANTMOVENUM != self.MOVES:
			self.ENPASSANTSQUARE = None
			self.ENPASSANTMOVENUM = None

		#assign new square to moved piece
		pieceToMove.setSquare(s2)

		self._finishMove(currPlayerColor, enemyAttacks)

		return True

	#PRIVATE
	#checks for checkmate or stalemate
	#method is called after every move, so color of (potential) winning
	#currPlayerColor: color of player who made the last move
	#enemyAttacks: dictionary with keys: enemy pieces and values: set of squares corresponding pieces attack
	#	this dictionary is created in the makeMove function and should be passed to this one as-is
	#updates the object's STALEMATE or CHECKMATE flags
	#no return value
	def _checkForMate(self, currPlayerColor, enemyAttacks):
		#get squares current player attacks and enemy king
		allyAttacks, enemyKing = self._getAttackingDict(currPlayerColor)

		#get amount of pieces that attack enemy king
		totalChecks = 0

		for piece in allyAttacks:
			for square in allyAttacks[piece]:
				if square == enemyKing.square:
					totalChecks += 1

		enemyPlayerColor = "black" if currPlayerColor == "white" else "white"

		#if there is no check
		if not totalChecks:

			#determine if there is an available move
			availableMove = False
			for enemyPiece in enemyAttacks:
				#for pawns, get squares they can move to
				#and make move to determine if it is legal
				if type(enemyPiece) is Pawn:
					availableSquares = enemyPiece.moves(self.bool_board)
					for square in availableSquares:
						if self.makeMove(enemyPiece.square, square, enemyPlayerColor, revertMove = True):
							availableMove = True
							break
				#for other pieces, look for moves in their attacking squares and try them
				#if they are legal, there is an available move
				else:
					for square in enemyAttacks[enemyPiece]:
						piece = self.board_arr[square[0]][square[1]]
						if not piece or piece.color == currPlayerColor:
							if self.makeMove(enemyPiece.square, square, enemyPlayerColor, revertMove = True):
								availableMove = True
								break

			#if there is no available move, it's a stalemate
			#else, available move was found
			if not availableMove:
				self.STALEMATE = True

			return

		#determine if there is an available square to move to
		#get squares around king
		potentialSquares = enemyAttacks[enemyKing]

		#check if there is free, non-attacked square
		moveExists = False
		for square in potentialSquares:
			if not self.bool_board[square[0]][square[1]]:
				squareIsAttacked = False
				for piece in allyAttacks:
					for attackedSquare in allyAttacks[piece]:
						if attackedSquare == square:
							squareIsAttacked = True
							break
					if squareIsAttacked:
						break

				if not squareIsAttacked:
					moveExists = True
					break

		#if king has available move
		if moveExists:
			return

		#king has no available move
		#if more than one piece attacks king, it's checkmate
		if totalChecks > 1:
			self.CHECKMATE = True
			return

		#if a single piece attacks king, that piece has to be captured (1)
		#or attack must be blocked (2)

		#determine which piece attacks king
		attackingPiece = None
		for piece in allyAttacks:
			if enemyKing.square in allyAttacks[piece]:
				attackingPiece = piece
				break

		#(1)
		#determine which enemy pieces attack attacking piece
		enemyPieces = []
		for piece in enemyAttacks:
			if attackingPiece.square in enemyAttacks[piece]:
				enemyPieces.append(piece)

		#for each enemy piece attacking ally piece, try to capture
		#if capture is legal, there is available move for enemy player
		for piece in enemyPieces:
			if self.makeMove(piece.square, attackingPiece.square, enemyPlayerColor, revertMove = True):
				return

		#no captures available, so move must be blocked

		#(2)

		#list of squares that enemy needs to occupy to block attack
		squaresToOccupy = Board._getSquaresBetween(attackingPiece.square, enemyKing.square)

		#if some square exists that can block the attack
		if squaresToOccupy:
			#determine which enemy pieces can occupy one of those squares
			for enemyPiece in enemyAttacks:
				#for pawns, get actual squares that they can move to
				#instead of squares they attack
				if type(enemyPiece) is Pawn:
					pawnSquares = set(enemyPiece.moves(self.bool_board))

					#check whether a move to one of the squares necessary is possible
					for destSquare in squaresToOccupy.intersection(pawnSquares):
						#if move is possible, then legal move exists, game continues
						if self.makeMove(enemyPiece.square, destSquare, enemyPlayerColor, revertMove = True):
							return
				#for other pieces, attacking squares are the same as squares they can move to
				elif type(enemyPiece) is not King:
					#similarly to pawns above
					for destSquare in squaresToOccupy.intersection(enemyAttacks[enemyPiece]):
						if self.makeMove(enemyPiece.square, destSquare, enemyPlayerColor, revertMove = True):
							return

		#if this point is reached, no move was able to block the attack, so current player wins
		self.CHECKMATE = True

	#PRIVATE
	#makes necessary changes after move has been made
	#if enemyAttacks is not passed, dictionary will be created by this function instead
	#no return value
	def _finishMove(self, currPlayerColor, enemyAttacks = None):
		#update board string after move was made
		self._updateBoardRepr()

		#add move to counter
		self.MOVES += 1
		
		if not enemyAttacks:
			enemyAttacks = self._getAttackingDict("black" if currPlayerColor == "white" else "black")[0]

		#check for mate
		self._checkForMate(currPlayerColor, enemyAttacks)

		#set last player color as current player's color
		self.LASTPLAYERCOLOR = currPlayerColor


	#PRIVATE STATIC
	#validates whether a passed string is a valid square
	#returns bool: whether square is valid
	def _validateSquare(square):
		if len(square) != 2 or type(square) != str:
			return False
		return ord(square[0]) in range(65, 73) and ord(square[1]) in range(49, 57)

	#PRIVATE STATIC
	#convert square (e.g a1) to corresponding board array indexes
	#assumes square is in correct format (lowercase letter a-h, integer 1-8)
	#returns tuple: (row, column)
	def _convertSquare(square):
		return 8 - int(square[1]), ord(square[0]) - 97

	#PRIVATE STATIC
	#convert board array indexes to square
	#opposite to _convertSquare
	#returns string: square
	def _convertToSquareNotation(squareIndexes):
		return chr(65 + squareIndexes[1]) + str(8 - squareIndexes[0])


	#PRIVATE STATIC
	#get squares in between two given squares
	#squares must either be in same row, same column, or same diagonal
	#or output list will be empty
	#passed squares must be in board array index format, e.g (2, 5)
	#returns set: squares in between passed squares
	def _getSquaresBetween(square1, square2):
		squaresInBetween = set()
		#if row is the same
		if square1[0] == square2[0]:
			for column in range(min(square1[1], square2[1]) + 1, max(square1[1], square2[1])):
				squaresInBetween.add((square1[0], column,))
		#if column is the same
		elif square1[1] == square2[1]:
			for row in range(min(square1[0], square2[0]) + 1, max(square1[0], square2[0])):
				squaresInBetween.add((row, square1[1]))
		#if diagonal is the same
		elif abs(square1[0] - square2[0]) == abs(square1[1] - square2[1]):
			row_op = lambda x: (x + 1 if square1[0] < square2[0] else x - 1)
			column_op = lambda x: (x + 1 if square1[1] < square2[1] else x - 1)

			currentSquare = row_op(square1[0]), column_op(square1[1])

			while currentSquare != square2:
				squaresInBetween.add(currentSquare)
				currentSquare = row_op(currentSquare[0]), column_op(currentSquare[1])

		return squaresInBetween

	#PRIVATE
	#get attacking dictionary for player
	#playerColor: color of player whose pieces will be in dictionary
	#returns tuple: 
	#	(dict with keys: enemy pieces, values: squares corresponding piece (key) attacks, enemy king)
	def _getAttackingDict(self, playerColor):
		attacks = {}
		enemyKing = None

		for row in self.board_arr:
			for piece in row:
				if piece:
					if piece.color == playerColor:
						attacks[piece] = piece.attacks(self.bool_board)
					elif type(piece) is King:
						enemyKing = piece

		return attacks, enemyKing


	#PRIVATE
	#initializes self.board_arr and fills it with pieces in starting positions
	#no return value
	def _initBoardArr(self):
		self.board_arr = [[] for _ in range(8)]

		lowerRow = (Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook)

		i = 0
		while i < 8:
			self.board_arr[0].append(lowerRow[i]((0, i,), "black"))
			self.board_arr[1].append(Pawn((1, i,), "black"))
			self.board_arr[7].append(lowerRow[i]((7, i,), "white"))
			self.board_arr[6].append(Pawn((6, i,), "white"))
			for j in range(2, 6):
				self.board_arr[j].append("")
			i += 1
		"""
		#TEMPCODESTART#
		i = 0
		while i < 8:
			self.board_arr[i][4] = ""
			i += 1

		#TEMPCODEEND
		"""
		self._updateBoardRepr()


	#PRIVATE
	#initializes array: boolean representation of board
	#no return value
	def _initBoardBoolRepr(self):
		self.bool_board = []

		i = 0
		while i < 8:
			if i < 2 or i > 5:
				self.bool_board.append([True] * 8)
			else:
				self.bool_board.append([False] * 8)

			i += 1


	#PRIVATE
	#updates the board representation string
	#must be called after a move has been made
	#no return value
	def _updateBoardRepr(self):
		#deep copy inner lists of board_arr, but shallow copy Piece objects
		#deepcopy(self.board_arr) would also deepcopy Piece objects, unnecessary!
		data = []
		for row in self.board_arr:
			data.append([x for x in row])

		self.BOARD_REPR = self.tb.buildTable(data, extraCellSpace = 2, cellNums = (True, True))


	def __repr__(self):
		return self.BOARD_REPR


