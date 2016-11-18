class Node:
    def __init__(self, name):
        self.name = name
        self.connections = []
        self.color = 'black'
        self.distance = 999
    
    def add_conn(self, v):
        if v not in self.connections:
            self.connections.append(v)

class Graph:
    def __init__(self):
        self.graph = {}
        self.edges_count = 0
        
    def add_vert(self, v):
        self.graph[v.name] = v
        
    def add_edge(self, v1, v2):
        error_msg = 'Error, vertice {} not present'
        self.edges_count += 1
        if v1 in self.graph.keys():
            self.graph[v1].connections.append(v2)
        else:
            print error_msg.format(v1)

        if v2 in self.graph.keys():
            self.graph[v2].connections.append(v1)
        else:
            print error_msg.format(v2)
            
    def print_graph(self, nodes=False):
        for key in sorted(list(self.graph.keys())):
            if not nodes:
                print('{} --{}-- {}'.format(key, self.graph[key].distance, self.target_num))
            else:
                print('{} {} {}'.format(key, self.graph[key].connections, self.graph[key].distance))
       
    def bfs(self, target_num):

        self.target_num = target_num
        fila = []
        target = self.graph[str(target_num)]
        target.color = 'red'
        target.distance = 0

        for v in target.connections:
            node = self.graph[v]
            # print node.name
            node.distance = target.distance + 1
            fila.append(node)

        while len(fila) > 0:
            node = fila.pop(0)
            node.color = 'red'

            for v in node.connections:
                child = self.graph[v]
                if child.color == 'black':
                    # print child.name
                    fila.append(child)

                    if child.distance > node.distance + 1:
                        child.distance = node.distance + 1

    def reset_colors_distances(self):
        for key in self.graph.keys():
            self.graph[key].color = 'black'
            self.graph[key].distance = 999
    
    def get_distances(self):
        return [self.graph[key].distance for key in self.graph.keys()]