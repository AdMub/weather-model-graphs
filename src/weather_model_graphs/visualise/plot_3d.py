import networkx as nx
import plotly.graph_objects as go

def plot_graph_3d(G: nx.DiGraph, title: str = "3D Weather Mesh", z_spacing: float = 10.0):
    """
    Generates a fast 3D Plotly visualization of a hierarchical graph.
    
    Parameters
    ----------
    G: nx.DiGraph
        The graph to visualize. Nodes must have 'pos' and ideally 'level' attributes.
    title: str
        The title of the plot.
    z_spacing: float
        The vertical multiplier to separate hierarchical levels.
        
    Returns
    -------
    plotly.graph_objects.Figure
    """
    node_x, node_y, node_z, node_colors = [], [], [], []
    
    # 1. Extract Nodes
    for node, data in G.nodes(data=True):
        if 'pos' not in data:
            continue
        node_x.append(data['pos'][0])
        node_y.append(data['pos'][1])
        
        # Use the level attribute for the Z-axis height
        level = data.get('level', 0)
        node_z.append(level * z_spacing) 
        node_colors.append(level)

    # 2. Extract Edges (Batched for high performance)
    edge_x, edge_y, edge_z = [], [], []
    
    for u, v, data in G.edges(data=True):
        if 'pos' not in G.nodes[u] or 'pos' not in G.nodes[v]:
            continue
            
        x0, y0 = G.nodes[u]['pos']
        z0 = G.nodes[u].get('level', 0) * z_spacing
        
        x1, y1 = G.nodes[v]['pos']
        z1 = G.nodes[v].get('level', 0) * z_spacing
        
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])

    # 3. Build Figure
    fig = go.Figure()

    # Add Edges
    fig.add_trace(go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(color='gray', width=1),
        hoverinfo='none',
        name='Connections'
    ))

    # Add Nodes
    fig.add_trace(go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers',
        marker=dict(
            size=4,
            color=node_colors,
            colorscale='Viridis',
            opacity=0.8,
            colorbar=dict(title="Hierarchy Level")
        ),
        text=[f"Node: {n}<br>Level: {c}" for n, c in zip(G.nodes, node_colors)],
        hoverinfo='text',
        name='Mesh Nodes'
    ))

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X Coordinate',
            yaxis_title='Y Coordinate',
            zaxis_title='Hierarchy Level (Z)',
            xaxis=dict(showbackground=False),
            yaxis=dict(showbackground=False),
            zaxis=dict(showbackground=False),
        ),
        showlegend=False,
        margin=dict(l=0, r=0, b=0, t=40)
    )
    
    return fig