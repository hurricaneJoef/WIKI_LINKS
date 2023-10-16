import pickle
import abc

DATA_FILE = 'wiki_data.pickle'

class dataBaseClass(abc.ABC):
    """"""
    def __init__(self):
        self.links_to_page = {} # these are pages that link to the page itself
        self.links_from_page = {} # these are the pages a given page links to
        self.load()# loads data into the vars
    
    @abc.abstractmethod
    def load(self):
        return False
    
    @abc.abstractmethod
    def save(self):
        return False


class dataPickle(dataBaseClass):
    def __init__(self):
        super().__init__()
    
    def load(self):
        try:
            with open(DATA_FILE, 'rb') as handle:
                self.links_to_page,self.links_from_page = pickle.load(handle)
            return True
        except Exception as e:
            print("failed to load with exception ",e)
            return False

    def save(self):
        try:
            with open(DATA_FILE, 'wb') as handle:
                pickle.dump((self.links_to_page,self.links_from_page), handle, protocol=pickle.HIGHEST_PROTOCOL)
            return True
        except Exception as e:
            print("failed to load with exception ",e)
            return False
