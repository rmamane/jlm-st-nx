
import numpy as np
import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt


poly = gpd.read_file('jerus_area.geojson').loc[0, 'geometry']
G = ox.graph_from_polygon(poly, network_type='walk')


H = nx.Graph(G)
H.remove_edges_from(list(nx.selfloop_edges(H)))
nx.set_node_attributes(H, {d[0]:[d[1]['x'], d[1]['y']] for d in H.nodes(data=True)}, 'pos')
pos = nx.get_node_attributes(H, 'pos')


seed = 239
layout = nx.spring_layout(H, pos=None, iterations =3000 ,seed=seed, k=2/np.sqrt(len(H.nodes())))

q = nx.edge_betweenness_centrality(H)
q = {k: np.log10(v+1e-3) for k, v in q.items()}

vmin , vmax = min(q.values()), max(q.values())
cmap = plt.cm.inferno

px = 1/plt.rcParams['figure.dpi']  # pixel in inches
plt.figure(figsize=(2000*px, 2900*px))

drawing = nx.draw(H,     
    pos = layout,
    edgelist=list(q.keys()),
    node_size=0,
    edge_color=list(q.values()), vmin=vmin, vmax=vmax,
    edge_cmap=cmap, arrows=False, alpha=0.8, width=3
)


plt.axis('off')
plt.gca().set_position([0, 0, 1, 1])

fname = 'edge_bw_'
plt.savefig(f'./output/{fname}{cmap.name}.png', dpi='figure', bbox_inches='tight')
plt.savefig(f'./output/{fname}{cmap.name}.svg')






