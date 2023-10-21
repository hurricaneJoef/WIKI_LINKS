import pickle
import random

DATA_FILE = "wiki_data.pickle"

links_from_page = {}
links_to_page = {}

with open(DATA_FILE, 'rb') as handle:
    links_to_page, links_from_page = pickle.load(handle)

# get 1000 keys from links_from_page
start = random.sample(list(links_from_page.keys()), 20000)

# get 1000 keys from links_to_page
end = random.sample(list(links_to_page.keys()), 20000)

# save lists to pickle file
with open("samples_20k.pickle", 'wb') as f:
    pickle.dump((start,end), f, protocol=pickle.HIGHEST_PROTOCOL)