import copy
import sys
def read_file():
    read_file = open(sys.argv[1], 'r')
    for line in read_file:
        items = line.rstrip('\r\n').split(' ')
        friends_list[items[0]] = [x for x in items if x != items[0]]
        for i in friends_list:
            if i not in unique_friends:
                unique_friends.append(i)
            for t in range(len(friends_list[i])):
                if friends_list[i][t] not in unique_friends:
                    unique_friends.append(friends_list[i][t])

def not_friend_list_dict():
    for i in range(len(unique_friends)):
        l = []
        if unique_friends[i] in friends_list:
            for g in range(len(unique_friends)):
                if unique_friends[g] not in friends_list[unique_friends[i]] and unique_friends[g] != unique_friends[i]:
                    if unique_friends[g] in friends_list:
                        if unique_friends[i] not in friends_list[unique_friends[g]]:
                            l.append(unique_friends[g])
                    else:
                        l.append(unique_friends[g])
            if len(l) == 0:
                l = [0]
            not_friend_list[unique_friends[i]] = l

def count_not_friends_dict():
    for i in not_friend_list:
        keep_count[i] = len(not_friend_list[i])

def partition():
    t_list = copy.deepcopy(not_friend_list)
    # t_list = [sorted(t_list.items(), reverse=False)]
    for i in not_friend_list:
        pl = []
        if len(t_list[i]) < N:
            if t_list[i] != [0]:
                pl = t_list[i]
            if i not in already_seated:
                pl.append(i)
            if len(pl) == 0:
                if i in already_seated:
                    del t_list[i]
                break
            tables.append(pl)
            for v in range(len(pl)):
                if pl[v] not in already_seated:
                    already_seated.append(pl[v])
            n1 = pl
            t_list2 = {}
            t_list2 = copy.deepcopy(t_list)
            for u in range(len(n1)):
                for m in t_list2:
                    for n in range(len(t_list2[m])):
                        if n1[u] == t_list2[m][n]:
                            del t_list2[m][n]
                            break
            t_list = t_list2
            del t_list[i]
            del keep_count[i]
    # t_list = [sorted(t_list.items(), reverse=False)]
    total = 0
    t_list4 = copy.deepcopy(t_list)
    for i in t_list4:
        l = {}
        if total == 0:
            for j in range(len(t_list[i])):
                common = 0
                for t in t_list:
                    if t_list[i][j] in t_list[t]:
                        common += 1
                if t_list[i][j] in t_list and t_list[i][j] not in already_seated:
                    l[t_list[i][j]] = common+1
                else:
                    l[t_list[i][j]] = common
            common = 0
            if i not in already_seated:
                for t in t_list:
                    if i in t_list[t]:
                        common += 1
                l[i] = common+1
            list = []
            l1 = copy.deepcopy(l)
            while len(l) > 0:
                min = 9000000
                for k in l:
                    if l[k] < min:
                        min = l[k]
                        id = k
                list.append(id)
                del l[id]
                if len(list) == N:
                    tables.append(list)
                    already_seated.extend(list)
                    for id1 in list:
                        t_list1 = {}
                        t_list1 = copy.deepcopy(t_list)
                        for m in t_list:
                            for n in range(len(t_list[m])):
                                if id1 == t_list[m][n]:
                                    del t_list1[m][n]
                                    break
                        # del t_list[i][j]
                        t_list = t_list1
                        del l1[id1]
                    list = []
            add = []
            for o in list:
                if l1[o] == 1:
                    add.append(o)
                    t_list3 = copy.deepcopy(t_list)
                    for m in t_list:
                        for n in range(len(t_list[m])):
                            if o == t_list[m][n]:
                                del t_list3[m][n]
                                break
                    t_list = t_list3
                if len(add) > 0:
                    tables.append(add)
                    already_seated.extend(list)
            del t_list[i]


keep_count = {}
tables = []
not_friend_list = {}
friends_list = {}
unique_friends = []
already_seated = []
N = int(sys.argv[2])
# N = int(raw_input("Type the value of N"))
read_file()
not_friend_list_dict()
count_not_friends_dict()
partition()
final_table = []
for i in range(len(tables)):
    if tables[i] != [0]:
        final_table.append(tables[i])
print final_table