import numpy
import random
import copy
import time
from math import floor

def randomiseNumberOrder():
	numberOrderGrid=numpy.zeros([9,9,9])
	for i in range(0,9):
		for j in range(0,9):
			numbersToSort=[1,2,3,4,5,6,7,8,9]
			for k in range(0,9):
				index=random.randint(0,len(numbersToSort)-1)
				numberOrderGrid[i][j][k]=numbersToSort[index]
				numbersToSort.pop(index)
	return numberOrderGrid

def createSolution():
	return sequentialBacktrackingMethod(sudokuGrid,0,randomiseNumberOrder(),-1,-1)

def searchForSolution(sudokuGridCopy,numberOrder,currentGridValue,i):
	return sequentialBacktrackingMethod(sudokuGridCopy,0,numberOrder,currentGridValue,i)

def sequentialBacktrackingMethod(sudokuGrid,recursionDepth,numberOrderGrid,disallowedValue,cellWhereValIsDisallowed):
	xPos=recursionDepth%9
	yPos=floor(recursionDepth/9)


	if sudokuGrid[xPos][yPos]!=0 and recursionDepth==80:
		return [True,sudokuGrid]
	elif sudokuGrid[xPos][yPos]!=0 and recursionDepth<80:
		return sequentialBacktrackingMethod(sudokuGrid,recursionDepth+1,numberOrderGrid,disallowedValue,cellWhereValIsDisallowed)
	

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

		#dont try filling it with the disallowed value
		if recursionDepth==cellWhereValIsDisallowed and disallowedValue==numberOrderGrid[xPos][yPos][i]:
			continue

		#break out of nested loops
		try:
			currentTestNumber=int(numberOrderGrid[xPos][yPos][i])

			#test current row
			for j in range(0,9):
				if currentTestNumber==sudokuGrid[j][yPos]:
					#break out of both loops
					raise Exception("break")

			#test current column
			for j in range(0,9):
				if currentTestNumber==sudokuGrid[xPos][j]:
					#break out of both loops
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
		recurse=sequentialBacktrackingMethod(sudokuGrid,recursionDepth+1,numberOrderGrid,disallowedValue,cellWhereValIsDisallowed)
		#if its true then sequentialBacktrackingMethod has returned a complete grid so we return to the next level up
		if recurse[0]==True:
			return recurse
		#otherwise, it was not able to fill in the next cell, and so this cell created an impossible to complete grid,
		#and so we continue
		else:
			sudokuGrid[xPos][yPos]=0
			continue

	#if we can not fill the cell with any number, we return false in order to indicate we must change the previous cell
	return [False,sudokuGrid]

def createPuzzle(sudukoGrid,sumOfFilledSquares,numberOrder):

	print("current filled spaces="+str(sumOfFilledSquares))

	if sumOfFilledSquares<30:
		return sudokuGrid


	gridSpaces=numpy.zeros(81)

	for i in range(0,81):
		gridSpaces[i]=i
	
	gridSpaceOrder=[]

	while len(gridSpaces)>0:
		index=random.randint(0,len(gridSpaces)-1)
		if (sudokuGrid[index%9][floor(index/9)]!=0):
			gridSpaceOrder.append(gridSpaces[index])
		gridSpaces=numpy.delete(gridSpaces,index)

	if sumOfFilledSquares==81:
		sudokuGrid[floor(gridSpaceOrder[0]%9)][floor(gridSpaceOrder[0]/9)]=0
		return createPuzzle(sudokuGrid,sumOfFilledSquares-1,numberOrder)

	for currentGridSpace in gridSpaceOrder:
		
		currentGridValue=int(sudokuGrid[floor(currentGridSpace%9)][floor(currentGridSpace/9)])

		sudokuGrid[floor(currentGridSpace%9)][floor(currentGridSpace/9)]=0

		sudokuGridCopy=copy.deepcopy(sudokuGrid)

		notUnique=searchForSolution(sudokuGridCopy,numberOrder,currentGridValue,currentGridSpace)[0]

		if notUnique:

			sudokuGrid[floor(i%9)][floor(i/9)]=currentGridValue
			continue

		return createPuzzle(sudokuGrid,sumOfFilledSquares-1,numberOrder)

	return sudokuGrid

	

boxIndex=[[0,2],[3,5],[6,8]]

sudokuGrid=numpy.zeros([9,9])
for i in range(0,1):
	solution=createSolution()[1]

	print(solution)

	start=time.time()
	puzzle=createPuzzle(solution,81,randomiseNumberOrder())
	end=time.time()
	print(end-start)

	f=open("puzzles/puzzle"+str(i)+".txt","w")
	for j in range(0,len(puzzle)):
		for k in puzzle[j]:
			f.write(str(int(k))+",")
		f.write("\n")
	f.close()