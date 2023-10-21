
import time
from data_storage import dataPickle


def bfs_fwd(db,starting_point,endpoint,max_depth=6):
    start = db.links_from_page[starting_point]
    paths = [[i] for i in start]
    output = []
    
    for i in range(max_depth):
        next_level = []
        while paths:
            path = paths.pop(0)
            # check for endpoint
            if endpoint in path:
                output.append(path)
            else:
                if path[-1] not in db.links_from_page:
                    continue
                for next in db.links_from_page[path[-1]]:# iter through new endpoints from old
                    next_level.append(path+[next])# add new endpoints to next level
        paths = next_level# move new endpoints to current
        if len(output):
            return i, output

def bfs_fast(db,starting_point,endpoint,max_depth=6):
    pages_to_look_at = set(db.links_from_page[starting_point])
    #if starting_point == endpoint:
    #    return 0, {}
    if endpoint in pages_to_look_at:
        return 1, {starting_point:{endpoint}}
    already_visited = set()
    output = {}
    for i in range(2,max_depth):
        next_pages = set()
        for page in pages_to_look_at:
            if page not in db.links_from_page.keys():
                continue
            if page in already_visited:
                continue
            already_visited.add(page)
            current =  db.links_from_page[page]
            current = current-already_visited
            if endpoint in current:
                length, next_layer = bfs_fast(db,starting_point,page,max_depth=i)
                length+=1
                if output:
                    for k,v in next_layer.items():
                        if k not in output.keys():
                            output[k] = set()
                        output[k].update(v)
                else:
                    output = next_layer
                if page not in output.keys():
                    output[page]=set()
                output[page].add(endpoint)
            next_pages.update(current)
        pages_to_look_at = next_pages
        if output:
            break
    if len(output)<1:
        return 1e7,{}
    return length, output

def bfs_fast_rev(db,starting_point,endpoint,max_depth=6):
    pages_to_look_at = set(db.links_to_page[endpoint])
    #if starting_point == endpoint:
    #    return 0, {}
    if starting_point in pages_to_look_at:
        return 1, {starting_point:{endpoint}}
    already_visited = set()
    output = {}
    length = 10000
    for i in range(2,max_depth):
        next_pages = set()
        for page in pages_to_look_at:
            if page not in db.links_to_page.keys():
                continue
            if page in already_visited:
                continue
            already_visited.add(page)
            current =  db.links_to_page[page]
            current = current-already_visited
            if starting_point in current:
                length, next_layer = bfs_fast_rev(db,page,endpoint,max_depth=i)
                length+=1
                if output:
                    for k,v in next_layer.items():
                        if k not in output.keys():
                            output[k] = set()
                        output[k].update(v)
                else:
                    output = next_layer
                if starting_point not in output.keys():
                    output[starting_point]=set()
                output[starting_point].add(page)
            next_pages.update(current)
        pages_to_look_at = next_pages
        if output:
            break
    if len(output)<1:
        return 1e7,{}
    return length, output

def dijkstras(db,starting_point,endpoint):
    weights = {}
    prev = {}
    if 'https://en.wikipedia.org/wiki/Main_Page' in db.links_from_page.keys():
        main  = db.links_from_page.pop('https://en.wikipedia.org/wiki/Main_Page')
        if '/wiki/Main_Page' not in db.links_from_page.keys():
            db.links_from_page['/wiki/Main_Page'] = []
        db.links_from_page['/wiki/Main_Page']+= main

    
    left_to_scan = set(db.links_from_page.keys())
    for vertex in db.links_to_page.keys():
        weights[vertex] = 1e10
    weights[starting_point] = 0
    
    while left_to_scan:
        u = min(left_to_scan, key=lambda x: weights[x])
        if u == endpoint:
            output = {}
            queue = [u]
            while queue:
                u = queue.pop(0)
                if u not in prev.keys():
                    continue
                for p in prev[u]:
                    if p not in output.keys():
                        output[p] = set()
                    output[p].add(u)
                    queue.append(p)
            return weights[endpoint], output
        left_to_scan.remove(u)
        current_dist = weights[u]
        for neighbor in db.links_from_page[u]:
            if neighbor not in left_to_scan:
                continue
            new_dist = current_dist+ 1# b/c everthing has a weight of 1
            if weights[neighbor]>new_dist:
                weights[neighbor]=new_dist
                prev[neighbor] = set([u])
            elif weights[neighbor]==new_dist:
                prev[neighbor].add(u)

#non functional atm
def bfs_double_ended(db,starting_point,endpoint,max_depth=6):
    #edge case of 0 length
    if starting_point == endpoint:
        return 0, {}
    #seconddary case of 1
    pages_from_start = set(db.links_from_page[starting_point])
    pages_to_start = set(db.links_to_page[endpoint])
    if endpoint in pages_from_start:
        return 1, {starting_point:{endpoint}}
    already_visited = set()
    output = {}
    for i in range(2,max_depth):
        next_pages = set()
        if i%2:
            for page in pages_from_start:
                if page not in db.links_from_page.keys():
                    continue
                if page in already_visited:
                    continue
                already_visited.add(page)
                current =  db.links_from_page[page]
                current = current-already_visited
                if endpoint in current:
                    _, next_layer = bfs_fast(db,starting_point,page,max_depth=i)
                    if output:
                        for k,v in next_layer.items():
                            if k not in output.keys():
                                output[k] = set()
                            output[k].update(v)
                    else:
                        output = next_layer
                    if page not in output.keys():
                        output[page]=set()
                    output[page].add(endpoint)
                next_pages.update(current)

        else:
            for page in pages_to_start:
                if page not in db.links_to_page.keys():
                    continue
                if page in already_visited:
                    continue
                already_visited.add(page)
                current =  db.links_to_page[page]
                current = current-already_visited
                if starting_point in current:
                    _, next_layer = bfs_fast_rev(db,page,endpoint,max_depth=int((max_depth/2)-i/2))
                    if output:
                        for k,v in next_layer.items():
                            if k not in output.keys():
                                output[k] = set()
                            output[k].update(v)
                    else:
                        output = next_layer
                    if starting_point not in output.keys():
                        output[starting_point]=set()
                    output[starting_point].add(page)
                next_pages.update(current)

        pages_to_look_at = next_pages
        if output:
            break
    return i, output







test_list = [
    ("/wiki/Weather_of_2016","/wiki/2016"),
    ("/wiki/Weather_of_2016","/wiki/Donald_Trump"),
    ("/wiki/Weather_of_2016","/wiki/Federal_Election_Commission"),
    ("/wiki/Olin_College","/wiki/Slime_mold"),
    ("/wiki/Olin_College","/wiki/Suite_for_Jazz_Orchestra_No._2")
]


if __name__ == "__main__":
    from visualizer import show_network
    start_time = time.time()
    db = dataPickle()
    end_time = time.time()
    print("db took ",end_time-start_time)
    print("/wiki/Olin_College" in db.links_from_page.keys())
    print("/wiki/Pigeonhole_principle" in db.links_from_page.keys())
    print("/wiki/Don't_Let_the_Pigeon_Drive_the_Bus!" in db.links_from_page.keys())


    #print("/wiki/Donald_Trump" in db.links_from_page.keys())
    for s,e in test_list:
        start_time = time.time()
        dist,path = bfs_fast_rev(db,s,e)
        end_time = time.time()
        print("this took ",end_time-start_time)
        print(path)
        show_network(path)
        None
    None
