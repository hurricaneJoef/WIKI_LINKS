from pyvis.network import Network


DEFAULT_COLOR   = "#E6A879"
END_COLOR       = "#e68878"
START_COLOR     = "#78e69a"

def show_network(input,name="test.html"):
    nt=Network(directed=True)
    if isinstance(input,dict):
        values_list = set()
        for v in input.values():
            values_list.update(v)
        for k in input.keys():
            if k not in values_list:
                nt.add_node(k.split("/wiki/",1)[1],color=START_COLOR)
                continue
            nt.add_node(k.split("/wiki/",1)[1],color=DEFAULT_COLOR)
        for k,v in input.items():
            for edge in v:
                if edge not in nt.node_ids:
                    nt.add_node(edge.split("/wiki/",1)[1],color=END_COLOR)
                nt.add_edge(k.split("/wiki/",1)[1],edge.split("/wiki/",1)[1],color="#000000")
    nt.repulsion(200)
    nt.show(name,notebook=False,)