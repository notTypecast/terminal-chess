class TableBuilder:

	def __init__(self):
		self.leftTopCorner = "╔"
		self.leftBottomCorner = "╚"
		self.rightTopCorner = "╗"
		self.rightBottomCorner = "╝"
		self.hSide = "═"
		self.hSideBottom = "╦"
		self.hSideTop = "╩"
		self.vSide = "║"
		self.vSideRight = "╠"
		self.vSideLeft = "╣"
		self.center = "╬"


	def _fixData(self, data):
		largestRowLength = len(max(data, key = len))

		for row in data:
			i = 0
			while i < len(row):
				if type(row[i]) != str:
					row[i] = str(row[i])

				i += 1

			while len(row) != largestRowLength:
				row.append("")

		return data


	#cellNums: tuple(bool, bool)
	#cellNums[0]: include cell numbers or not
	#cellNums[1]: reverse cell numbers or not
	def buildTable(self, data, extraCellSpace = 0, cellNums = (False, False)):
		data = self._fixData(data)

		totalColumns = len(data[0])
		if cellNums[0] and totalColumns > 24:
			return ""

		columnMaximum = 0

		column = 0
		while column < len(data[0]):
			row = 0
			columnMax = 0
			while row < len(data):
				if len(data[row][column]) > columnMax:
					columnMax = len(data[row][column])

				row += 1

			totalSpace = columnMax + extraCellSpace
			if totalSpace > columnMaximum:
				columnMaximum = totalSpace

			column += 1

		
		vSideIndexes = []
		for _ in range(len(data[0])):
			vSideIndexes.append(columnMaximum + 3) 

		topLine = self.leftTopCorner
		bottomLine = self.leftBottomCorner
		middleLine = self.vSideRight

		for index in vSideIndexes:
			indexSide = self.hSide * (index - 1)

			topLine += indexSide + self.hSideBottom
			bottomLine += indexSide + self.hSideTop
			middleLine += indexSide + self.center

		topLine = topLine[:-1] + self.rightTopCorner
		bottomLine = bottomLine[:-1] + self.rightBottomCorner
		middleLine = middleLine[:-1] + self.vSideLeft

		dataLines = []
		if cellNums[0]:
			columnLine = "  "
			currentColumn = 0

		for row in data:
			currItem = 0
			rowString = ""
			while currItem < len(row):
				padSpace = " " * ((vSideIndexes[currItem] - len(row[currItem])) // 2)
				toAdd = self.vSide + padSpace + row[currItem]
				rowString += toAdd + " " * (vSideIndexes[currItem] - len(toAdd))

				if cellNums[0] and currentColumn < totalColumns:
					toAdd = padSpace + " " + chr(65 + currentColumn)
					columnLine += toAdd + " " * (vSideIndexes[currItem] - len(toAdd))
					currentColumn += 1

				currItem += 1

			dataLines.append(rowString + self.vSide)

		table = ""
		if cellNums[0] and not cellNums[1]:
			table += columnLine + "\n"

		table += ("  " if cellNums[0] else "") + topLine + "\n"

		currDataLine = 0
		while currDataLine < len(dataLines):
			if cellNums[0]:
				table += str(len(dataLines) - currDataLine if cellNums[1] else currDataLine + 1) + " "

			table += dataLines[currDataLine] + "\n"
			if currDataLine != len(dataLines) - 1:
				table += ("  " if cellNums[0] else "") + middleLine + "\n"

			currDataLine += 1

		table += ("  " if cellNums[0] else "") + bottomLine

		if cellNums[0] and cellNums[1]:
			table += "\n" + columnLine


		return table