# Sasha Sreckovic
#
import random
import math
import time

def main():
    #UNCOMMENT FOR TIMING
    #ts = time.time()

    with open('nqueens.txt') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        with open('nqueens_out.txt', 'a') as w:
            queensPos = []
            while(queensPos == []):

                #run min conflicts passing in board size
                queensPos = minConflictsSolver(int(lines[i]))
            w.write(str(queensPos))
            w.write("\n")

    
    #UNCOMMENT FOR TIMING
    #td = time.time() - ts
    #print(td)   



#This function takes the size of the board and returns a list of 
#the positions of the queens on the board
def minConflictsSolver(boardSize):

    if boardSize > 10000:
        maxSteps = int(boardSize/50)
    else: 
        maxSteps = 200

    #set current initial state of board using greedy alg with
    # with random start point (in the column) then go column by column
    # picking a position with least conflicts
    (current, colConflicts, negDiagonal,posDiagonal, queensInConflict,emptyCols) = setInitialBoard(boardSize)
    
    for i in range(maxSteps):

        #if the current positions are a solution, return the current list
        solved = checkSolved(queensInConflict, emptyCols)

        if solved:
            return current



        #determine the number of pieces you are randomly checking for conflicts
        #(checking all would take too much time)
        numChecks = math.floor(math.log(boardSize, 2))

        if numChecks < 2:
            numChecks = 2

        maxConflicts = 0
        maxIndex = -1

        #randomly pick log(boardsize) number of pieces and find conflicts and take the one with the most
        #conflicts so it can be moved.
        for i in range(numChecks):
            conflicts = 0
            randIndex = random.randint(0,len(queensInConflict) -1)
            row = queensInConflict[randIndex]
            col = current[row]
            conflicts = colConflicts[col] + negDiagonal[row - col + boardSize -1] + posDiagonal[row + col]

            if conflicts > maxConflicts:
                maxConflicts = conflicts
                maxIndex = randIndex    



        #the chosen queen
        var = queensInConflict[maxIndex]
        col = current[var]
        
        #move the queen to min conflicts position in the row
        (newCol, index) = getMinConflicts((var,col), current , boardSize, colConflicts, negDiagonal, posDiagonal, emptyCols) 

        if len(emptyCols) <= 1:
            emptyCols = []

        elif index == len(emptyCols) -1:
            emptyCols.pop()
        else:
            
            emptyCols[minIndex] = emptyCols.pop()


        #fix the conflicts lists after the move
        colConflicts[col] -= 1
        colConflicts[newCol] +=1

        posDiagonal[var + col] -= 1 
        posDiagonal[var + newCol] += 1

        negDiagonal[var - col + boardSize-1] -=1
        negDiagonal[var - newCol + boardSize-1] +=1

        
        #add the column that was just moved from to the empty columns list
        #if there are no queens currently in that column
        if colConflicts[col] == 0:
            emptyCols.append(col)


        current[var] = newCol
        queensInConflict = []

        #find all the new queens in conflict after the move
        for row in range(boardSize):
            col = current[row]
            confs = colConflicts[col] + negDiagonal[row - col + boardSize -1] + posDiagonal[row + col]
            if confs > 3:
                queensInConflict.append(row)


    #if you make it through maxSteps iterations return an empty list;
    return []



