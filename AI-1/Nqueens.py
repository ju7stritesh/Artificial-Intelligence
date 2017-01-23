# nrooks.py : Solve the N-Rooks problem!
# D. Crandall, August 2016
#
# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.
#l = []
# This is N, the size of the board.
N=8

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] )

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] )

# Count diagonals for a given row and column
def count_on_diagonal(board, row, col):
    diag1 = 0
    for r in range(0,N):
        diag1 += board[row+r][col+r]
        if row+r == N-1 or col+r == N-1:
            break
    for r in range(0,N):
        diag1 += board[row-r][col-r]
        if row-r == 0 or col-r ==0:
            break
    diag2 = 0
    for r in range (0,N):
        diag2 += board[row+r][col-r]
        if (row+r)==N-1 or col-r == 0:
            break
    for r in range(0,N):
        diag2 += board[row-r][col+r]
        if row-r == 0 or col+r == N-1:
            break
    return diag1 - board[row][col],diag2 - board[row][col]

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([ " ".join([ "Q" if col else "_" for col in row ]) for row in board])

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
def successors(board):
    return [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) ]

# Get list of successors of given board state without duplicates
def successors2(board):
    l = []
    if count_pieces(board) == N:   #Stop generating successors when the board already has N rooks
        return l
    l = [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) ]
    l = [x for x in l if x != board]  #delete duplicate successors to avoid cycles
    return l

def successors3(board):
    t = []
    if count_pieces(board) == N:            #Stop generating successors when the board already has N rooks
        return t
    l = [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) ]
    total = count_pieces(board) + 1
    l = [x for x in l if x != board]        #delete duplicate successors to avoid cycles
    for x in l:                             #send only those successors where the queens are placed diagonally
        d,f = count_on_diagonal(x,0,0)
        if d == total:
            t.append(x)
            break
    return t

# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )


# Solve n-rooks!
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors3( fringe.pop() ):
            if is_goal(s):
                return(s)
            # if count_pieces(s) < N:
            fringe.append(s)
    return False

# Solve the Queen problem using backtracking
def nqueens_solve(initial_board):
    fringe = initial_board
    queen = 1                       #initialize first queen
    col = []
    curr_col = 0
    fringe[queen-1][curr_col] = 1   #insert the first queen in the first position
    col.append(curr_col)            # keep track of all the queen's column position while index gives the row count
    queen += 1                      #one queen placed so increase the count
    while queen <= N:
        if len(col) == queen:       # The if condition keeps track of whether it is a new Queen or a Queen we backtracked
            x = col[queen-1] + 1
            if x >= N:              #This is to check if the Queen cannot go further right
                fringe[queen-1] = [0]*N
                col.pop()
                queen -= 1
                continue
            else:                   #reset the row and find a new position for the queen
                col.pop()
                fringe[queen-1] = [0]*N
        else:
            x = 0                   #new queen to be placed so start from first column
        for c in range(x,N):                #for loop to check every column and place a Queen
            diag1, diag2 = count_on_diagonal(fringe, queen-1, c)
            row_count = count_on_col(fringe, c)
            if row_count != 1 and diag1 != 1 and diag2 != 1:  #when all conditions are satisfied then place the queen
                fringe[queen-1][c] = 1
                col.append(c)
                queen += 1
                break
            elif c == N-1:                  #If the Queen cannot be placed anywhere, backtrack to the last Queen and change its position
                queen -= 1
    return fringe


# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
#initial_board = [[0]*N]*N
initial_board = [[0]*N for _ in range(N)]
print "Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n"
option = int(raw_input("Type 1 or 2 for Queen or Rook respectively"))
if option == 1:
    solution = nqueens_solve(initial_board)
if option == 2:
    solution = solve(initial_board)
print printable_board(solution) if solution else "Sorry, no solution found. :("
