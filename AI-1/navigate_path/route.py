import math
import sys
class cities_info(object):
    def __init__(self, id, city1, city2, length, speed_limit, highway_name):
            self.id = id
            self.city1 = city1
            self.city2 = city2
            self.length = length
            self.speed_limit = speed_limit
            self.highway_name = highway_name

class city_node(object):
    def __init__(self, id, parent_node, depth):
        self.id = id
        self.parent_node = parent_node
        self.depth = depth

def read_gps():
    read_file = open('city-gps.txt', 'r')
    for line in read_file:
        items = line.split(' ')
        items[1] = float(items[1])
        items[2] = float(items[2])
        city_gps[items[0]] = [items[1], items[2]]

def distance_lat_lon(latitude1, longitude1, latitude2, longitude2):
    lat1_radians = math.radians(latitude1)
    lat2_radians = math.radians(latitude2)

    diff_lat = math.radians(abs(latitude2 - latitude1))
    diff_lon = math.radians(abs(longitude2 - longitude1))
    a = (math.pow((math.sin(diff_lat/2.0)),2)) + math.cos(lat1_radians)*math.cos(lat2_radians)*(math.pow((math.sin(diff_lon/2.0)),2))
    c = 2.0*(math.atan2(*(math.sqrt(a), math.sqrt(1-a))))
    d = 3960*c
    return d

def read_road_segments():
    read_file = open('road-segments.txt', 'r')
    counter = 1
    for line in read_file:
        items = line.split(' ')
        id = counter
        city1 = items[0]
        city2 = items[1]
        length = int(items[2])
        if items[3] == '' or items[3] == 0:              #Speed limit may be missing
            speed_limit = 36
        else:
            speed_limit = int(items[3])
        highway_name = items[4]
        cities_obj = cities_info(id, city1, city2, length, speed_limit, highway_name)
        cities_dict[id] = cities_obj
        counter += 1

def successor_cities(city):
    l =[]
    for i in cities_dict:
        if cities_dict[i].city1 == city.id:
            city_obj = city_node(cities_dict[i].city2, city.id, city.depth+1)
            l.append(city_obj)
        if cities_dict[i].city2 == city.id:
            city_obj = city_node(cities_dict[i].city1, city.id, city.depth+1)
            l.append(city_obj)
    return l

def solve_ids():
    global stop
    while stop != 1:
        solve_bfs(start_city, final_city)

def solve_bfs(start_city, end_city):
    global ids_count
    global main_list
    global paths
    global stop
    read_road_segments()
    city_obj = city_node(start_city, 'root', 0)
    fringe = []
    main_list = []
    paths = []
    fringe.append(city_obj)
    main_list.append(city_obj)
    count = 0
    while len(fringe) > 0:
        if rout_algo == 2:
            k = fringe.pop()
        elif rout_algo == 1 or rout_algo == 3:
            k = fringe.pop(0)
        # print k.id, len(main_list), len(set(main_list))
        p = (successor_cities(k))
        if rout_algo == 3:
            if k.depth == ids_count:
                ids_count += 1
                # print ids_count, k.depth
                return
            # else:
            #     ids_count += 1
            #     print ids_count
        final_list = []
        f = 0
        for d in range(len(p)):
            add = 0
            for t in range(len(main_list)):
                if p[d].id == end_city:
                    if len(paths) == 1 and rout_algo == 3:
                        print journey(paths[0])
                        stop = 1
                        return False
                    if len(paths) == 1:
                        q = journey(paths[0])
                        q[3].insert(len(q[3]),final_city)
                        # print w[len(w)-1]
                        u = dist_between_cities(q[3][len(q[3])-1], q[3][len(q[3])-2])
                        q[0] = q[0] + u[0]
                        q[1] = q[1] + u[1]
                        q[2] = q[2] + u[2]
                        print q
                        print "Waiting for the optimal path"
                    if k.id in paths:
                            paths.remove(k.id)
                    if rout_algo == 2 or rout_algo == 3 or rout_option == 1:
                        paths.append(k.id)
                        q = journey(paths[0])
                        q[3].insert(len(q[3]),final_city)
                        # print w[len(w)-1]
                        u = dist_between_cities(q[3][len(q[3])-1], q[3][len(q[3])-2])
                        q[0] = q[0] + u[0]
                        q[1] = q[1] + u[1]
                        q[2] = q[2] + u[2]
                        print q
                        return paths
                    else:
                        paths.append(k.id)
                    add = 1
                    count += 1
                    # print k.id
                    if len(set(paths)) == t_neighbours:
                        return paths
                    else:
                        break
                if p[d].id == main_list[t].id:
                    a = journey(k.id)
                    m = dist_between_cities(k.id, p[d].id)
                    info1 = a[option] + m[option]
                    c = journey(p[d].id)
                    # print c
                    info2 = c[option]
                    if info1 >= info2:
                        add = 1
                        break
                    else:
                        new_parent = [x for x in main_list if x.id == p[d].id]
                        main_list = [x for x in main_list if x.id != p[d].id]
                        main_list.append(p[d])
                        f = 1
                        fringe = [x for x in fringe if x.id != new_parent[0].id]
                        break
            if add == 0:
                final_list.append(p[d])

        fringe.extend(final_list)
        if f == 1:
            temp_list = [x for x in final_list if x.id != new_parent[0].id]
            main_list.extend(temp_list)
        else:
            main_list.extend(final_list)

    return False

