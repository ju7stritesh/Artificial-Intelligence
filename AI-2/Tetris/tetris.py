# Simple tetris program! v0.2
# D. Crandall, Sept 2016

from AnimatedTetris import *
from SimpleTetris import *
# from kbinput import *
import time, sys
import copy

class HumanPlayer:
    def get_moves(self, tetris):
        print "Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\nThen press enter. E.g.: bbbnn\n"
        moves = raw_input()
        return moves

    def control_game(self, tetris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": tetris.left, "n": tetris.rotate, "m": tetris.right, " ": tetris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. tetris is an object that lets you inspect the board, e.g.:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #
    def get_moves(self, tetris):
        tetris_temp = copy.deepcopy(tetris)
        all_comb = []
        curr_piece = tetris_temp.get_piece()
        all_comb.append(curr_piece[0])
        for g in range(3):
            tetris_temp.rotate()
            if tetris_temp.get_piece()[0] not in all_comb:
                all_comb.append(tetris_temp.get_piece()[0])
        piece = tetris_temp.get_piece()
        eval_dict = {}
        for r in range(len(all_comb)):
            for c in range(10 - len(all_comb[r][0])+1):
                tetris_temp = copy.deepcopy(tetris)
                tetris_temp.piece = all_comb[r]
                tetris_temp.col = c
                tetris_temp.row = 0
                try:
                    tetris_temp.down()
                except:
                    # print "Next value"
                    # print tetris_temp.get_board()
                    continue
                board = tetris_temp.get_board()
                tetris_temp1 = copy.deepcopy(tetris_temp)
                tetris_temp1.piece = tetris_temp.get_next_piece()
                all_comb1 = []
                curr_piece1 = tetris_temp1.piece
                all_comb1.append(curr_piece1)
                for g in range(3):
                    tetris_temp1.rotate()
                    if tetris_temp1.get_piece()[0] not in all_comb1:
                        all_comb1.append(tetris_temp1.get_piece()[0])
                for r1 in range(len(all_comb1)):
                    for c1 in range(10 - len(all_comb1[r1][0])+1):
                        tetris_temp1 = copy.deepcopy(tetris_temp)
                        tetris_temp1.piece = all_comb1[r1]
                        tetris_temp1.col = c1
                        tetris_temp1.row = 0
                        try:
                            tetris_temp1.down()
                        except:
                            # print "Next value1"
                            # print tetris_temp1.get_board()
                            continue
                        # tetris_temp1.down()
                        board = tetris_temp1.get_board()
                        num_holes = 0
                        lines_cleared = 0
                        holes = []
                        for i in range(1,len(board)):
                            line = 0
                            for j in range(len(board[i])):
                                if board[i][j] == ' ':
                                    for k in range(1,i):
                                        if board[i-k][j] == 'x':
                                            num_holes += 1
                                            holes.append([i,j])
                                            break
                                if board[i][j] == 'x':
                                    line += 1
                            if line == 10:
                                lines_cleared += 1
                        max_h = 0
                        for t in range(20):
                            if tetris.get_board()[t][c] == 'x':
                                max_h = 20-t
                                break
                            else:
                                max_h = 0
                        l_height = max_h + len(piece[0])/2
                        m = -200
                        for i in range(len(board)):
                            for j in range(len(board[i])-1):
                                if board[i][j] == 'x':
                                    if m < j:
                                        m = j
                        n = 200
                        for i in range(len(board[0])):
                            for j in range(len(board)-1):
                                if board[j][i] == 'x':
                                    if n > j:
                                        n = j
                        h = []
                        sum_heights = 0
                        bumpiness = 0
                        q = -10
                        for i in range(len(board[0])):
                            for j in range(len(board)):
                                if board[j][i] == 'x':
                                    h.append(20-j)
                                    break
                                if j == 19 and board[19][i] == ' ':
                                    h.append(0)
                        sum_heights = sum(h)
                        for b in range(len(h)-1):
                            bumpiness += abs(h[b] - h[b+1])

                        row_trans = 0
                        if m > 0:
                            for i in range(n,20):
                                for j in range(m):
                                    if board[i][j] == 'x' and board[i][j+1] == ' ':
                                        row_trans += 1
                                    elif board[i][j] == ' ' and board[i][j+1] == 'x':
                                        row_trans += 1
                        col_trans = 0
                        if n < 19:
                            for i in range(m+1):
                                for j in range(n,19):
                                    if board[j][i] == 'x' and board[j+1][i] == ' ':
                                        col_trans += 1
                                    elif board[j][i] == ' ' and board[j+1][i] == 'x':
                                        col_trans += 1
                        total_i = 0
                        for i in range(len(board[0])):
                            for j in range(len(board)-4):
                                if board[j][i] == 'x' and board[j+1][i] == ' ' and board[j+2][i] == ' ' and board[j+3][i] == ' ':
                                    total_i += 1
                                    break

                        well_sums = 0
                        for i in range(len(board)):
                            for j in range(1,(len(board[i])-1)):
                                if board[i][j] == ' ' and board[i][j+1] == 'x' and board[i][j-1] == 'x':
                                    well_sums += 1


                        # eval = -4.500158825082766*l_height + 3.4181268101392694*lines_cleared - 3.2178882868487753*row_trans - 9.348695305445199*col_trans - 7.899265427351652*num_holes - 3.3855972247263626*well_sums
                        # eval = -.310066*sum_heights + 4.9960666*lines_cleared - 2.55663*num_holes - 2.384483*bumpiness - .67878*max(h)
                        # eval = -.510066*(sum_heights)+ .760666*lines_cleared - .35663*num_holes - .184483*bumpiness
                        # eval = -max(h) + lines_cleared - .8*num_holes - .2*bumpiness
                        eval = 9.5182E14*lines_cleared + 8.627E-32*max(h) - 1.3699E21*bumpiness - 3.4514E22*num_holes
                        if eval not in eval_dict:
                            eval_dict[eval] = [all_comb[r], tetris.col, c, num_holes, lines_cleared, row_trans, col_trans, l_height, well_sums, total_i]
                        else:
                            eval_dict[eval].append([all_comb[r], tetris.col, c, num_holes, lines_cleared, row_trans, col_trans, l_height, well_sums, total_i])
        max1 = -1000000e123
        for key in eval_dict:
            if max1 < key:
                max1 = key
        temp_tetris1 = copy.deepcopy(tetris)
        str = ""
        if len(eval_dict) > 0:
            if (eval_dict[max1][1] - eval_dict[max1][2]) < 0:
                for v in range(abs((eval_dict[max1][1] - eval_dict[max1][2]))):
                    str += 'm'
            elif (eval_dict[max1][1] - eval_dict[max1][2]) > 0:
                for v in range(abs((eval_dict[max1][1] - eval_dict[max1][2]))):
                    str += 'b'
            if temp_tetris1.piece != eval_dict[max1][0]:
                for z in range(3):
                    temp_tetris1.rotate()
                    if temp_tetris1.get_piece()[0] != eval_dict[max1][0]:
                        str += 'n'
                    if temp_tetris1.get_piece()[0] == eval_dict[max1][0]:
                        str += 'n'
                        break

        test = random.choice("mnb") * random.randint(1, 10)

        # super simple current algorithm: just randomly move left, right, and rotate a few times
        return str

    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "tetris" object to control the movement. In particular:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, tetris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)

            board = tetris.get_board()
            column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            index = column_heights.index(max(column_heights))

            if(index < tetris.col):
                tetris.left()
            elif(index > tetris.col):
                tetris.right()
            else:
                tetris.down()


###################
#### main program

# (player_opt, interface_opt) = sys.argv[1:3]
player_opt = 'computer'
interface_opt = 'simple'

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print "unknown player!"

    if interface_opt == "simple":
        tetris = SimpleTetris()
    elif interface_opt == "animated":
        tetris = AnimatedTetris()
    else:
        print "unknown interface!"

    tetris.start_game(player)

except EndOfGame as s:
    print "\n\n\n", s