import numpy as np
import sys
import random

# A global variable used to display the tic-tac-toe board in proper format
displayBoard = None

# A global quantity used to represent a very high negative value
negativeInfinity = (-1 * sys.maxsize)

# A global quantity used to represent a very high positive value
positiveInfinity = sys.maxsize



class MiniMaxNode:
    """Class that is used to construct every node in the MiniMax Tree"""
    def __init__(self, depth, currentPlayer, boardState, noOfFreeSpaces, row, col):
        """The node constructor that creates a node in the MiniMax tree after making a move from the parent"""
        self.depth = depth
        self.currentPlayer = currentPlayer
        self.boardState = boardState
        self.noOfFreeSpaces = noOfFreeSpaces
        self.moveRow = row
        self.moveCol = col
        self.noOfChildren = 0
        self.chosenChild = None
        if self.currentPlayer > 0:
            self.heuristicValue = negativeInfinity
        else:
            self.heuristicValue = positiveInfinity
        self.childrenStates = []
        self.generateChildren()
        return
    def generateChildren(self):
        """Function that in an recursive Depth First manner generates the childern of the current node by applying valid moves"""
        global flag, criticalFlag
        try :
            if findValueOfState(self.boardState, self.currentPlayer) == 3:
                self.heuristicValue = 3
                return
            if findValueOfState(self.boardState, self.currentPlayer) == -3:
                self.heuristicValue = -3
                return
            if self.noOfFreeSpaces == 0 or self.depth < 0:
                self.heuristicValue = findValueOfState(self.boardState, -1 * self.currentPlayer)
                return
            if self.depth >= 0:
                possibleMoves = findMoves(self.boardState)
                for move in possibleMoves:
                    duplicateBoard = np.empty((3,3), dtype=np.int32)
                    np.copyto(duplicateBoard, self.boardState)
                    duplicateBoard[move[0]][move[1]] = self.currentPlayer
                    child = MiniMaxNode(self.depth - 1, -1 * self.currentPlayer, duplicateBoard, self.noOfFreeSpaces - 1, move[0], move[1])
                    self.childrenStates.append(child)
                    self.noOfChildren += 1
                    if self.currentPlayer > 0:
                        if child.heuristicValue > self.heuristicValue:
                            self.heuristicValue = child.heuristicValue
                            self.chosenChild = child
                        elif child.heuristicValue == self.heuristicValue:
                            if child.noOfChildren < self.chosenChild.noOfChildren:
                                self.heuristicValue = child.heuristicValue
                                self.chosenChild = child

                    else:
                        if child.heuristicValue < self.heuristicValue:
                            self.heuristicValue = child.heuristicValue
                            self.chosenChild = child
                        elif child.heuristicValue == self.heuristicValue:
                            if child.noOfChildren < self.chosenChild.noOfChildren:
                                self.heuristicValue = child.heuristicValue
                                self.chosenChild = child

        except Exception as e:
            print("FAIL\nFailed to generateChildren : ", str(e))
            exit(0)
        return

def findValueOfState(boardOfState, playerOfState):
    """A function that is used to decide the value of a particular board state."""
    stateValue = [sum(boardOfState[:,0]), sum(boardOfState[:,1]), sum(boardOfState[:,2]), sum(boardOfState[0,:]), sum(boardOfState[1,:]), sum(boardOfState[2,:])]
    stateValue.append(boardOfState[0][0]+boardOfState[1][1]+boardOfState[2][2])
    stateValue.append(boardOfState[0][2] + boardOfState[1][1] + boardOfState[2][0])
    if min(stateValue) == -3:
        return -3
    if max(stateValue) == 3:
        return 3
    if playerOfState > 0:
        stateValue = max(stateValue)
    else:
        stateValue = min(stateValue)
    return stateValue


def findMoves(boardParameter):
    """A function that iteratively finds the currently possible moves and returns a list of these moves"""
    try:
        possibleMoves = []
        for i in range(0, 3):
            for j in range(0, 3):
                if boardParameter[i][j] == 0:
                    possibleMoves.append([i,j])
        return possibleMoves
    except Exception as e:
        print("FAIL\nfindMoves :- ", str(e))
        exit(0)
    return