def journey(end_city):
    if start_city == end_city:
        return 0,0,0,[]
    path = []
    path.append(end_city)
    while end_city != 'root':
        for i in range(len(main_list)):
            if end_city == main_list[i].id:
                path.append(main_list[i].parent_node)
                end_city = main_list[i].parent_node
                break

    del path[len(path)-1]
    count = len(path)-1
    dist = 0
    time = 0.0
    scenic_route = 0

    while count > 0:
        for f in cities_dict:
            if cities_dict[f].city1 == path[count] or cities_dict[f].city2 == path[count]:
                if cities_dict[f].city1 == path[count-1] or cities_dict[f].city2 == path[count-1]:
                    dist += cities_dict[f].length
                    # print "Speed limit",cities_dict[f].speed_limit, cities_dict[f].city1, cities_dict[f].city2
                    if cities_dict[f].speed_limit == 0:
                        cities_dict[f].speed_limit = 36
                    time += 1.0*cities_dict[f].length/cities_dict[f].speed_limit
                    if cities_dict[f].speed_limit >= 55:
                        scenic_route += 1
                    count = count - 1
                    break

    path_rev = []
    for i in reversed(path):
        path_rev.append(i)
    return [dist, time, scenic_route, path_rev]

def dist_between_cities(city1, city2):
    for f in cities_dict:
            if cities_dict[f].city1 == city1 or cities_dict[f].city2 == city1:
                if cities_dict[f].city1 == city2 or cities_dict[f].city2 == city2:
                    dist = cities_dict[f].length
                    if cities_dict[f].speed_limit == 0:
                        cities_dict[f].speed_limit = 36
                    time = cities_dict[f].length/cities_dict[f].speed_limit
                    if cities_dict[f].speed_limit > 55:
                        scenic = 1
                    else:
                        scenic = 0
    return [dist, time, scenic]

def A_star(end_city):
    global main_list
    read_road_segments()
    city_obj = city_node(start_city, 'root', 0)
    fringe = []
    fringe.append(city_obj)
    main_list.append(city_obj)
    count = 0
    try_city = city_obj
    while len(fringe) > 0:
        fringe = [x for x in fringe if x.id != try_city.id]
        p = (successor_cities(try_city))
        final_list = []
        f = 0
        for d in range(len(p)):
            add = 0
            for t in range(len(main_list)):
                if p[d].id == end_city:
                    if len(paths) == 1:
                        q = journey(paths[0])
                        q[3].insert(len(q[3]),final_city)
                        # print w[len(w)-1]
                        u = dist_between_cities(q[3][len(q[3])-1], q[3][len(q[3])-2])
                        q[0] = q[0] + u[0]
                        q[1] = q[1] + u[1]
                        q[2] = q[2] + u[2]
                        print q
                        print "Waiting for the optimal path as well"
                    if try_city.id in paths:
                            paths.remove(try_city.id)
                    if rout_option == 1:
                        paths.append(try_city.id)
                        q = journey(paths[0])
                        q[3].insert(len(q[3]),final_city)
                        # print w[len(w)-1]
                        u = dist_between_cities(q[3][len(q[3])-1], q[3][len(q[3])-2])
                        q[0] = q[0] + u[0]
                        q[1] = q[1] + u[1]
                        q[2] = q[2] + u[2]
                        print q
                        return paths
                    else:
                        paths.append(try_city.id)
                    add = 1
                    count += 1
                    # print try_city.id, count, len(paths)
                    if len(set(paths)) == t_neighbours:
                        return paths
                    else:
                        break
                if p[d].id == main_list[t].id:
                    a = journey(try_city.id)
                    m = dist_between_cities(try_city.id, p[d].id)
                    info1 = a[option] + m[option]
                    c = journey(p[d].id)
                    info2 = c[option]
                    if info1 >= info2:
                        add = 1
                        break
                    else:
                        new_parent = [x for x in main_list if x.id == p[d].id]
                        main_list =  [x for x in main_list if x.id != p[d].id]
                        main_list.append(p[d])
                        f = 1
                        fringe = [x for x in fringe if x.id != new_parent[0].id]
                        break
            if add == 0:
                final_list.append(p[d])

        fringe.extend(final_list)
        if f == 1:
            temp_list = [x for x in final_list if x.id != new_parent[0].id]
            main_list.extend(temp_list)
        else:
            main_list.extend(final_list)
        min = 200000
        for h in range(len(fringe)):
            if fringe[h].id in city_gps and final_city in city_gps:
                z = distance_lat_lon(city_gps[fringe[h].id][0],city_gps[fringe[h].id][1],city_gps[final_city][0], city_gps[final_city][1])

            elif fringe[h].id in city_gps:
                neighbour = minimum_neighbour(final_city)
                if neighbour[0] == 0:
                    z = 10
                else:
                    z = distance_lat_lon(city_gps[fringe[h].id][0],city_gps[fringe[h].id][1],neighbour[1], neighbour[2])

            elif final_city in city_gps:
                neighbour = minimum_neighbour(fringe[h].id)
                if neighbour[0] == 0:
                    z = 10
                else:
                    z = distance_lat_lon(neighbour[1], neighbour[2], city_gps[final_city][0], city_gps[final_city][1])

            if z < min:
                min = z
                try_city = fringe[h]
        # if try_city.id == final_city:
        #     return try_city.id
    return False

