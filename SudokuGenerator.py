import numpy
import random
import copy
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

def generateCompletedGrid(sudokuGrid,recursionDepth,numberOrderGrid,disallowedValue,cellWhereValIsDisallowed):
	xPos=recursionDepth%9
	yPos=floor(recursionDepth/9)

	##print(recursionDepth)
	##print(xPos)
	##print(yPos)

	if sudokuGrid[xPos][yPos]!=0 and recursionDepth==80:
		return [True,sudokuGrid]
	elif sudokuGrid[xPos][yPos]!=0 and recursionDepth<80:
		return generateCompletedGrid(sudokuGrid,recursionDepth+1,numberOrderGrid,disallowedValue,cellWhereValIsDisallowed)
	

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

		##print(i)

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
		recurse=generateCompletedGrid(sudokuGrid,recursionDepth+1,numberOrderGrid,disallowedValue,cellWhereValIsDisallowed)
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

def createPuzzle(sudukoGrid,sumOfFilledSquares):

	print("current filled spaces="+str(sumOfFilledSquares))

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
		return createPuzzle(sudokuGrid,sumOfFilledSquares-1)

	for i in gridSpaceOrder:
		
		#print("try to remove space="+str(floor(i%9))+" "+str(floor(i/9))+" "+str(i))
		currentGridValue=int(sudokuGrid[floor(i%9)][floor(i/9)])

		sudokuGrid[floor(i%9)][floor(i/9)]=0

		#print("try to complete puzzle disallowing "+str(currentGridValue)+" in this spot")

		#print(sudokuGrid)
		sudokuGridCopy=copy.deepcopy(sudokuGrid)
		notUnique=generateCompletedGrid(sudokuGridCopy,0,randomiseNumberOrder(),currentGridValue,i)[0]
		#print(sudokuGrid)
		if notUnique:
			#print("no longer unique")
			sudokuGrid[floor(i%9)][floor(i/9)]=currentGridValue
			continue
		#print("no solution exists")
		#print("deleting "+str(i))	
		#print(sudokuGrid)
		return createPuzzle(sudokuGrid,sumOfFilledSquares-1)

	return sudokuGrid

	

boxIndex=[[0,2],[3,5],[6,8]]

sudokuGrid=numpy.zeros([9,9])
for i in range(0,100):
	solution=generateCompletedGrid(sudokuGrid,0,randomiseNumberOrder(),-1,-1)[1]
	print(solution)
	puzzle=createPuzzle(solution,81)
	f=open("puzzle"+str(i)+".txt","w")
	for j in range(0,len(puzzle)):
		for k in puzzle[j]:
			f.write(str(int(k))+",")
		f.write("\n")
	f.close()