def initializeParameters(boardTobeInitialized):
    """A function that initializes the display as well as starting boards"""
    initializeDisplayBoard()
    boardTobeInitialized = np.zeros((3, 3), dtype=np.int32)
    return boardTobeInitialized

def initializeDisplayBoard():
    """A function that acutally sets up the display board"""
    global displayBoard
    displayBoard = np.full((11,11), ' ', dtype=np.chararray)
    for i in range(0,11):
        for j in range(0,11):
            if (i == 3 and j == 3) or (i == 3 and j == 7) or (i == 7 and j == 3) or (i == 7 and j == 7):
                displayBoard[i][j] = '+'
            elif i == 3 or i == 7:
                displayBoard[i][j] = '-'
            elif j == 3 or j == 7:
                displayBoard[i][j] = '|'
            else:
                displayBoard[i][j] = ' '
    return

def displayBoardState(boardToDisplay):
    displayBoard[1][1] = "" + str(boardToDisplay[0][0])
    displayBoard[1][5] = "" + str(boardToDisplay[0][1])
    displayBoard[1][9] = "" + str(boardToDisplay[0][2])

    displayBoard[5][1] = "" + str(boardToDisplay[1][0])
    displayBoard[5][5] = "" + str(boardToDisplay[1][1])
    displayBoard[5][9] = "" + str(boardToDisplay[1][2])

    displayBoard[9][1] = "" + str(boardToDisplay[2][0])
    displayBoard[9][5] = "" + str(boardToDisplay[2][1])
    displayBoard[9][9] = "" + str(boardToDisplay[2][2])

    for i in range(0,11):
        print(end="\t\t")
        for j in range(0,11):
            if displayBoard[i][j] == '1':
                print("X", end="")
            elif displayBoard[i][j] == '-1':
                print("O", end = "")
            elif displayBoard[i][j] == '0':
                print(" ", end="")
            else:
                print(displayBoard[i][j], end="")
        print()

    return

def validateInput(row, col, boardToValidateOn):
    """A function to validate the input"""
    try:
        if row < 0 or row > 2:
            return False
        if col < 0 or col > 2:
            return False
        if boardToValidateOn[row][col] != 0:
            return False
        return True
    except:
        return False



def game():
    """The function that actually simulates the game"""
    try:
        board = None
        depth = 9
        noOfFreeLocations = 9
        player = -1
        board = initializeParameters(board)

        print("Choose your difficulty : \n\tEasy - (e\E)\n\tHard - (h\H)")
        difficulty = input("Choice : ")

        if difficulty in 'eE':
            depth = 1
        elif difficulty in 'hH':
            depth = 6
        else:
            depth = 9

        if random.random() > random.random():
            print("\n\nBy random Choice, the computer starts !\n\n")
            player = 1
        else:
            print("\n\nBy random Choice, you start the game !\n\n")
            player = -1

        displayBoardState(board)

        while noOfFreeLocations > 0:
            state = findValueOfState(board,player)

            if state == 3:
                print("Computer Wins !")
                exit(0)
            elif state == -3:
                print("You Win !")
                exit(0)

            if player == 1:
                a = MiniMaxNode(depth,1,board,noOfFreeLocations,-1,-1)
                print("Computer makes the move :- Row : ",a.chosenChild.moveRow+1,"  |  Column : ", a.chosenChild.moveCol+1)
                board[a.chosenChild.moveRow][a.chosenChild.moveCol] = 1

            else:
                r = c = -1
                while validateInput(r, c, board) == False:
                    print("Your turn to make a move, choose a row and column (1 - 3) : ")
                    r = int(input("Row    : ")) - 1
                    c = int(input("Column : ")) - 1

                board[r][c] = -1

            noOfFreeLocations -= 1
            player = player * -1
            print("\n*********************************************************\n\n")
            displayBoardState(board)

        print("It's a draw ! Everybody wins .!! Or does Everybody loose ?? Food for thought ! :)")

    except Exception as e:
        print("Game exception : ", str(e))
        exit(0)


game()