def minimum_neighbour(city):
    min = 200000
    neighbor_city = 'none'
    for index in cities_dict:
        if cities_dict[index].city1 == city:
            if cities_dict[index].city2 in city_gps:
                if cities_dict[index].length < min:
                    min = cities_dict[index].length
                    neighbor_city = cities_dict[index].city2

        if cities_dict[index].city2 == city:
            if cities_dict[index].city1 in city_gps:
                if cities_dict[index].length < min:
                    min = cities_dict[index].length
                    neighbor_city = cities_dict[index].city1

    if neighbor_city == 'none':
        city_gps[neighbor_city] = [0,0]
        var = 0

    # print "City",city
    return [neighbor_city, city_gps[neighbor_city][0], city_gps[neighbor_city][1]]

def total_neighbours():
    total = 0
    for index in cities_dict:
        if cities_dict[index].city1 == final_city or cities_dict[index].city2 == final_city:
            total += 1
    return total



start_city = 'Bloomington,_Indiana'
final_city = 'Indianapolis,_Indiana'
paths = []
main_list = []
cities_dict = {}
city_info_dict = {}
city_gps = {}
ids_count = 0
stop = 0
rout_algo = int(raw_input("Type 1 for bfs, 2 for dfs, 3 for ids, 4 for A star"))
algo = rout_algo - 1
rout_option = int(raw_input("1 for min edges, Type 2 for distance, 3 for time, 4 for scenic routes"))
if rout_option == 1:
    option = 0
else:
    option = rout_option - 2
read_gps()
read_road_segments()
t_neighbours = total_neighbours()
if rout_algo == 1 or rout_algo == 2:
    solve_bfs(start_city, final_city)
elif rout_algo == 3:
    solve_ids()
elif rout_algo == 4:
    A_star(final_city)
diff_paths = []
for i in range(len(paths)):
    count_speedlimit = 0
    for j in range(len(paths[i])-1):
        for y in cities_dict:
            if (cities_dict[y].city1 == paths[i][j] and cities_dict[y].city2 == paths[i][j+1]) or (cities_dict[y].city1 == paths[i][j+1] and cities_dict[y].city2 == paths[i][j]):
                if cities_dict[y].speed_limit == 0:
                    count_speedlimit += 1
    q = journey(paths[i])
    q[3].insert(len(q[3]),final_city)
    u = dist_between_cities(q[3][len(q[3])-1], q[3][len(q[3])-2])
    for h in range(3):
        q[h] = q[h] + u[h]
    diff_paths.append(q)

path = []
min = 999999
for i in range(len(diff_paths)):
    if diff_paths[i][rout_option-2] < min:
        path = diff_paths[i]
        min = diff_paths[i][rout_option-2]
print path


# print dist_between_cities('"Y"_City,_Arkansas', 'Acorn,_Arkansas')
#print try_q