from bs4 import BeautifulSoup as bs
import requests
from data_storage import dataPickle
import time

START_URL = r"https://en.wikipedia.org/wiki/Main_Page"
WIKI_PREFIX = "https://en.wikipedia.org"
MANDITORY_URL_CONTENTS= "/wiki"
MIN_SAVE_DELAY = 240

def add_to_dicts(database,page,links):
    """adds the given link to the 2 dicts in the database (from and to)

    Args:
        database: data_base_class: the database to update
        page: string of the url: the url as a string to be used in the database
        links: set, list or tuple of pages: list of pages linked
    """
    for link in links:
        if link not in database.links_to_page.keys():
            database.links_to_page[link]={page}
        database.links_to_page[link].add(page)

        # do the from db
    if page not in database.links_from_page.keys():
        database.links_from_page[page]=set(links)
    else:
        database.links_from_page[page].update(links)
    pass

def scrape_data(starting_point):
    """_summary_

    Args:
        starting_point (_type_): _description_
    """
    db = dataPickle()
    not_finished = True
    page = starting_point
    
    last_save = time.time()
    while not_finished:
        if not page.startswith(WIKI_PREFIX):
            full_page = WIKI_PREFIX+page
        else:
            full_page = page
        print("scrape page :",page)
        res = requests.get(full_page)
        soup = bs(res.text, "html.parser")
        links = set(())
        for link in soup.find_all("a"):
            url = link.get("href", "")
            if url.startswith(MANDITORY_URL_CONTENTS) and "/Talk:" not in url:
                url = url.split('#')[0]
                links.add(url)
        add_to_dicts(db,page,links)
        pages_i_know_of = set(db.links_to_page.keys())
        pages_ive_been_to = set(db.links_from_page.keys())
        leftover_pages = pages_i_know_of - pages_ive_been_to
        print((len(pages_ive_been_to)/len(pages_i_know_of))*100,r"% complete")
        not_finished = len(leftover_pages)>0
        page = list(leftover_pages)[0]
        time.sleep(.5)
        if time.time()-last_save > MIN_SAVE_DELAY:
            db.save()

        

if __name__ == "__main__":
    scrape_data(START_URL)