#include <vector>
#include <random>
#include <iostream>
#include <chrono>
#include <string>
void print2DVector(std::vector<std::vector<int>> Vec2d)
{
	for (int i = 0; i < Vec2d.size(); i++)
	{
		for (int j = 0; j < Vec2d[0].size(); j++)
		{
			std::cout << Vec2d[i][j] << " ";
		}
		std::cout << std::endl;
	}
	std::cout << std::endl;
}

struct coord
{
	coord(int xPos, int yPos) : xPos(xPos), yPos(yPos) {}
	int xPos;
	int yPos;
};

struct gridWithSolveableBool
{
	gridWithSolveableBool(bool solvable, std::vector < std::vector<int>> grid) : solvable(solvable), grid(grid) {}

	bool solvable;
	std::vector < std::vector<int>> grid;
};

struct gridWithUniqueness
{
	gridWithUniqueness(std::vector < std::vector<int>> grid, int uniqueness) : grid(grid), uniqueness(uniqueness) {}

	std::vector < std::vector<int>> grid;
	int uniqueness;
};

coord getSubgrid(int xPos, int yPos)
{
	int subgridX;
	int	subgridY;


	if (xPos < 3)
	{
		subgridX = 0;
	}
	else if (xPos < 6)
	{
		subgridX = 1;
	}
	else
	{
		subgridX = 2;
	}
	if (yPos < 3)
	{
		subgridY = 0;
	}
	else if (yPos < 6)
	{
		subgridY = 1;
	}
	else
	{
		subgridY = 2;
	}
	return coord(subgridX, subgridY);

}

gridWithSolveableBool sequentialBacktrackingMethod(std::vector<std::vector<int>>& sudokuGrid,
	int recursionDepth, std::vector<std::vector<std::vector<int>>> &numberOrderGrid,int disallowedValue,int cellWhereValIsDisallowed)
{

	int xPos = recursionDepth % 9;
	int yPos = floor(recursionDepth / 9);

	if (sudokuGrid[xPos][yPos] != 0 && recursionDepth == 80)
	{
		return gridWithSolveableBool(true, sudokuGrid);
	}
	else if (sudokuGrid[xPos][yPos] != 0 && recursionDepth < 80)
	{
		return sequentialBacktrackingMethod(sudokuGrid, recursionDepth + 1, numberOrderGrid, disallowedValue, cellWhereValIsDisallowed);
	}

	//for each digit in a random order according to numberOrderGrid
	for (int i = 0; i < 9; i++)
	{

		if (recursionDepth == cellWhereValIsDisallowed and disallowedValue == numberOrderGrid[xPos][yPos][i])
		{
			continue;
		}

		int currentTestNumber = numberOrderGrid[xPos][yPos][i];

		std::vector<std::vector<int>> subgridIndex = { {0, 2},{3, 5},{6, 8} };
		coord subgrid = getSubgrid(xPos, yPos);

		try
		{
			//test row
			for (int j = 0; j < 9; j++)
			{
				if (currentTestNumber == sudokuGrid[j][yPos])
				{
					throw std::exception("nested continue");
				}
			}
			//test column
			for (int j = 0; j < 9; j++)
			{
				if (currentTestNumber == sudokuGrid[xPos][j])
				{
					throw std::exception("nested continue");
				}
			}


			//testbox
			for (int j = subgridIndex[subgrid.xPos][0]; j < subgridIndex[subgrid.xPos][1] + 1; j++)
			{
				for (int k = subgridIndex[subgrid.yPos][0]; k < subgridIndex[subgrid.yPos][1] + 1; k++)
				{
					if (currentTestNumber == sudokuGrid[j][k])
					{
						throw std::exception("nested continue");
					}
				}
			}
		}
		catch (const  std::exception& e)
		{
			continue;
		}

		sudokuGrid[xPos][yPos] = currentTestNumber;
		if (recursionDepth == 80)
		{
			return gridWithSolveableBool(true, sudokuGrid);
		}
		gridWithSolveableBool recurse = sequentialBacktrackingMethod(sudokuGrid, recursionDepth + 1, numberOrderGrid,disallowedValue,cellWhereValIsDisallowed);
		if (recurse.solvable)
		{
			return recurse;
		}
		else
		{
			sudokuGrid[xPos][yPos] = 0;
			continue;
		}
	}
	return gridWithSolveableBool(false, sudokuGrid);

}

