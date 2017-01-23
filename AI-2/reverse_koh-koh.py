import numpy as np
import time as t
#n is for board size and k is for number of matching pieces that cannot be together
n,k,board,time=4,3,'..bww.w.....wbbb',5

# def Game(N,k,board,time):
#     init_board=[ls for ls in [[i for i in board[i:i + len(board)/N]] for i in range(0, len(board), len(board)/N)]]
#     return init_board

def main():
    if n * n != len(board):
            print 'Please enter a valid board'
    else:
        game = Game(n,k,board,time)
    pos = 4*game[0][0][0] + game[0][0][1] - 1
    new_board = []
    for l in range(len(board)):
        if pos == l:
            new_board.append(game[1])
        else:
            new_board.append(board[l])
    print new_board
    # board[pos] += 'w'
    # board[game[0][0]][game[0][1]] = game[0][2]

def Game(N,k,board,time):
    init_board=[ls for ls in [[i for i in board[i:i + len(board)/N]] for i in range(0, len(board), len(board)/N)]]
    temp_board = []
    for i in range(len(init_board)):
        temp_board = [1 if x=='.' else x for x in init_board[i]]
        init_board[i] = temp_board
    w_count = 0
    b_count = 0
    for i in range(len(init_board)):
        for j in range(len(init_board[i])):
            if init_board[i][j] == 'w':
                w_count += 1
            elif init_board[i][j] == 'b':
                b_count += 1
    if w_count <= b_count:
        ch = 'w'
    elif w_count > b_count:
        ch = 'b'
    list1, list2 = best_position1(init_board,k,N,ch)
    # list1 = best_position2(init_board,k,N,ch)
    return choose_best_move(list1, list2), ch

