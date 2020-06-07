import numpy
import random
from multiprocessing.pool import ThreadPool as Pool
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

#search for solutions using traditional 'human viable' techniques.
# Each technique type is organised according the the classifications
# used in the paper 'A Scale to Measure the Difficulty of Sudoku Puzzles'
# by José Silva Coelho
def traditionalSearch(sudokuGridCopy,maxTechniqueDifficulty,disallowedValue,cellWhereValIsDisallowed):
	
	#green technique

	#grid of 'mentally marked' cells as in Coelho's paper. They are marked
	#when set to 1
	flag=True

	while flag:
		try:
			#print("currentGridState:")
			#print(sudokuGridCopy)
			for digit in range(1,10):
				
				#print("digit="+str(digit))

				mentalMarkGrid=numpy.zeros([9,9])
				fillMentalMarkGrid(sudokuGridCopy,mentalMarkGrid,digit)
				#print("mentalMarkGrid:")
				#print(mentalMarkGrid)
				cellsFilledFlag=fillLoneEmptyCells(sudokuGridCopy,mentalMarkGrid,digit,disallowedValue,cellWhereValIsDisallowed)
				if cellsFilledFlag:
					#print("cells filled")
					raise Exception("break")
			#print("nothing to fill")
			flag=False
		except:
			continue

def fillMentalMarkGrid(sudokuGridCopy,mentalMarkGrid,digit):

	for xPos in range(0,9):
		for yPos in range(0,9):
			if sudokuGridCopy[xPos][yPos]==digit:
				markRowColumnSubgrid(xPos,yPos,mentalMarkGrid)
			#we also mark all filled cells
			if sudokuGridCopy[xPos][yPos]!=0:
				mentalMarkGrid[xPos][yPos]=1

#fill all lone empty cells (cells that are the only cell in their
#row, column, or subgrid that are not mentally marked
def fillLoneEmptyCells(sudokuGridCopy,mentalMarkGrid,digit,disallowedValue,cellWhereValIsDisallowed):

	cellsFilledFlag=False

	#check rows
	for i in range(0,9):
		count=sum(mentalMarkGrid[i])
		if count==8:
			cellsFilledFlag=True
			for j in range(0,9):
				if mentalMarkGrid[i][j]==0:
					index=j
					break
			if not(digit==disallowedValue and cellWhereValIsDisallowed==(i*9+j)):
				sudokuGridCopy[i][index]=digit
	
	#columns
	for i in range(0,9):
		count=0
		for j in range(0,9):
			if mentalMarkGrid[j][i]==1:
				count+=1
		if count==8:
			cellsFilledFlag=True
			for j in range(0,9):
				if mentalMarkGrid[j][i]==0:
					index=j
					break
			if not(digit==disallowedValue and cellWhereValIsDisallowed==(i*9+j)):
				sudokuGridCopy[index][i]=digit

	#boxes TODO
	return cellsFilledFlag

#mark the row column and subgrid of (xPos,yPos) in the mentalMarkGrid
def markRowColumnSubgrid(xPos,yPos,mentalMarkGrid):

	#mark row and column
	for i in range(0,9):
		mentalMarkGrid[xPos][i]=1
		mentalMarkGrid[i][yPos]=1

	#get indices of sub grid
	subgridIndex=[[0,2],[3,5],[6,8]]
	subgridX=0
	subgridY=0
	#getSubgrid(xPos,yPos,subgridX,subgridY)

	if xPos<3:
		subgridX=0
	elif xPos<6:
		subgridX=1
	else:
		subgridX=2

	if yPos<3:
		subgridY=0
	elif yPos<6:
		subgridY=1
	else:
		subgridY=2

	#mark subgrid
	for i in range(subgridIndex[subgridX][0],subgridIndex[subgridX][1]+1):
		for j in range(subgridIndex[subgridY][0],subgridIndex[subgridY][1]+1):
			mentalMarkGrid[i][j]=1



#def getSubgrid(xPos,yPos,subgridX,subgridY):
	

def createSolution():
	sudokuGrid=numpy.zeros([9,9])
	return sequentialBacktrackingMethod(sudokuGrid,0,randomiseNumberOrder(),-1,-1)

def searchForSolution(sudokuGridCopy,numberOrder,disallowedValue,cellWhereValIsDisallowed):
	#traditionalSearch(sudokuGridCopy,0,disallowedValue,cellWhereValIsDisallowed)
	return sequentialBacktrackingMethod(sudokuGridCopy,0,numberOrder,disallowedValue,cellWhereValIsDisallowed)

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

def createPuzzle(sudokuGrid,sumOfFilledSquares,numberOrder):

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

		sudokuGridCopy=copy.deepcopy(sudokuGrid)

		sudokuGridCopy[floor(currentGridSpace%9)][floor(currentGridSpace/9)]=0

		notUnique=searchForSolution(sudokuGridCopy,numberOrder,currentGridValue,currentGridSpace)[0]

		if notUnique:

			continue

		sudokuGrid[floor(currentGridSpace%9)][floor(currentGridSpace/9)]=0

		return createPuzzle(sudokuGrid,sumOfFilledSquares-1,numberOrder)

	return sudokuGrid

	

def createAndSavePuzzles(numberOfPuzzles,threadNo):
	totalTime=0
	for i in range(0,numberOfPuzzles):
		solution=createSolution()[1]
	
		print(solution)

		start=time.time()
		puzzle=createPuzzle(solution,81,randomiseNumberOrder())
		end=time.time()
		timeTaken=end-start
		totalTime+=timeTaken
		f=open("puzzles/puzzle"+str(i*threadNo)+".txt","w")
		for j in range(0,len(puzzle)):
			for k in puzzle[j]:
				f.write(str(int(k))+",")
			f.write("\n")
		f.close()


boxIndex=[[0,2],[3,5],[6,8]]
max=50

pool_size = 4

pool = Pool(pool_size)

for i in range(0,pool_size):
	pool.apply_async(createAndSavePuzzles, (max,i))

pool.close()