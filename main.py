from classes import Graph, Node
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__)


@app.route("/")
def hello():
    if g.edges_count >= 2:
        farness = []

        # Calculate farness for all vertices
        for node in g.graph.keys():
            g.reset_colors_distances()
            g.bfs(node)
            farness.append((node, sum(g.get_distances())))

        df = pd.DataFrame(farness)
        df.columns = ['Node', 'Farness']
        df['Closeness'] = 1/df['Farness']
        table = df.sort('Closeness', ascending=False).to_html(index=False)

        conns = ['{} - {}'.format(key, g.graph[key].connections) for key in g.graph.keys()]
        conns = pd.DataFrame(conns)
        conns = conns.to_html(index=False)
        return render_template('index.html', table=table, conns=conns)
    else:
        return render_template('index.html', msg=True)


@app.route('/edgesdat', methods=['POST'])
def edgesdat():
    run_()
    return redirect('/')


@app.route('/clean')
def clean():
    print('cleaning..')
    g.graph = {}
    g.edges_count = 0
    g.target_num = 0
    return redirect('/')


@app.route("/add_vertice", methods=['POST'])
def add_vertice():

    name = request.form['vert1_name']
    g.add_vert(Node(str(name)))
    print('Name:', name)
    return render_template('index.html', vertice_added=name,list_of_vs=g.graph.keys())


@app.route("/add_connection", methods=['POST'])
def add_connection():
    name = request.form['vert1_conn']
    name2 = request.form['vert2_conn']
    print('{} - {}'.format(name, name2))
    g.add_edge(str(name), str(name2))
    connection_added = '{} - {}'.format(name, name2)

    return render_template('index.html', connection_added=connection_added, list_of_vs=g.graph.keys())


def run_():
    with open('edges.dat', 'r') as f:
        edges = [line.replace('\n', '') for line in f]

    # Create vertices
    for i in range(100):
        g.add_vert(Node(str(i)))

    # Create edges
    for row in edges:
        v1, v2 = row.split(' ')
        g.add_edge(v1, v2)

    # farness = []
    #

    # Calculate farness for all vertices
    # for node in g.graph.keys():
    #     g.reset_colors_distances()
    #     g.bfs(node)
    #     farness.append((node, sum(g.get_distances())))
    #
    # df = pd.DataFrame(farness)
    # df.columns = ['Node', 'Farness']
    # df['Closeness'] = 1/df['Farness']
    # print(df.sort('Closeness', ascending=False))


# Create graph structure
g = Graph()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