def best_position1(board,k,n,ch):
    if ch == 'w':
        ch_t = 'b'
    else:
        ch_t = 'w'
    dic = {}
    dic1 = {}
    dic2 = {}
    clash = False
    l_j = []
    l_i = []
    for i in range(len(board)):
        for j in range(len(board)):
            total = 0
            max = -1
            if board[i][j] == 1:
                if clash == False:
                    l_j = []
                    count = 0
                    count1 = 0
                    for l in range(1,k):
                        if j+l < n:
                            if board[i][j+l] == ch_t:
                                break
                            elif board[i][j+l] == ch:
                                count += 1
                                l_j.append(j+l)
                        else:
                            break
                        if max < count:
                            max = count
                    if count > 0:
                        total += 1
                if clash == False:
                    l_i = []
                    count = 0
                    for l in range(1,k):
                        if j-l >= 0:
                            if board[i][j-l] == ch_t:
                                break
                            elif board[i][j-l] == ch:
                                count += 1
                                l_i.append(j-l)
                        else:
                            break
                    if count > 0:
                        total += 1
                    if len(l_i) > 0 and len(l_j) > 0:
                        m = -1
                        for x in range(len(l_i)):
                            for y in range(len(l_j)):
                                if l_j[y] - l_i[x] < k:
                                    s = x+y+2
                                    if m < s:
                                        m = s
                        if count < m:
                            count = m
                    if max < count:
                        max = count

                if clash == False:
                    l_j = []
                    count = 0
                    for l in range(1,k):
                        if i+l < n:
                            if board[i+l][j] == ch_t:
                                break
                            elif board[i+l][j] == ch:
                                count += 1
                                l_j.append(i+l)
                        else:
                            break
                        if max < count:
                            max = count
                    if count == k - 1:
                        total += 1
                if clash == False:
                    l_i = []
                    count = 0
                    for l in range(1,k):
                        if i-l >= 0:
                            if board[i-l][j] == ch_t:
                                break
                            elif board[i-l][j] == ch:
                                count += 1
                                l_i.append(i-l)
                        else:
                            break
                    if count > 0:
                        total += 1
                    if len(l_i) > 0 and len(l_j) > 0:
                        m = -1
                        for x in range(len(l_i)):
                            for y in range(len(l_j)):
                                if l_j[y] - l_i[x] < k:
                                    s = x+y+2
                                    if m < s:
                                        m = s
                        if count < m:
                            count = m
                    if max < count:
                        max = count
                if clash == False:
                    count = 0
                    l_j = []
                    for l in range(1,k):
                        if i+l < n and j+l < n:
                            if board[i+l][j+l] == ch_t:
                                break
                            elif board[i+l][j+l] == ch:
                                count += 1
                                l_j.append(j+l)
                        else:
                            break
                        if max < count:
                            max = count
                    if count > 0:
                        total += 1
                if clash == False:
                    count = 0
                    l_i = []
                    for l in range(1,k):
                        if i-l >= 0 and j-l >= 0:
                            if board[i-l][j-l] == ch_t:
                                break
                            elif board[i-l][j-l] == ch:
                                count += 1
                                l_i.append(j-l)
                        else:
                            break
                    if count > 0:
                        total += 1
                    if len(l_i) > 0 and len(l_j) > 0:
                        m = -1
                        for x in range(len(l_i)):
                            for y in range(len(l_j)):
                                if l_j[y] - l_i[x] < k:
                                    s = x+y+2
                                    if m < s:
                                        m = s
                        if count < m:
                            count = m
                    if max < count:
                        max = count
                if clash == False:
                    count = 0
                    l_j = []
                    for l in range(1,k):
                        if i-l >= 0 and j+l < n:
                            if board[i-l][j+l] == ch_t:
                                break
                            elif board[i-l][j+l] == ch:
                                count += 1
                                l_j.append(j+l)
                        else:
                            break
                        if max < count:
                            max = count
                    if count > 0:
                        total += 1
                if clash == False:
                    count = 0
                    l_i = []
                    for l in range(1,k):
                        if i+l < n and j-l >= 0:
                            if board[i+l][j-l] == ch_t:
                                break
                            elif board[i+l][j-l] == ch:
                                count += 1
                                l_i.append(j-l)
                    if count > 0:
                        total += 1
                    if len(l_i) > 0 and len(l_j) > 0:
                        m = -1
                        for x in range(len(l_i)):
                            for y in range(len(l_j)):
                                if l_j[y] - l_i[x] < k:
                                    s = x+y+2
                                    if m < s:
                                        m = s
                                else:
                                    break
                        if count < m:
                            count = m
                    if max < count:
                        max = count
            if max not in dic:
                dic[max] = [[i,j]]
            else:
                dic[max].append([i,j])
            if total not in dic1:
                dic1[total] = [[i,j]]
            else:
                dic1[total].append([i,j])
    del dic1[0]
    # del dic[0]
    del dic[-1]

    # print "List", dic1
    return dic1, dic