std::vector<std::vector<std::vector<int>>> randomiseNumberOrder()
{

	std::vector<std::vector<std::vector<int>>> numberOrderGrid(9, std::vector<std::vector<int>>(9, std::vector<int>(9, 0)));
	for (int i = 0; i < 9; i++)
	{
		for (int j = 0; j < 9; j++)
		{
			std::vector<int> numbersToSort = { 1, 2, 3, 4, 5, 6, 7, 8, 9 };
			for (int k = 0; k < 9; k++)
			{
				std::random_device rd;
				std::mt19937 gen(rd());
				std::uniform_int_distribution<> distr(0, numbersToSort.size() - 1);


				int index = distr(gen);
				numberOrderGrid[i][j][k] = numbersToSort[index];
				numbersToSort.erase(numbersToSort.begin() + index);
			}

		}
	}
	return numberOrderGrid;

}

//rule out the row column and subgrid of (xPos,yPos) in the mentalMarkGrid
void ruleOutRowColumnSubgrid(int xPos, int yPos, std::vector<std::vector<int>>& mentalMarkGrid)
{
	//mark row and column
	for (int i = 0; i < 9; i++)
	{
		mentalMarkGrid[xPos][i] = 1;
		mentalMarkGrid[i][yPos] = 1;
	}

	//mark subgrid
	std::vector<std::vector<int>> subgridIndex = { {0, 2},{3, 5},{6, 8} };
	coord subgrid = getSubgrid(xPos, yPos);
	for (int i = subgridIndex[subgrid.xPos][0]; i < subgridIndex[subgrid.xPos][1] + 1; i++)
	{
		for (int j = subgridIndex[subgrid.yPos][0]; j < subgridIndex[subgrid.yPos][1] + 1; j++)
		{
			mentalMarkGrid[i][j] = 1;
		}
	}
}

void fillMentalMarkGrid(std::vector<std::vector<int>>&sudokuGrid, std::vector<std::vector<int>>&mentalMarkGrid, int digit)
{
	for (int xPos = 0; xPos < 9; xPos++)
	{
		for (int yPos = 0; yPos < 9; yPos++)
		{
			if (sudokuGrid[xPos][yPos] == digit)
			{
				ruleOutRowColumnSubgrid(xPos, yPos, mentalMarkGrid);
			}
			//we also rule out all filled cells
			if (sudokuGrid[xPos][yPos] != 0)
			{
				mentalMarkGrid[xPos][yPos] = 1;
			}
		}
	}
}

std::vector<std::vector<int>> createSolution()
{
	std::vector<std::vector<int>> sudokuGrid(9, std::vector<int>(9, 0));
	std::vector<std::vector<std::vector<int>>> randomNumberOrder = randomiseNumberOrder();
	return sequentialBacktrackingMethod(sudokuGrid, 0, randomNumberOrder,-1,-1).grid;
}

gridWithUniqueness candidateBacktrackingMethod(std::vector<std::vector<int>> sudokuGrid, std::vector<std::vector<std::vector<int>>>& numberOrderGrid,
	int prevModified, int recursionDepth, std::vector<std::vector<std::vector<int>>> mentalMarkGrid, int solutions)
{
	bool flag = true;
	for (std::vector<int> i : sudokuGrid)
	{
		for (int j : i)
		{
			if (j == 0)
			{
				flag = false;
			}
		}
	}

	if (flag)
	{
		return gridWithUniqueness(sudokuGrid, solutions + 1);
	}

	if (recursionDepth == 0)
	{
		for (int i = 0; i < 9; i++)
		{
			fillMentalMarkGrid(sudokuGrid, mentalMarkGrid[i], i + 1);
		}
	}
	else
	{
		ruleOutRowColumnSubgrid(floor(prevModified % 9), floor(prevModified / 9), mentalMarkGrid[sudokuGrid[floor(prevModified % 9)][floor(prevModified / 9)] - 1]);
	}

	std::vector<coord> listOfCandidates;
	for (int i = 0; i < 9; i++)
	{
		for (int j = 0; j < 9; j++)
		{
			int candidateSum = 0;
			for (int k = 0; k < 0; k++)
			{
				if (mentalMarkGrid[k][i][j] == 0)
					candidateSum += 1;
			}
			if (candidateSum > 0)
			{
				listOfCandidates.push_back(coord(i, j));
			}
		}
	}

	for (coord candidate : listOfCandidates)
	{
		for (int i = 1; i < 10; i++)
		{
			if (mentalMarkGrid[i - 1][candidate.xPos][candidate.yPos] == 0)
			{
				std::vector<std::vector<int>> sudokuGridCopy = sudokuGrid;
				sudokuGridCopy[candidate.xPos][candidate.yPos] = i;
				int solutionAmount = candidateBacktrackingMethod(sudokuGridCopy, numberOrderGrid,
					candidate.yPos * 9 + candidate.xPos, recursionDepth + 1, mentalMarkGrid, solutions).uniqueness;
				if (solutionAmount > 1)
				{
					return gridWithUniqueness(sudokuGrid, solutions);
				}
				else
				{
					continue;
				}
			}
			else
			{
				continue;
			}
		}
	}

	return gridWithUniqueness(sudokuGrid, solutions);

}

