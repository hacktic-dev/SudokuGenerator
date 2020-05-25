from numpy import zeros
import random
from math import floor

def randomiseNumberOrder():
	numberOrderGrid=zeros([9,9,9])
	for i in range(0,9):
		for j in range(0,9):
			numbersToSort=[1,2,3,4,5,6,7,8,9]
			for k in range(0,9):
				index=random.randint(0,len(numbersToSort)-1)
				numberOrderGrid[i][j][k]=numbersToSort[index]
				numbersToSort.pop(index)
	return numberOrderGrid

def generateCompletedGrid(sudokuGrid,recursionDepth,numberOrderGrid):
	xPos=recursionDepth%9
	yPos=floor(recursionDepth/9)

	#TODO tidy up this block of if elses
	if xPos<3:
		boxX=0
	elif xPos<6:
		boxX=1
	else:
		boxX=2

	if yPos<3:
		boxY=0
	elif yPos<6:
		boxY=1
	else:
		boxY=2

    
	
		
	#we try each number from 1-9 in random order and use the first one that is valid
	for i in range(0,9):
		#break out of nested loops
		try:
			currentTestNumber=numberOrderGrid[xPos][yPos][i]

			#test current row
			for j in range(0,9):
				if currentTestNumber==sudokuGrid[j][yPos]:
					#TODO break out of both loops
					raise Exception("break")

			#test current column
			for j in range(0,9):
				if currentTestNumber==sudokuGrid[xPos][j]:
					#TODO break out of both loops
					raise Exception("break")

			#test current box
			for j in range(boxIndex[boxX][0],boxIndex[boxX][1]+1):
				for k in range(boxIndex[boxY][0],boxIndex[boxY][1]+1):
					if currentTestNumber==sudokuGrid[j][k]:
						#break out of 3 loops
						raise Exception("break")
		except:
			continue

		#if we've passed all these, add number to grid
		sudokuGrid[xPos][yPos]=currentTestNumber
		#if we're at this depth we have filled the whole grid and so we return true
		if recursionDepth==80:
			return [True,sudokuGrid]
		#go down to next level to generate next cell
		recurse=generateCompletedGrid(sudokuGrid,recursionDepth+1,numberOrderGrid)
		#if its true then generateCompletedGrid has returned a complete grid so we return to the next level up
		if recurse[0]==True:
			return recurse
		#otherwise, it was not able to fill in the next cell, and so this cell created an impossible to complete grid,
		#and so we continue
		else:
			sudokuGrid[xPos][yPos]=0
			continue

	#if we can not fill the cell with any number, we return false in order to indicate we must change the previous cell
	return [False,sudokuGrid]

	
		

boxIndex=[[0,2],[3,5],[6,8]]

sudokuGrid=zeros([9,9])
final=generateCompletedGrid(sudokuGrid,0,randomiseNumberOrder())
print(final[1])