#this function takes the size of the board and creates an initial configuration of the board using greedy algorithm
#with minimum conflicts as the heuristic to determine where to place each queen.
def setInitialBoard(boardSize):
    
    #List of positions of the queens
    piecePositions = [] 

    #List of queens that have conflicts, useful for when moving positions of queens 
    queensInConflict = []

    #initialize the lists
    #emptyCols holds a list of all columns that currently have no queens
    #colConflicts holds a list of length boardSize that holds the number of conflicts in each row
    #negDiagonals holds the number of conflicts in each diagonal going from top left to bottom right
    #PosDiagonals holds the number of conflicts in each diagonal going from top right to bottom left
    
    emptyCols = list(range(0,boardSize))
    colConflicts = [0] * boardSize
    negDiagonal = [0]*(2*boardSize - 1)
    posDiagonal = [0]*(2*boardSize - 1)
    

    #loop through rows
    for row in range(boardSize):
        conflicts = 0
        minIndex = -1
        minConflicts = boardSize

        #offset is randomly chosen so that each new configuration of the board starts in a different spot
        offset = random.randint(1,boardSize-1)

        #in this row, for each empty column look for a spot with zero conflict, if not choose the minimum conflicts spot
        for i in range(len(emptyCols)-1):
            
            if len(emptyCols) == 1:
                minIndex = 0
                break
            elif len(emptyCols) < 1:
                break

            else:
                index = (i+offset)%len(emptyCols)
                col = emptyCols[index]

                conflicts = colConflicts[col] + negDiagonal[row - col + boardSize -1] + posDiagonal[row + col]

                if conflicts == 0:
                    #if no conflicts choose this option
                    minConflicts = 0
                    minIndex = index
                    break

                elif conflicts < minConflicts:
                    minConflicts = conflicts
                    minIndex = index



        colNum = emptyCols[minIndex]
        piecePositions.append(colNum)

        if len(emptyCols) <= 1:
            emptyCols = []

        elif minIndex == len(emptyCols) -1:
            emptyCols.pop()
        else:
            
            emptyCols[minIndex] = emptyCols.pop()

        colConflicts[colNum] +=1

        #set the positions of the new pieces in the diagonal list
        #neg Diagonal shows them from top right corner as first index
        negDiagonal[row - colNum + boardSize -1] +=1
        posDiagonal[row + colNum] += 1



    #get a list of all of the queens in conflict after the board is set.
    for row in range(boardSize):
        col = piecePositions[row]
        confs = colConflicts[col] + negDiagonal[row - col + boardSize -1] + posDiagonal[row + col]
        if confs > 3:
            queensInConflict.append(row)


    return (piecePositions, colConflicts, negDiagonal,posDiagonal, queensInConflict,emptyCols)




#this function takes the position of 1 queen, the state of the board and
#the board size as well as the lists that hold the number of conflicts
#and returns the position in the column of the single queen
#that has the least number of conflicts with other queens.
def getMinConflicts(queen, current , boardSize, colConflicts, negDiagonal, posDiagonal,emptyCols):

    (qRow, qCol) = queen

    minRow = 0
    minConf = boardSize
    minIndex = -1
    minList = []

    confs = 0
    emptyIndex = -1
    length = len(emptyCols)

    #if there are any columns that are empty put a queen in there first.
    if length > 0:

        for i in range(len(emptyCols)-1):
            col = emptyCols[i]
            confs = posDiagonal[qRow + col] + negDiagonal[qRow-col+boardSize-1]

            if confs == 0:
                return (col,i)
            elif confs < minConf:
                minConf = confs
                minIndex = col
                emptyIndex = i

        if length == 1:
            return (emptyCols[0], 0)
        else:
            return (col, emptyIndex)

    else:
        #find the column with the least number of conflicts for the pieces given row.
        for j in range(boardSize):
            colIndex = random.randint(0,boardSize-1)
            confs = colConflicts[colIndex] + posDiagonal[qRow + colIndex] + negDiagonal[qRow-colIndex+boardSize-1]

            if confs == 1:
                return (colIndex,-1)
            elif confs < minConf:
                minConf = confs
                minIndex = colIndex

    #the item was not in the emptyCols list so return -1 along with the column
    return (minIndex, -1)



#function to see if the current state of the board is a solution
#returns true if solved, false otherwise
def checkSolved(queensInConflict,emptyCols):

    if len(queensInConflict) == 0 and len(emptyCols) == 0:
        return True
    else:
        return False
