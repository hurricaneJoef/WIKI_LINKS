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
    if starting_point == endpoint:
        return 0, {}
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
        pages_to_look_at = next_pages
        if output:
            break
    return i, output



test_list = [
    ("/wiki/Weather_of_2016","/wiki/2016"),
    ("/wiki/Weather_of_2016","/wiki/Donald_Trump"),
    ("/wiki/Weather_of_2016","/wiki/Federal_Election_Commission"),
    #("/wiki/Kyra_Condie","/wiki/Different_Set")
]


if __name__ == "__main__":
    from visualizer import show_network
    start_time = time.time()
    db = dataPickle()
    end_time = time.time()
    print("db took ",end_time-start_time)
    #print("/wiki/Donald_Trump" in db.links_from_page.keys())
    for s,e in test_list:
        start_time = time.time()
        dist,path = bfs_fast(db,s,e)
        end_time = time.time()
        print("this took ",end_time-start_time)
        print(path)
        show_network(path)
        None
    None