def best_position2(board,k,n,ch):
    if ch == 'w':
        ch_t = 'b'
    else:
        ch_t = 'w'
    dic = {}
    dic1 = {}
    dic2 = {}
    clash = False
    l_j = []
    l_i = []
    for i in range(len(board)):
        for j in range(len(board)):
            total = 0
            max = -1
            if board[i][j] == 1:
                if clash == False:
                    l_j = []
                    count = 0
                    count1 = 0
                    for l in range(1,k):
                        if j+l < n:
                            if board[i][j+l] != ch:
                                count += 1
                                l_j.append(j+l)
                            elif board[i][j+l] == ch:
                                break
                        else:
                            break
                        if max < count:
                            max = count
                    if count > 0:
                        total += 1
                if clash == False:
                    l_i = []
                    count = 0
                    for l in range(1,k):
                        if j-l >= 0:
                            if board[i][j-l] != ch:
                                count += 1
                                l_i.append(j-l)
                            elif board[i][j-l] == ch:
                                break
                        else:
                            break
                    if count > 0:
                        total += 1
                    if len(l_i) > 0 and len(l_j) > 0:
                        m = -1
                        for x in range(len(l_i)):
                            for y in range(len(l_j)):
                                if l_j[y] - l_i[x] < k:
                                    s = x+y+2
                                    if m < s:
                                        m = s
                        if count < m:
                            count = m
                    if max < count:
                        max = count

                if clash == False:
                    l_j = []
                    count = 0
                    for l in range(1,k):
                        if i+l < n:
                            if board[i+l][j] != ch:
                                count += 1
                                l_j.append(i+l)
                            elif board[i+l][j] == ch:
                                break
                        else:
                            break
                        if max < count:
                            max = count
                    if count > 0:
                        total += 1
                if clash == False:
                    l_i = []
                    count = 0
                    for l in range(1,k):
                        if i-l >= 0:
                            if board[i-l][j] != ch:
                                count += 1
                                l_i.append(i-l)
                            elif board[i-l][j] == ch:
                                break
                        else:
                            break
                    if count > 0:
                        total += 1
                    if len(l_i) > 0 and len(l_j) > 0:
                        m = -1
                        for x in range(len(l_i)):
                            for y in range(len(l_j)):
                                if l_j[y] - l_i[x] < k:
                                    s = x+y+2
                                    if m < s:
                                        m = s
                        if count < m:
                            count = m
                    if max < count:
                        max = count
                if clash == False:
                    count = 0
                    l_j = []
                    for l in range(1,k):
                        if i+l < n and j+l < n:
                            if board[i+l][j+l] != ch:
                                count += 1
                                l_j.append(j+l)
                            elif board[i+l][j+l] == ch:
                                break
                        else:
                            break
                        if max < count:
                            max = count
                    if count > 0:
                        total += 1
                if clash == False:
                    count = 0
                    l_i = []
                    for l in range(1,k):
                        if i-l >= 0 and j-l >= 0:
                            if board[i-l][j-l] != ch:
                                count += 1
                                l_i.append(j-l)
                            elif board[i-l][j-l] == ch:
                                break
                        else:
                            break
                    if count > 0:
                        total += 1
                    if len(l_i) > 0 and len(l_j) > 0:
                        m = -1
                        for x in range(len(l_i)):
                            for y in range(len(l_j)):
                                if l_j[y] - l_i[x] < k:
                                    s = x+y+2
                                    if m < s:
                                        m = s
                        if count < m:
                            count = m
                    if max < count:
                        max = count
                if clash == False:
                    count = 0
                    l_j = []
                    for l in range(1,k):
                        if i-l >= 0 and j+l < n:
                            if board[i-l][j+l] != ch:
                                count += 1
                                l_j.append(j+l)
                            elif board[i-l][j+l] == ch:
                                break
                        else:
                            break
                        if max < count:
                            max = count
                    if count > 0:
                        total += 1
                if clash == False:
                    count = 0
                    l_i = []
                    for l in range(1,k):
                        if i+l < n and j-l >= 0:
                            if board[i+l][j-l] != ch:
                                count += 1
                                l_i.append(j-l)
                            elif board[i+l][j-l] == ch:
                                break
                    if count > 0:
                        total += 1
                    if len(l_i) > 0 and len(l_j) > 0:
                        m = -1
                        for x in range(len(l_i)):
                            for y in range(len(l_j)):
                                if l_j[y] - l_i[x] < k:
                                    s = x+y+2
                                    if m < s:
                                        m = s
                                else:
                                    break
                        if count < m:
                            count = m
                    if max < count:
                        max = count
            if max not in dic:
                dic[max] = [[i,j]]
            else:
                dic[max].append([i,j])
            if total not in dic1:
                dic1[total] = [[i,j]]
            else:
                dic1[total].append([i,j])
    del dic1[0]
    # del dic[0]
    del dic[-1]

    # print "List", dic1
    return dic1, dic


def choose_best_move(list1, list2):
    for key1 in list1:
        for i in range(len(list1[key1])):
            for key2 in list2:
                for j in range(len(list2[key2])):
                    if list1[key1][i] == list2[key2][j] and key2 < k-1:
                        return list1[key1][i], key2


if __name__ == '__main__':
    start_time = t.time()
    main()
    print "time",(t.time() - start_time)