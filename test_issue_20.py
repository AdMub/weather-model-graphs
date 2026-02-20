import numpy as np
from weather_model_graphs.create.mesh.kinds.hierarchical import create_hierarchical_multiscale_mesh_graph
from weather_model_graphs.visualise.plot_3d import plot_graph_3d

print("1. Generating hierarchical mesh...")
nx_ny = 10
x = np.linspace(0, 10, nx_ny)
y = np.linspace(0, 10, nx_ny)
xx, yy = np.meshgrid(x, y)
xy = np.column_stack([xx.ravel(), yy.ravel()])

# Build a 3-level graph
g = create_hierarchical_multiscale_mesh_graph(
    xy=xy, mesh_node_distance=2.0, level_refinement_factor=2, max_num_levels=3
)

print("2. Rendering 3D plot...")
# This uses the new tool you just built inside the visualise/ directory!
fig = plot_graph_3d(g, title="Issue #20 PoC: 3D Hierarchical Mesh")

print("3. Saving to HTML...")
html_file = "mesh_3d_preview.html"
fig.write_html(html_file)

print(f"✅ Success! 3D Plot saved to {html_file}")