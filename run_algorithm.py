import pickle
import time
from data_storage import dataPickle
import sorter as st

#get list of origins and destinations
LIST_FILE = "samples_20k.pickle"

with open(LIST_FILE, 'rb') as handle:
    start, end = pickle.load(handle)

#load the database
DATA_FILE = 'wiki_data.pickle'
db = dataPickle()

degs = []
outputs = []
runtimes = []

for i in range(len(start)):
    #add a way to keep track of progress
    if i % 2000 == 0 and i != 0:
        percent = len(start) // i
        print(f"At {percent}%")

    #run the algorithm
    startTime = time.time()
    deg, output = st.bfs_fast_rev(db,start[i],end[i],max_depth=20)
    execTime = (time.time() - startTime)

    #store the relevant information
    degs.append(deg)
    outputs.append(output)
    runtimes.append(execTime)

with open("wiki_stats_20k.pickle", 'wb') as f:
    pickle.dump((degs,outputs,runtimes), f, protocol=pickle.HIGHEST_PROTOCOL)

print("DONE")
