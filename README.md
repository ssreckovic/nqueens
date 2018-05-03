# nqueens


The N-Queens Problem is a game where given a square chess board of size n you must place n Queens on the
board such that none of them could immediately attack or be attacked by another queen (Cannot be in the same row, column or diagonal).

This solution creates an initial board configuration using a greedy algorithm to attempt to reduce the number of conflicting pieces.
It then uses an iterative repair algorithm with a minimum-conflicts heuristic to determine which pieces to move around. If a solution is 
not found within a certain number of steps a new board is created and everything is attempted again.


This program reads input from a file called “nqueens.txt” which contains successive lines of 
input. Each line of input consists of a single integer value, n, where n > 3 and n <= 1,000,000, that determines the size of the n-queens problem to be solved. 

Eg. 

64
200
1000
45000

The program outputs a solution to each of the inputted board sizes into a text file called "nqueens_out.txt". The output
contains the position of each queen on the board. (ROW, COLUMN).