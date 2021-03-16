class InvalidSquareException(Exception):
	def __init__(self):
		super().__init__("Given square format is invalid!")