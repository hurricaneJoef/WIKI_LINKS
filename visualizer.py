from pyvis.network import Network

def show_network(input):
    nt=Network(directed=True)
    if isinstance(input,dict):
        for k in input.keys():
            nt.add_node(k)
        for k,v in input.items():
            for edge in v:
                if edge not in nt.node_ids:
                    nt.add_node(edge)
                nt.add_edge(k,edge)
    nt.show('test.html',notebook=False)