gridWithSolveableBool searchForSolution(std::vector<std::vector<int>> sudokuGrid, std::vector<std::vector<std::vector<int>>>numberOrder,int disallowedVal,int cellWhereValIsDisallowed)
{
	std::vector<std::vector<std::vector<int>>> mentalMarkGrid(9, std::vector<std::vector<int>>(9, std::vector<int>(9, 0)));
	int solutions = 0;
	return sequentialBacktrackingMethod(sudokuGrid, 0, numberOrder, disallowedVal, cellWhereValIsDisallowed);
}

std::vector<std::vector<int>> createPuzzle(std::vector<std::vector<int>> sudokuGrid, int sumOfFilledSquares, std::vector<std::vector<std::vector<int>>> numberOrder, int threshold)
{
	std::cout << "current filled spaces=" + std::to_string(sumOfFilledSquares)<<std::endl;

	if (sumOfFilledSquares < threshold)
	{
		return sudokuGrid;
	}

	std::vector<int> gridSpaces(81);
	for (int i = 0; i < 81; i++)
	{
		gridSpaces[i] = i;
	}


	std::random_device rd;
	std::mt19937 gen(rd());
	

	std::vector<int> gridSpaceOrder;

	while (gridSpaces.size() > 0)
	{
		std::uniform_int_distribution<> distr(0, gridSpaces.size()-1);

		int index = distr(gen);
		if (sudokuGrid[index % 9][floor(index / 9)] != 0)
		{
			gridSpaceOrder.push_back(gridSpaces[index]);
		}
		gridSpaces.erase(gridSpaces.begin() + index);
	}

	//can automatically remove first cell
	if (sumOfFilledSquares == 81)
	{
		sudokuGrid[floor(gridSpaceOrder[0] % 9)][floor(gridSpaceOrder[0] / 9)] = 0;
		return createPuzzle(sudokuGrid, sumOfFilledSquares - 1, numberOrder, threshold);
	}

	for (int currentGridSpace : gridSpaceOrder)
	{
		int currentGridValue = sudokuGrid[floor(currentGridSpace % 9)][floor(currentGridSpace / 9)];
		std::vector<std::vector<int>> sudokuGridCopy = sudokuGrid;
		sudokuGridCopy[floor(currentGridSpace % 9)][floor(currentGridSpace / 9)] = 0;
		gridWithSolveableBool checkForSolution = searchForSolution(sudokuGridCopy, numberOrder, currentGridValue, currentGridSpace);

		if (checkForSolution.solvable)
		{
			continue;
		}
		sudokuGrid[floor(currentGridSpace % 9)][floor(currentGridSpace / 9)] = 0;
		return createPuzzle(sudokuGrid, sumOfFilledSquares - 1, numberOrder, threshold);

	}
	return sudokuGrid;

}

int main()
{
	std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
	std::vector<std::vector<int>> solution = createSolution();
	std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();


	print2DVector(solution);
	std::cout << "Time difference = " << std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count() << std::endl;
	std::cout << "Time difference = " << std::chrono::duration_cast<std::chrono::milliseconds>(end - begin).count() << std::endl;
	std::cout << "Time difference = " << std::chrono::duration_cast<std::chrono::seconds>(end - begin).count() << std::endl;

	std::vector<std::vector<std::vector<int>>> randomNumberOrder = randomiseNumberOrder();
	std::vector<std::vector<int>> puzzle = createPuzzle(solution, 81, randomNumberOrder, 50);
	print2DVector(puzzle);

	randomNumberOrder = randomiseNumberOrder();
	std::vector<std::vector<std::vector<int>>> mentalMarkGrid(9, std::vector<std::vector<int>>(9, std::vector<int>(9, 0)));

	//std::cout << candidateBacktrackingMethod(puzzle, randomNumberOrder, -1, 0, mentalMarkGrid, 0).uniqueness;

	return 0;
}